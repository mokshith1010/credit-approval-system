import io
import pandas as pd
from celery import shared_task
from .models import Customer, Loan

@shared_task
def ingest_customer_data(file_bytes):
    import pandas as pd
    import io
    from .models import Customer

    df = pd.read_excel(io.BytesIO(file_bytes))

    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            phone_number=row["Phone Number"],  # Excel column
            defaults={
                "first_name": row["First Name"],
                "last_name": row["Last Name"],
                "monthly_salary": row["Monthly Salary"],
                "approved_limit": row["Approved Limit"],
                "current_debt": 0  
            }
        )


@shared_task
def ingest_loan_data(file_bytes):
    df = pd.read_excel(io.BytesIO(file_bytes))

    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row["Customer ID"])
            Loan.objects.update_or_create(
                loan_id=row["Loan ID"],
                defaults={
                    "customer": customer,
                    "loan_amount": row["Loan Amount"],
                    "tenure": row["Tenure"],
                    "interest_rate": row["Interest Rate"],
                    "monthly_repayment": row["Monthly payment"],
                    "emis_paid_on_time": row["EMIs paid on Time"],
                    "start_date": row["Date of Approval"],
                    "end_date": row["End Date"]
                }
            )
        except Customer.DoesNotExist:
            continue

