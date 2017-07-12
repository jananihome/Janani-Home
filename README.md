# Janani-Care

## Environment configuration for developers
* Create a virtualenv with Python 3.4 or 3.5 as interpreter.
* Install requirements: `pip install -r requirements.txt`.
* Migrate database: `python manage.py migrate`.
* Load initial data for countries and states: `python manage.py loaddata countries_and_states`.
* Create superuser: `python manage.py createsuperuser`.
* Run development server: `python manage.py runserver`.
