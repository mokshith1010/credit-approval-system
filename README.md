# 💳 Credit Approval System

This is a Django-based backend application designed for managing credit approvals. It allows for customer registration, checking loan eligibility, approving loans, viewing loan details, and uploading historical loan/customer data via Excel.

---

## 🚀 Features

- Register new customers
- Check credit score and loan eligibility
- Create/approve new loans
- View loan details and list of loans per customer
- Upload customer and loan data from Excel
- All operations run inside Docker containers
- Background data ingestion using Celery + Redis

---

## 🛠️ Technologies Used

- Python 3.11
- Django 4.x
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- Pandas + Openpyxl
- Docker + Docker Compose

---

## 📦 Setup Instructions

### 1. Clone the repo

git clone https://github.com/mokshith1010/credit-approval-system.git
cd credit-approval-system

### 2. Start the system using Docker
docker-compose up --build

### 3. Run Celery Worker in new terminal
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
