# Financial Services Dependencies

## python3
    https://www.python.org/
## Django3
    pip install django
## mysql
    add mysql server details in accounts/database.py
##smtp server
    add email_server details in accounts/email_server.py
# Instructions

### pip install -r requirements.txt
### Run "python manage.py makemigrations"
### Run "python manage.py migrate"
### Run "python manage.py createsuperuser"
	Create Superuser to access/manage the database 
### Run "python manage.py runserver"
	Server runs on localhost:8000
