from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .models import Customer, Loan
from .serializers import CheckEligibilitySerializer
from rest_framework.parsers import MultiPartParser
from .tasks import ingest_customer_data, ingest_loan_data
import math

@api_view(['GET'])
def root(request):
    return Response({"message": "Loan Management API is live"})

@api_view(['POST'])
def register(request):
    data = request.data
    monthly_salary = data['monthly_income']
    approved_limit = round(36 * monthly_salary, -5)  # round to nearest lakh

    customer = Customer.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone_number=data['phone_number'],
        monthly_salary=monthly_salary,
        approved_limit=approved_limit,
        current_debt=0
    )
    return Response({
        "customer_id": customer.customer_id,
        "name": f"{customer.first_name} {customer.last_name}",
        "age": data["age"],
        "monthly_income": monthly_salary,
        "approved_limit": approved_limit,
        "phone_number": customer.phone_number
    })

class CheckEligibilityView(APIView):
    def post(self, request):
        serializer = CheckEligibilitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        customer_id = data['customer_id']
        loan_amount = data['loan_amount']
        interest_rate = data['interest_rate']
        tenure = data['tenure']

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=404)

        # Fetch customer's past loans
        past_loans = Loan.objects.filter(customer=customer)
        total_loans = past_loans.count()
        loans_this_year = past_loans.filter(start_date__year=date.today().year).count()
        total_approved_volume = sum(l.loan_amount for l in past_loans)
        on_time_payments = sum(l.emis_paid_on_time for l in past_loans)
        max_emis = sum(l.monthly_repayment for l in past_loans)

        # Base condition: if debt > approved limit or EMIs too high → credit_score = 0
        if (
            customer.current_debt > customer.approved_limit or
            (max_emis + (loan_amount / tenure)) > (0.5 * customer.monthly_salary)
        ):
            credit_score = 0
        else:
            credit_score = min(100, (
                (on_time_payments / (total_loans or 1)) * 30 +  # on-time score
                max(0, 100 - total_loans * 5) +                  # fewer loans → better
                loans_this_year * 10 +
                (total_approved_volume / (customer.approved_limit or 1)) * 10
            ))

        # Loan decision logic
        approval = False
        corrected_interest_rate = interest_rate

        if credit_score > 50:
            approval = True

        elif 30 < credit_score <= 50:
            if interest_rate >= 12:
                approval = True
            else:
                corrected_interest_rate = 12
                approval = True

        elif 10 < credit_score <= 30:
            if interest_rate >= 16:
                approval = True
            else:
                corrected_interest_rate = 16
                approval = True

        else:
            approval = False

        # Calculate monthly installment (Compound Interest EMI formula)
        monthly_interest_rate = corrected_interest_rate / (12 * 100)
        emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure) / (((1 + monthly_interest_rate) ** tenure) - 1)

        return Response({
            "customer_id": customer_id,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_interest_rate,
            "tenure": tenure,
            "monthly_installment": round(emi, 2)
        }, status=200)


class CreateLoanView(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get("customer_id")
        loan_amount = data.get("loan_amount")
        interest_rate = data.get("interest_rate")
        tenure = data.get("tenure")

        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"message": "Customer not found"}, status=404)

        monthly_interest_rate = interest_rate / (12 * 100)
        emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure) / (((1 + monthly_interest_rate) ** tenure) - 1)

        if customer.current_debt + loan_amount > customer.approved_limit:
            return Response({
                "loan_id": None,
                "customer_id": customer_id,
                "loan_approved": False,
                "message": "Loan exceeds approved limit",
                "monthly_installment": round(emi, 2)
            }, status=200)

        from datetime import date, timedelta
        start = date.today()
        end = start + timedelta(days=30 * tenure)

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            tenure=tenure,
            interest_rate=interest_rate,
            monthly_repayment=round(emi, 2),
            emis_paid_on_time=0,
            start_date=start,
            end_date=end
        )

        customer.current_debt += loan_amount
        customer.save()

        return Response({
            "loan_id": loan.loan_id,
            "customer_id": customer_id,
            "loan_approved": True,
            "message": "Loan approved",
            "monthly_installment": round(emi, 2)
        }, status=201)

class ViewLoanView(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.select_related("customer").get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=404)

        customer = loan.customer
        return Response({
            "loan_id": loan.loan_id,
            "customer": {
                "id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone_number": customer.phone_number,
                "age": None  # age was in /register input, but not stored
            },
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_repayment,
            "tenure": loan.tenure
        })


class ViewLoansByCustomer(APIView):
    def get(self, request, customer_id):
        loans = Loan.objects.filter(customer__customer_id=customer_id)

        result = []
        for loan in loans:
            repayments_left = loan.tenure - loan.emis_paid_on_time
            result.append({
                "loan_id": loan.loan_id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_repayment,
                "repayments_left": repayments_left
            })

        return Response(result)

class UploadExcelView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get("file")
        if not excel_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if "customer" in request.path:
            ingest_customer_data.delay(excel_file.read())
            return Response({"message": "Customer data upload task triggered"}, status=status.HTTP_202_ACCEPTED)

        elif "loan" in request.path:
            ingest_loan_data.delay(excel_file.read())
            return Response({"message": "Loan data upload task triggered"}, status=status.HTTP_202_ACCEPTED)

        return Response({"error": "Invalid upload endpoint"}, status=status.HTTP_400_BAD_REQUEST)

    
