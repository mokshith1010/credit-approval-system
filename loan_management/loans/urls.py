from django.urls import path
from .views import (
    root,
    register, 
    CheckEligibilityView,
    CreateLoanView,
    ViewLoanView,
    ViewLoansByCustomer,
    UploadExcelView  
)

urlpatterns = [
    path('', root),
    path('register', register),
    path('check-eligibility', CheckEligibilityView.as_view()),
    path('create-loan', CreateLoanView.as_view()),
    path('view-loan/<int:loan_id>', ViewLoanView.as_view()),
    path('view-loans/<int:customer_id>', ViewLoansByCustomer.as_view()),
    path('upload-customer-excel', UploadExcelView.as_view()),
    path('upload-loan-excel', UploadExcelView.as_view()),
]
