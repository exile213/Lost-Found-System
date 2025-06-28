# Campus Lost and Found System

A Django-based web application for managing lost and found items on campus with data analytics for behavior statistics.
This was made by Emil Joaquin H. Diaz, Clea Jene Miles, Izyl Barbosa De la Fuente as a system project for OOP

## Prerequisites

Before running this project, make sure you have:

- **Python 3.8+** installed on your system
- **pip** (Python package installer)

## Installation & Setup

### 1. Extract and Navigate to Project
Extract the downloaded zip file to your desired location, then navigate to the project directory:
```bash
cd LostAndFound
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
cd LostFoundProject
pip install -r requirements.txt
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

### 8. Access the Application
Open your browser and go to: `http://127.0.0.1:8000/`

## Features

- **User Registration & Authentication**: Students and staff can register and login
- **Report Lost Items**: Users can report lost items with details and images
- **Report Found Items**: Users can report found items
- **Claim System**: Users can claim found items
- **Analytics Dashboard**: Data analytics for behavior statistics
- **Admin Panel**: Staff management interface
- **Search Functionality**: Search for lost/found items

## Project Structure

- `AccountsApp/` - User authentication and profiles
- `ReportsApp/` - Lost and found item reports
- `ClaimsApp/` - Item claiming system
- `AnalyticsApp/` - Data analytics and statistics
- `static/` - CSS, JavaScript, and other static files
- `media/` - User uploaded files (images)
- `templates/` - HTML templates

## Default Admin Access

- URL: `http://127.0.0.1:8000/admin/`
- Use the superuser credentials created in step 6

## Troubleshooting

- If you get a "port already in use" error, try: `python manage.py runserver 8001`
- Make sure your virtual environment is activated before running commands
- If dependencies fail to install, try upgrading pip: `pip install --upgrade pip`
