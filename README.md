# room-booking-managment
The application for making and tracking room reservations. It allows users to add, edit and delete rooms. It allows booking a selected room for the whole time. The reserved room does not appear in the search results of other users. On the main page of the application users see two lists with information about available or reserved rooms on a given datetime.

## Technologies
* Python 3.8.10
* Django 4.0.4
* djangorestframework 3.13.1
* psycopg2-binary 2.9.3

## make Virtualenv:
* python3 -m venv .env 
* source .env/bin/avtivate

## LocalSetup
1) Install All Dependencies  
`pip3 install -r requirements.txt`
2) Database cofiguration 
    * change 'settings.py' 
      https://docs.djangoproject.com/en/4.0/ref/settings/#databases
    * create postgresql
      sudo docker-compose build
      sudo docker-compose up
      ./manage.py create_database.py
3) Change ``INSTALLED_APPS`` 
    INSTALLED_APPS = (
        ...,
        'room_reserve',
        'rest_framework',
        'drf_yasg',
    )
4) Run the File  
`python manage.py runserver`

## Run
http://127.0.0.1:8000/booking/core/swagger/

