# HelpDesk - College Complaint & Support Management System

A web-based complaint management application developed using Python, Flask, SQLite, HTML, and CSS.

## Features

* Student registration and login
* Password hashing
* Student dashboard
* Complaint submission
* Admin dashboard
* Complaint status management
* SQLite database integration
* Responsive website styling

## Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* Werkzeug

## Project Structure

```
HelpDesk/
├── app.py
├── create_admin.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── admin.html
└── static/
    └── style.css
```

## Installation

### 1. Clone the repository

```
git clone https://github.com/sundramsingh259-alt/HelpDesk-Complaint-Management.git
```

### 2. Open the project folder

```
cd HelpDesk-Complaint-Management
```

### 3. Create a virtual environment

```
python -m venv venv
```

### 4. Activate the environment on Windows

```
venv\Scripts\activate
```

### 5. Install Flask

```
pip install Flask
```

### 6. Run the application

```
python app.py
```

Open your browser and visit http://127.0.0.1:5000/

## How It Works

1. Students register and log in.
2. Students submit complaints.
3. Complaint information is stored in the SQLite database.
4. Administrators view submitted complaints.
5. Administrators update complaint statuses.
6. Students can check their complaint information on the dashboard.

## Learning Outcomes

* Python web development using Flask
* SQLite database integration
* User authentication
* SQL operations
* HTML and CSS
* Flask routing and sessions

## Future Improvements

* Email notifications
* Complaint categories and priorities
* Search and filtering
* Complaint reports

## Author

**Sundaram Singh**

B.Tech Student

## Purpose

Developed as an educational project to demonstrate basic web application development and complaint management.
