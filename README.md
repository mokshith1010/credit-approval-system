Credit Approval System
A Django-based backend system that handles customer registration, loan eligibility checking, loan management, and asynchronous Excel data ingestion using Celery and Redis.

🚀 Features
Customer Registration (/register)

Loan Eligibility Check (/check-eligibility)

Loan Creation (/create-loan)

Loan Detail View (/view-loan/<loan_id>)

View Customer Loans (/view-loans/<customer_id>)

Excel Upload (Async via Celery):

Upload Customer Data (/upload-customer-excel)

Upload Loan Data (/upload-loan-excel)

🛠️ Tech Stack
Python 3.11

Django 4+

Django REST Framework

PostgreSQL

Celery + Redis (background task processing)

Pandas & Openpyxl (Excel file parsing)

Docker & Docker Compose

⚙️ Setup Instructions
1. Clone the Repository

git clone https://github.com/your-username/credit-approval-system.git
cd credit-approval-system

2. Start Services with Docker
docker-compose up --build

3. Run Celery Worker
In a separate terminal:
docker-compose exec web celery -A loan_management worker --loglevel=info


##  API Endpoints
Method	          Endpoint                         	Description
POST	            /register	                  Register a new customer
POST	            /check-eligibility	        Check customer’s credit eligibility
POST	            /create-loan               	Approve and create a loan
GET	              /view-loan/<loan_id>	      Get loan and customer info
GET               /view-loans/<customer_id>	  List all loans for a customer
POST	           /upload-customer-excel       Upload customer data from Excel
POST	           /upload-loan-excel         	Upload loan data from Excel
