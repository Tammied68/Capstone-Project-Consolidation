# 📰 News Management System (Capstone Project)

Repository:
https://github.com/Tammied68/Capstone-Project-Consolidation

## 📌 Overview

This project is a Django-based News Management System developed as part of a capstone assignment. It demonstrates full-stack web development skills including authentication, role-based access control, REST APIs, documentation, version control, and containerization.

The system supports multiple user roles and allows controlled creation, approval, and consumption of news articles.



## ✨ Features

### 👥 User Roles

* **Reader**

  * View approved articles
  * Subscribe to publishers and journalists

* **Journalist**

  * Create and manage articles
  * Submit articles for approval

* **Editor**

  * Review and approve submitted articles

* **Admin**

  * Full access via Django admin panel



### 📰 Article Workflow

1. Journalist creates an article
2. Article is marked as **pending**
3. Editor reviews and approves the article
4. Approved articles become visible to readers



### 🔐 Authentication

* Django built-in authentication system
* Login is **username-based**
* Role-based access control enforced


### 🌐 API

* Endpoint: `/api/subscribed-articles/`
* Returns articles based on user subscriptions
* Requires API key via `X-API-KEY` header


## 🛠️ Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* Docker
* Git & GitHub
* Sphinx (documentation)



## ⚙️ Setup with Virtual Environment

```bash
# Clone the repository
git clone https://github.com/Tammied68/Capstone-Project-Consolidation.git

cd Capstone-Project-Consolidation
```


# Activate environment
source venv312/bin/activate   # Mac/Linux
venv312\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run server
python manage.py runserver


## 🐳 Running with Docker
## 🐳 Docker Verification

Build:

```bash
docker build -t news_project .
```

Run:

```bash
docker run -p 8000:8000 news_project
```

Access:

```text
http://localhost:8000
```

> Passwords can be reset using:

docker exec -it <container_name> python manage.py changepassword <username>


## 📚 Documentation was generated using Sphinx.

To rebuild documentation:

```bash
cd docs
sphinx-apidoc -o source ../
make html
```

Generated files can be found in:

```text
docs/build/html/
```

## 📦 Project Structure


accounts/       # Custom user model & roles
news/           # Core application logic
docs/           # Sphinx-generated documentation
Dockerfile      # Container configuration
requirements.txt
README.md
capstone.txt


## 🔄 Version Control

This project uses Git with structured branching:

* `main` → final merged project
* `docs` → documentation and docstrings
* `container` → Docker setup

## ⚠️ Notes

* Do not commit sensitive data (e.g., API keys, passwords)
* Uses SQLite for simplicity
* Authentication uses **username**, not email

## 📌 Capstone Submission

This repository fulfills the following requirements:

* Version control with Git
* Branching strategy (`docs`, `container`)
* Documentation using Sphinx
* Docker containerization
* Requirements file for dependencies

## 👩‍💻 Author

TammieD
