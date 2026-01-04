# 🚀 Credit Approval System

The **Credit Approval System** is a scalable backend application designed to automate **loan eligibility evaluation and loan management** for financial institutions. It provides a robust RESTful API to handle customer registration, credit eligibility checks, loan approvals, and loan history management.

Built using **Django and Django REST Framework**, the system supports **asynchronous background processing** with **Celery and Redis**, ensuring efficient handling of bulk data operations such as Excel-based customer and loan uploads. The entire application is containerized using **Docker**, enabling consistent and seamless deployment across environments.

---

## ✨ Key Features

### 🔐 Customer & Loan Management
- Register customers and maintain detailed credit profiles.
- Evaluate loan eligibility based on credit score, income, and loan history.
- Approve and create loans with configurable interest rates and tenure.
- Retrieve individual loan details or complete loan history per customer.

### ⚙️ RESTful API Architecture
- Well-structured REST APIs built using **Django REST Framework**.
- Clean separation of business logic and API layers.
- Easily extensible for future features.

### 📊 Bulk Data Ingestion
- Upload large customer and loan datasets using Excel files.
- Data processing handled using **Pandas**.
- Background execution to prevent API blocking.

### 🚀 Asynchronous Task Processing
- Integrated **Celery + Redis** for long-running and compute-intensive tasks.
- Improves responsiveness and scalability of the system.

### 🐳 Containerized Deployment
- Fully containerized using **Docker and Docker Compose**.
- One-command setup for local development.
- Consistent environment across machines.

### 🗄️ Database Management
- Uses **PostgreSQL** for secure and scalable data storage.
- Designed relational schema for efficient querying.

---

## 📦 Setup Instructions

Follow the steps below to run the application locally using Docker.

### 1️⃣ Clone the Repository
- git clone https://github.com/mokshith1010/credit-approval-system.git
- cd credit-approval-system

### 2️⃣ Start the Application using Docker
This command builds and starts all services including Django, PostgreSQL, Redis, and Celery.

- docker-compose up --build

### 3️⃣ Run the Celery Worker (in a New Terminal)
Celery processes background tasks such as Excel data ingestion.

- docker-compose exec web celery -A loan_management worker --loglevel=info

Once all services are running, the API will be accessible locally.

## 🔗 API Endpoints

### 📌 Customer & Loan APIs

| Method | Endpoint | Description |
|:------:|----------|-------------|
| POST | `/register` | Register a new customer |
| POST | `/check-eligibility` | Check customer credit eligibility |
| POST | `/create-loan` | Approve and create a loan |
| GET | `/view-loan/<loan_id>` | View loan and customer details |
| GET | `/view-loans/<customer_id>` | View all loans for a customer |

---

### 📊 Data Upload APIs

| Method | Endpoint | Description |
|:------:|----------|-------------|
| POST | `/upload-customer-excel` | Upload customer data from Excel |
| POST | `/upload-loan-excel` | Upload loan data from Excel |

