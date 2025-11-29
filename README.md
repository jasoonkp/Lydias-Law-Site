# Lydias-Law-Site

## Getting Started 🚀

### 🛠️ Prerequisites 
- Python 3.8 or higher installed
- A configured database (or access credentials ready)
- Google, Calendly, and Stripe API keys prepared for your .env file

## ⚙️ Configuration

### 1. Create and activate virtual environment

#### MacOS / Linux
```
$ python3 -m venv venv/
$ source venv/bin/activate
```
#### Microsoft
```
PS> py -m venv .venv\
PS> .venv\Scripts\activate
```

### 2. Install necessary python packages (virtual environment should be activated before)
```
$ pip install -r requirements.txt
```
### 3. Setting Up .env File 🔐
#### MacOS / Linux
```
cp .env.example .env
```
#### Windows
```
copy .env.example .env
```
#### Configure the .env File
###### Open the newly created .env file and fill in all the required environment variables (e.g., DATABASE_URL, SECRET_KEY, email settings, API keys, etc)
###### ⚠️The application will not run properly without valid environment variables⚠️ 

### 4. Running the Django Server ▶️
#### Start the development Server once environment variables and dependencies are configured
```
python manage.py runserver
```

## 🧱 Architecture Overview

### Project Application (`Lydias_Law_Site`)
- Stores the main project configuration, including:
  - Global Django settings
  - Root URL routing
  - WSGI/ASGI setup

### Core Application (`core`)
- Contains most of the website’s foundational functionality, including:
  - All primary HTML templates
  - Main URL paths
  - Core view logic used across the site

### Additional Applications

#### 📅 Appointments (`appointments`)
- Handles all Calendly-related operations, including sending and receiving API data.
- Includes database models for:
  - Appointments
  - Invitees
  - Notifications

#### 💰 Finances (`finances`)
- Contains models for payments and invoices.
- Will integrate with Stripe for financial transactions and tracking.

#### 📝 Site Content (`sitecontent`)
- Powers the Home, About, and Contact pages.
- Contains models for storing dynamic site content.

#### 👤 Users (`users`)
- Manages all authentication and account processes, including:
  - Login and signup
  - Email verification
  - Secure user session handling
- Includes models for:
  - User profiles
  - Admin profiles

## 🧑‍💻 Tech Stack Overview
### Frontend:
- Mark-up/Styling: HTML/CSS
- Framework: Bootstrap
### Backend:
- Programming Language: Python
- Framework: Django
- Database: MySQL

## Authors
- Hunter Powell
- Michael Kenny
- Jason Prakash
- Moises Robledo
- Maria Adil
- Regina Gil
- Alex Giovannini
- Nayeli Flores Valdez