# Lydias-Law-Site

## Authors
- Hunter Powell
- Michael Kenny
- Jason Prakash
- Moises Robledo
- Maria Adil
- Regina Gil
- Alex Giovannini
- Nayeli Flores Valdez

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

## Features

### 1. Overview
Lydia's Law Site gives clients information about Lydia A. Suprun and her practice areas as an adoption lawyer. Clients can schedule appointments with her and make payments through the site. Aditionally, admin has control of what information the site contains and is able to manage appointments and payments.

### 2. Appointment Scheduling
- Clients can schedule appointments through the Contact Page or through their dashboard once they log in 
- Admin can schedule appointments for clients through their dashboard once they log in
- Clients will automatically recieve an email confirmation and reminder with appointment information

### 3. Payment
- Clients without an account are able to make payments through the payment page after recieving an invoice number
- Clients with an account can automatically see how much they owe and make payments after they log in

### 4. Client Dashboard
Through their dashboards, clients can:
- Schedule, cancel, and view upcoming appointments
- Make payments and view past transactions

### 5. Admin Dashboard
Through their dashboard, admin can:
- Schedule, cancel, and view upcoming and past appointments
- View complete and uncomplete transaction
- View client list
- Make edits to the content of the site
