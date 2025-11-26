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

##🚀 Getting Started

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
### 3.🔐 Setting Up .env File
#### MacOS / Linux
```
cp .env.example .env
```
#### Windows
```
copy .env.example .env
```
#### Configure the .env File
##### Open the newly created .env file and fill in all the required environment variables (e.g., DATABASE_URL, SECRET_KEY, email settings, API keys, etc)
⚠️ The application will not run properly without valid environment variables

### 4. ▶️ Running the Django Server
#### Start the development Server once environment variables and dependencies are configured
```
python manage.py runserver
```
