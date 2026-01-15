# Django Task Management System

A web-based **Task Management System** built with **Django & Django REST Framework** to create, assign, update, and track task with user authentication and role-based access.

---

## Project Overview

This Django application allows users to manage task in an organized way. The app supports multiple user types (e.g., admin and employee), task categorization, and basic task lifecycle management - from creation to completion.

---

## Features

1. User Registration & Login
2. Role-based access control (Admin/ Employee)
3. Create, Edit, Delete Tasks
4. Assign tasks to users
5. Track task status (e.g., Pending / In Progress / Completed)
6. User-specific task views
7. Secure email configuration
8. Environment variable based on configuration (no secrets in code)
9. Real-time sends email when task is assign

> The repository includes app like `tasks` and `users` , with Django project scaffolding found in `task_manager/`.
> (Exact file-by-file implementation may vary.)

---

## Project Structure

```bash
django-task-management-system/
├── task_manager/ # Main Django project
│ ├── init.py
│ ├── settings.py # Django settings
│ ├── urls.py # Project URLs
│ └── wsgi.py # WSGI entry point
├── tasks/ # Tasks app (models, views, templates)
│ ├── migrations/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── templates/
├── users/ # Custom user management app
│ ├── migrations/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── templates/
├── manage.py # Django CLI entry point
├── .gitignore
└── README.md
```

## Tech Stack

- **Backend**: Django (Python) & Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django Auth
- **Email**: SMTP (Gmail)
- **Environment Config**: python-decouple

## Getting Started (Local Setup)

Follow these steps to run the project on your machine:

### 1. Clone the repository

```bash
git clone https://github.com/Vishwa-Bhalodiya/django-task-management-system.git
cd django-task-management-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
.\.venv\Scripts\Activate.ps1 #Windows
source venv/bin/activate #macOs/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env file (IMPORTANT)

Create a .env file in the project root (same level as manage.py) :

```bash
SECRET_KEY=your_secret_key

DB_NAME=task_manager_db
DB_USER=task_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 5. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```







