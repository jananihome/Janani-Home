# Janani-Care

## Environment configuration for developers
* Create virtual environment with Python 3.4+ and activate it.
* Install project requirements: `pip install -r requirements.txt`.
* Create `.env` file in project root and add config variables (see example below).
* Migrate database: `python manage.py migrate`.
* Load initial data for countries and states: `python manage.py loaddata countries_and_states`.
* Create superuser: `python manage.py createsuperuser`.
* Run development server: `python manage.py runserver`.

## Example .env file for development
```
ALLOWED_HOSTS=127.0.0.1,0.0.0.0,localhost
DATABASE_URL=sqlite:////media/m/DATA/code/jananihome/db.sqlite3
DEBUG=True
SECRET_KEY=+vza#nc9(w-c9z_l5ek5p(t#d3_jee4-ekplyi6(6evgr^uukc
```
