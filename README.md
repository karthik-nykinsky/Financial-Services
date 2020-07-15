# Financial Services Dependencies

## python3
    https://www.python.org/
## Django3
    pip install django
## mysqlclient
    pip install mysqlclient
## Pillow
    pip install Pillow

# Instructions

### pip install -r requirements.txt
### Connect to Mysql by changing database.py
### Connect to SMTP server by changing email_server.py
### Run "python manage.py makemigrations"
### Run "python manage.py migrate"
### Run "python manage.py createsuperuser"
	Create Superuser to access/manage the database 
### Run "python manage.py runserver"
	Server runs on localhost:8000

## Note
	Insert the services table in database prior to running the app
