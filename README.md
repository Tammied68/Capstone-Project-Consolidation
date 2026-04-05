# 📰 News Application (Django Capstone Project)

# https://github.com/Tammied68/Capstone-News-Appliation

## 📌 Overview

This project is a full-stack **News Application** built using Django. It allows users with different roles (Reader, Journalist, Editor) to interact with articles through a structured workflow.

The application supports:

* Role-based access control
* Article creation and approval workflow
* Subscription-based content delivery
* RESTful API for third-party clients
* Email notifications on article approval

---

## 🚀 Features

### 👤 User Roles

* **Reader**

  * View approved articles
  * Subscribe to publishers and journalists
* **Journalist**

  * Create, edit, and manage articles
* **Editor**

  * Review and approve articles before publication

---

### 📝 Article Workflow

1. Journalist creates an article
2. Article is marked as *pending*
3. Editor reviews and approves the article
4. Approved articles become visible to readers
5. Email notification is sent to subscribers

---

### 🔐 Authentication & Authorization

* Custom user model with roles
* Django Groups and Permissions
* Login/logout system using Django auth

---

### 📡 REST API

Endpoint:

```text
/api/subscribed-articles/
```

Features:

* Returns approved articles only
* Filters by subscribed publishers and journalists
* Requires API key in header:

```text
X-API-KEY: your_api_key
```

---

### 📧 Email Notifications

* Triggered when an article is approved
* Sent to users subscribed to the article’s publisher or journalist
* Uses Django console email backend for development

---

## 🗄 Database Design

The application uses normalized models:

* **CustomUser**
* **Publisher**
* **Article**
* **Newsletter**
* **APIClientSubscription**

Relationships:

* Users subscribe to publishers/journalists
* Articles belong to publishers and authors
* Editors approve articles

---

## 🧪 Testing

Unit tests were implemented using Django’s testing framework.

Run tests:

```bash
python manage.py test news -v 2
```

---

## ⚙️ Installation & Setup

### 1. Clone repository

```bash
git clone <your-repo-url>
cd news_project
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser

```bash
python manage.py createsuperuser
```

### 6. Run server

```bash
python manage.py runserver
```

---

## 🔑 Default Routes

| Route                       | Description          |
| --------------------------- | -------------------- |
| `/accounts/login/`          | Login page           |
| `/reader-dashboard/`        | Reader dashboard     |
| `/journalist-dashboard/`    | Journalist dashboard |
| `/editor-dashboard/`        | Editor dashboard     |
| `/articles/create/`         | Create article       |
| `/articles/pending/`        | Pending articles     |
| `/api/subscribed-articles/` | API endpoint         |

---

## 🧪 API Testing (Postman)

Include header:

```text
X-API-KEY: your_api_key
```

Test cases:

* Valid API key → returns articles
* Missing API key → error
* Invalid API key → error

---

## 📸 Screenshots

The following screenshots are included:

* Login and role dashboards
* Article creation
* Editor approval workflow
* Reader view of approved articles
* API response
* Unit test results
* Email notification output

---

## 🗄 MariaDB Migration

The project supports migration from SQLite to MariaDB by updating the `DATABASES` configuration in `settings.py`.

---

## 🧹 Code Quality

* Follows PEP 8 guidelines
* Modular and readable code
* Defensive programming practices
* Clear separation of concerns (models, views, templates)

---

## 🎯 Conclusion

This project demonstrates:

* Full-stack Django development
* Role-based system design
* API development with DRF
* Database normalization
* Real-world workflow implementation

---

## 👩‍💻 Author

**Tammie Davis**

---

