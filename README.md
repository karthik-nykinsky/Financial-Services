# Financial Services Dependencies

## python3
    https://www.python.org/
## Django3
    pip install django
## smtp server
    add email_server details in accounts/email_server.py
## psycopg2
    pip install psycopg2

# Instructions

### pip install -r requirements.txt
### Connect to Postgres in settings.py
### Run "python manage.py makemigrations"
### Run "python manage.py migrate"
### Run "python manage.py createsuperuser"
	Create Superuser to access/manage the database 
### Run "python manage.py runserver"
	Server runs on localhost:8000
