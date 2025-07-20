# Credit Approval System

This is a backend Django-based Credit Approval System that allows customer registration, loan eligibility checks, loan management, and background ingestion of Excel data using Celery and Redis.

---

## 🚀 Features

- Customer Registration (`/register`)
- Loan Eligibility Check (`/check-eligibility`)
- Loan Creation (`/create-loan`)
- View Loan Details (`/view-loan/<loan_id>`)
- View All Loans by Customer (`/view-loans/<customer_id>`)
- Background Excel Upload:
  - Upload Customer Data (`/upload-customer-excel`)
  - Upload Loan Data (`/upload-loan-excel`)

---

## 🛠️ Tech Stack

- Python 3.11
- Django 4+
- Django REST Framework
- PostgreSQL
- Celery + Redis (for background tasks)
- Docker & Docker Compose
- Pandas & Openpyxl (for Excel processing)

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/credit-approval-system.git
cd credit-approval-system

### 2. Start the system using Docker
bash
Copy
Edit
docker-compose up --build

### 3. Run Celery Worker in new terminal
bash
Copy
Edit
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
