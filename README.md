# Full Stack Developers Nano Degree Program
Welcome to my Capstone Project for Full Stack Developers Nano Degree program. This part is the explanatory documents required for you to get started!

# Casting Agency API
This API is responsible for creating, managing movies and actors. 

## Objectives
1. Create two database models of 'Movie' and 'Actor' in 'models.py'
2. Create a CRUD RESTful API using Flask in 'app.py'
3. Provide the verification of permissions of the user's role in 'auth.py'
4. Automate tests in 'test_app.py'
5. Deploy applications using heroku

## Getting Started
### Dependencies
- Alembic
- Flask
- Flask-CORS
- Flask-Migrate
- Flask-SQLAlchemy
- Werkzeug
- Gunicorn

### Installing Dependencies

#### Python 3.7

Refer to the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) on instructions to install the latest version of python on your platform

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

### Populate the Database
You can use 'movies.psql' to populate the database. Create the database using createdb command and populate them using psql command. These are all packaged under 'set_db.sh':
```
source ./set_db.sh
```
