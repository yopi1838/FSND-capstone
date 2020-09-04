# Full Stack Developers Nano Degree Program
Welcome to my Capstone Project for Full Stack Developers Nano Degree program. This part is the explanatory documents required for you to get started!

# Casting Agency API
This API is responsible for creating, managing movies and actors. 

## Objectives
1. Create two database models of `Movie` and `Actor` in `models.py`
2. Create a CRUD RESTful API using Flask in `app.py`
3. Provide the verification of permissions of the user's role in `auth.py`
4. Automate tests in `test_app.py`
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

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

### Populate the Database
You can use `movies.psql` to populate the database. Create the database using createdb command and populate them using psql command. These are all under `set_db.sh`:
```
source ./set_db.sh
```

### Running the server
To run the server, execute:

```bash
$ source setup.sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```
or simply:

```bash
$ source ./setup.sh
$ flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` which directs flask to find the application consisting of all the main app methods.

## User Roles and Permissions:
- Casting Assistant
    - Can view actors and movies. These include permissions:
        - 'get:movies'
        - 'get:actors'

- Casting Director
    - All permissions a Casting Assistant has, including:
    - Add or delete an actor from the database. These actions need permissions:
        - 'post:actors'
        - 'delete:actors'
    - Modify actors or movies. These actions need permissions:
        - 'patch:actors'
        - 'patch:movies'

- Executive Producer
    - All permissions a Casting Director has, including:
    - Add or delete a movie from the database. These actions need permissions:
        - 'post:movies'
        - 'delete:movies'

- Note: We can check the payload of a user's JWT token can be decoded at [jwt.io](https://jwt.io/) to see permission for each token. 

## Deployment
The API is deployed using Heroku

## Endpoints
- GET '/movies'
- GET '/actors'
- POST '/movies'
- POST '/actors'
- PATCH '/movies/<int:movie_id>'
- PATCH '/actors/<int:actor_id>'
- DELETE '/movies/<int:movie_id>'
- DELETE '/actors/<int:actor_id>'

### GET '/movies'
- Fetches a dictionary of movies consisting of movie title and its corresponding release date
- Required Permission: `get:movies`
- Request Arguments: None
- Returns: A JSON object with 2 key-value pairs; movies (return the formatted movies), total_movies( return the total movies in the database)
```JSON
{
    "movies":[
    {
        "id": 5,
        "title": "Deadpool",
        "release_date": "2020-02-29 16:33:41"
    },
    {
        "id": 6,
        "title": "Harry Potter and The Prisoner of Azkaban",
        "release_date": "2004-06-26 10:45:24"
    },
    {
        "id": 3,
        "title": "Back to The Future",
        "release_date": "1985-12-07 21:37:24"
    }
    ],
    "success": true
}
```

### GET '/actors'
- Fetches dictionary of actors
- Required Permission: `get:actors`
- Request Arguments: None
- Returns: A JSON object with two key-value pairs; actors (return the formatted actors), and total_actors(return the total actors in the database)
```JSON
{
    "actors":[
    {
        "id": 1,
        "name": "Robert De Niro",
        "age": 77,
        "gender": "Male"
    },
    {
        "id":2,
        "name": "Gerard Butler",
        "age": 40,
        "gender": "Male"
    },
    {
        "id":3,
        "name": "Jerry Seinfeld",
        "age": 60,
        "gender": "Male"
    }
    ],
    "success": true
}
```

### POST '/movies'
- POST movies into the database
- Required Permission: `post:movies`
- Request Arguments: JSON object with title and release_date key-value pairs
```JSON
{
    "title": "Jumanji",
    "release_date": "2020-01-09 00:40:23"
}
```
- Returns: A JSON object with the movie title and total of the movies in database
```JSON
{
    "success": true,
    "title": "Jumanji",
    "total_movies": 6
}
```

### POST '/actors/'
- POST actors into the database
- Required Permission: `post:actors`
- Request Arguments: JSON object with name, age, and gender key-value pairs
```JSON
{
    "name": "Gerard Butler",
    "age": 40,
    "gender": "Male"
}
```


