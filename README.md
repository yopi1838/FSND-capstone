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
- Run `token.sh` to export the token for each roles
```bash
source token.sh
```
- Note: We can check the payload of a user's JWT token can be decoded at [jwt.io](https://jwt.io/) to see permission for each token. 

## Deployment
The API is deployed using Heroku. You can run them [here] (https://castingagencyyopi.herokuapp.com/)

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
        "id": 3,
        "title": "Deadpool",
        "release_date": "2020-02-29 16:33:41"
    },
    {
        "id": 5,
        "title": "Harry Potter and The Prisoner of Azkaban",
        "release_date": "2004-06-26 10:45:24"
    },
    {
        "id": 6,
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

### POST '/actors'
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

### PATCH '/movies/<int:movie_id>'
- PATCH a movie entry based on the `movie_id`
- Required Permission: `patch:movies`
- Request Arguments: A JSON object with title and release_date key-value pairs
```JSON
{
    "title": "Back to The Future",
    "release_date": "1985-12-07 21:37:24"
}
```
- Returns: A JSON object with success indicator and the id of the updated movie
```JSON
{
    "success": true,
    "id": 6
}
```

### PATCH '/actors/<int:actor_id>'
- PATCH an actor entry based on the `actor_id`
- Required Permission: `patch:movies`
- Request Arguments: A JSON object with name, age, and gender key-value pairs
```JSON
{
    "name": "Tom Holland",
    "age": 23,
    "gender": "Male"
}
```
- Returns: A JSON object with success indicator and the id of the updated actor
```JSON
{
    "success": true,
    "id": 2
}
```

### DELETE '/movies/<int:movie_id>'
- DELETE a movie entry from database based on the `movie_id`
- Required Permission: `delete:movies`
- Required Arguments: None
- Returns: A JSON object with success indicator and the id of the deleted movie and current dictionary of movies in the database
```JSON
{
    "success": true,
    "delete": 6,
    "movies_now": [
    {
        "id": 3,
        "title": "Deadpool",
        "release_date": "2020-02-29 16:33:41"
    },
    {
        "id": 5,
        "title": "Harry Potter and The Prisoner of Azkaban",
        "release_date": "2004-06-26 10:45:24"
    }
    ]
}
```

### DELETE '/actors/<int:actor_id>'
- DELETE an actor entry from database based on `actor_id`
- Required Permission: `delete:actors`
- Required Arguments: None
- Returns: A JSON object with success indicator and the id of the deleted actor and current dictionary of actors in the database
```JSON
{
    "success": true,
    "delete": 3,
    "actors_now": [
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
    }
    ]
}
```

## Testing API
Create the database for API testing by running
```
source test_db.sh
```
Note: the above command runs on postgres, if have not installed yet [link](https://www.postgresql.org/download/)

To run the tests, run
```bash
source setup.sh
python3 test_app.py
```

## Authors
Yopi Prabowo Oktiovan

## Acknowledgement
Author would like to thank Udacity for the content of the FSND course and the help of mentors throughout the course. 
