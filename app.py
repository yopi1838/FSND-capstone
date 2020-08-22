import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#import database models from models.py
from models import setup_db, Movie, Actor
from auth impiort AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  #Setup CORS. Set all endpoints for origins. 
  cors = CORS(app, resources={r"/api/*":{"origins":"*"}})

  #Add after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE')
    return response
  '''
  Create endpoint for index to greet users
  '''
  #Coded by self at Wed 19th Aug 2020, 23:41 JST
  @app.route('/')
  def index():
    return 'Hello, World! Welcome to my Capstone project. Have fun!'

  '''
  Create Endpoint to handle GET requests for all movies
  '''
  @app.route('/movies', methods=['GET'])
  def return_movies():
    try:
      #query the movie and format them with the defined methods.
      movies = Movie.query.order_by(Movie.id).all()
      formatted_movies = [movie.format() for movie in movies]
      if len(movies)== 0:
        abort(404)
      return jsonify({
        'success': True,
        'movies': formatted_movies,
        'total_movies': len(formatted_movies)
      })
    except:
      abort(422)

  '''
  Create Endpoint tohandle GET requests to handle all actors
  '''
  @app.route('/actors')
  def return_actors():
    try:
      #query the actor and format them with previously defined methods
      actors = Actor.query.order_by(Actor.id).all()
      formatted_actors = [actor.format() for actor in actors]
      if len(actors) == 0:
        abort(404)
      return jsonify({
        'success': True,
        'actors': formatted_actors,
        'total_actors': len(formatted_actors)
      })
    except:
      abort(422)
    
  '''
  Create an endpoint to POST new movies
  This requires title and release date.
  '''
  @app.route('/movies', methods=['POST'])
  def create_movies():
    try:
      body = request.get_json()
      if not body:
        abort(400)
      new_title = body.get('title', None)
      new_release_date = body.get('release_date', None)
      movie = Movie(title=new_title, release_date=new_release_date)
      movie.insert()
      result = {
        'success': True,
        'title': new_title,
        'total_movies': len(Movie.query.all())
      }
      return jsonify(result)
    except:
      abort(422)
      result = {
        'success': False
      }
      return jsonify(result)

  '''
  Create an endpoint to POST new actors
  This requires name, age, and gender
  '''
  @app.route('/actors', methods=['POST'])
  def create_actors():
    try:
      body = request.get_json()
      if not body:
        abort(400)
      new_name = body.get('name', None)
      new_age = body.get('age', None)
      new_gender = body.get('gender', None)
      actor = Actor(name=new_name, age=new_age, gender=new_gender)
      actor.insert()
      actors = Actor.query.order_by(Actor.id).all()
      formatted_actors = [actor.format() for actor in actors]
      result = {
        'success': True,
        'actor': formatted_actors,
        'total_actor': len(Actor.query.all())
      }
      return jsonify(result)
    except Exception as e:
      print(e)
      abort(422)
      

  '''
  Create endpoint to DELETE movies based on the movie ID.
  '''
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  def delete_movies(movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if movie is None:
        abort(404)
      movie.delete()
      selections = Movie.query.order_by(Movie.id).all()
      formatted_movie = [selection.format() for selection in selections]
      return jsonify({
        'success': True,
        'delete': movie_id,
        'movies_now': formatted_movie
      })
    except:
      abort(422)
  
  '''
  Create endpoint to DELETE actors based on the actor ID.
  '''
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  def delete_actors(actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      if actor is None:
        abort(404)
      actor.delete()
      selections = Actor.query.order_by(Actor.id).all()
      formatted_actors = [selection.format() for selection in selections]
      return jsonify({
        'success': True,
        'delete': actor_id,
        'actors_new': formatted_actors
      })
    except:
      abort(422)

  '''
  Create endpoint to PATCH movies based on the movie ID
  '''
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  def update_movies(movie_id):
    body = request.get_json()
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if movie is None:
        abort(404)
      movie.title = body.get('title', None)
      movie.release_date = body.get('release_date', None)
      movie.update()
      return jsonify({
        'success': True,
        'id': movie_id
      })
    except:
      abort(422)

    '''
    Create endpoint to PATCH actors based on the actor ID
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def update_actors(actor_id):
      body.request.get_json()
      try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
          abort(404)
        actor.name = body.get('name', None)
        actor.age = body.get('age', None)
        actor.gender = body.get('gender', None)
        actor.update()
        return jsonify({
          'success': True,
          'id': actor_id
        })
      except:
        abort(422)

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)