# HelpDesk - College Complaint & Support Management System

## About the Project

HelpDesk is a web-based College Complaint & Support Management System developed using Python and Flask. It helps students submit complaints and allows administrators to manage complaints and update their status.

The project aims to make complaint management easier, faster, and more organized within a college.

## Features

* Student registration and login
* Secure password hashing
* Student dashboard
* Complaint submission
* Admin login and dashboard
* View and manage student complaints
* Update complaint status
* SQLite database integration
* Simple and user-friendly interface

## Technologies Used

* **Python** - Backend programming
* **Flask** - Web framework
* **SQLite** - Database
* **HTML** - Web page structure
* **CSS** - Website styling
* **Werkzeug** - Password hashing

## Project Structure

```text
HelpDesk/
├── app.py
├── create_admin.py
├── database.db
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

The `database.db` file is created by the application when required. It may not be included in the GitHub repository.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the Project Folder

```bash
cd HelpDesk
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install Flask
```

### 6. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## How It Works

1. Students create an account and log in.
2. Students submit complaints through their dashboard.
3. The application stores complaint information in the SQLite database.
4. The administrator logs in to view submitted complaints.
5. The administrator updates complaint statuses.
6. Students can log in to view their dashboard and complaint information.

## Learning Outcomes

Through this project, I learned about:

* Developing web applications using Flask
* Connecting Python applications to SQLite
* Implementing user registration and login
* Using object-independent database operations and SQL queries
* Creating web pages with HTML and CSS
* Managing application routes and user sessions
* Implementing basic role-based access control

## Future Improvements

* Email notifications for complaint updates
* Complaint categories and priority levels
* Search and filtering options
* Complaint statistics and reports

## Author

**Sundaram Singh**

B.Tech Student

## License

This project was developed for educational purposes.
