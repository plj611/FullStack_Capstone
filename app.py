import os
import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Gender, Movie

from auth import AuthError, requires_auth

def create_app():
  # create and configure the app

  #print(__name__)
  app = Flask(__name__)
  CORS(app)
  #setup_db(app, os.getenv('SQLALCHEMY_DATABASE_URI'))
  #setup_db(app, os.getenv('DATABASE_URI'))
  #setup_db(app, os.environ['DATABASE_URL'])
  #if __name__ == '__main__':
  setup_db(app, os.environ['DATABASE_URL'])

  return app

  #APP = create_app()

#APP = create_app(os.environ['DATABASE_URL'], test=False)
APP = create_app()

@APP.route('/', methods=['GET'])
def check_health():
  #
  # base endpoint without authentication for check app health
  #

  return jsonify({
      'success': True,
      'healthy': True,
      'db': os.environ['DATABASE_URL']
      #'path': os.environ['DATABASE_URL']
  })

@APP.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
  #
  # Endpoint to get the list of actors, requires get:actors permission
  #

  try:
    ans = Actor.query.all()
    formatted_ans = []
    for i in ans:
      formatted_ans.append(i.format())
  except:
    abort(422)
  return jsonify({
          'actors': formatted_ans,
          'total_actors': len(formatted_ans),
          'success': True,
  })

@APP.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
  #
  # Endpoint to get the list of movies, requires get:movies permission
  #

  try:
    ans = Movie.query.all()
    formatted_ans = []
    for i in ans:
      formatted_ans.append(i.format())
  except:
    abort(422)
  return jsonify({
          'movies': formatted_ans,
          'total_movies': len(formatted_ans),
          'success': True,
  })

@APP.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(payload, actor_id):
  #
  # Endpoint for delete actor by providing the actor id, requires delete:actor permission
  #

  try:
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
  except:
    # processing error
    abort(422)
  if actor:
    #print('if')
    try:
      actor.delete()
    except:
      # processing error
      abort(422)
  else:
    # actor not found
    #print('else')
    abort(404)
  return jsonify({
            'actor_id': actor_id,
            'success': True,
  })

@APP.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(payload, movie_id):
  #
  # Endpoint to delete movie by providing the movie id, requires delete:movie permission
  #

  try:
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
  except:
    # processing error
    abort(422)
  if movie:
    #print('if')
    try:
      movie.delete()
    except:
      # processing error
      abort(422)
  else:
    # movie not found
    #print('else')
    abort(404)
  return jsonify({
            'movie_id': movie_id,
            'success': True,
  })

def check_movies_exist(movies_id):
  #
  # Called by add_actor enpoint, check the list of movies provided. Return the Movies objects if all exists, 
  # otherwise return None
  #  

  movies = Movie.query.filter(Movie.id.in_(movies_id)).all()
  #print(movies_id)
  #print(movies)
  if len(movies) == len(movies_id):
    return movies
  else:
    return None 

@APP.route('/actors', methods=['POST'])
@requires_auth('post:actor')
def add_actor(payload):
  #
  # Endpoint to add actor. name, age, gender must be provided. movies_id is optional,
  # if provided, endpoint will check the existence of them. Actor can only be added
  # if all the movies_id exist
  #

  body = request.get_json()

  if not body:
    abort(400)
  else:
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')
    movies_id = list(set(body.get('movies_id', [])))

  if name is None or age is None or gender is None:
    abort(400)
  else:
    # determine all the movies exist
    movies = check_movies_exist(movies_id)
    #print(movies)
    if movies is not None or movies_id == []:
      try:
        #print(f'{name} {age} {gender} {movies}')
        actor = Actor(name=name, age=age, gender=Gender(gender))
        actor.movies = movies
        actor.insert()
      except:
        # processing error
        abort(422)
    else:
      # input error, some or all movies do not exist
      abort(404)

  return jsonify({
        'success': True,
        'actor_id': actor.id,
  })

def check_actors_exist(actors_id):
  #
  # Call by add_movie endpoint, it checks for the existence of the list actors_id,
  # return Actor objects if all exist, otherwise return None
  #  

  actors = Actor.query.filter(Actor.id.in_(actors_id)).all()
  if len(actors) == len(actors_id):
    return actors
  else:
    return None

@APP.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def add_movie(payload):
  #
  # Endpoint to add movie. Must provide title, date_release and actors_id,
  # endpoint will check the existence of the actors_id provided, movie can be
  # added if all actors_id exist
  #

  body = request.get_json()

  if not body:
    abort(400)
  else:
    title = body.get('title')
    date_release = body.get('date_release')
    actors_id = list(set(body.get('actors_id', [])))

  if title is None or date_release is None or actors_id == []:
    abort(400)
  else:
    # determine all the actors exist
    actors = check_actors_exist(actors_id)
    if actors:
      try:
        date_release = datetime.datetime.strptime(date_release, '%Y%m%d').date()
        #print(f'{title} {date_release} {actors_id} {actors}')
        movie = Movie(title=title, date_release=date_release, actors=actors)
        movie.insert()
      except:
        # processing error
        abort(422)
    else:
      # input error, some or all actors do not exist
      abort(404)

  return jsonify({
      'success': True,
      'movie_id': movie.id,
  })

@APP.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actor')
def update_actor(payload, actor_id):
  #
  # Endpoint to update actor. name, age, gender must be provided. movies_id is optional,
  # if provided, endpoint will check the existence of them. Actor can only be updated 
  # if all the movies_id exist
  #
  body = request.get_json()

  if not body:
    abort(400)
  else:
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')
    movies_id = list(set(body.get('movies_id', [])))

  if name is None or age is None or gender is None:
    abort(400)
  else:
    # determine all the movies exist
    movies = check_movies_exist(movies_id)
    #print(movies)
    if movies is not None or movies_id == []:
      #print(f'{name} {age} {gender} {movies}')
      try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      except:
        abort(422)
      if actor:
        try:
          actor.name = name
          actor.age = age
          actor.gender = Gender(gender)
          actor.movies = movies
          actor.update()
        except:
          abort(422)
      else:
        #print('1')
        # The actor that going to be modified does not exist
        abort(404)
    else:
      #print('2')
      # Some or all movies_id do not exist
      abort(404)

  return jsonify({
        'success': True,
        'actor_id': actor.id,
  })

@APP.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movie')
def update_movie(payload, movie_id):
  #
  # Endpoint to update movie. Must provide title, date_release and actors_id,
  # endpoint will check the existence of the actors_id provided, movie can be
  # updated if all actors_id exist
  #
  body = request.get_json()

  if not body:
    abort(400)
  else:
    title = body.get('title')
    date_release = body.get('date_release')
    actors_id = list(set(body.get('actors_id', []))) 

  if title is None or date_release is None or actors_id == []:
    abort(400)
  else:
    # determine all the actors exist
    actors = check_actors_exist(actors_id)
    if actors:
      try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      except:
        abort(422)
      if movie:
        try:
          movie.title = title
          movie.date_release = datetime.datetime.strptime(date_release, '%Y%m%d').date()
          movie.actors = actors
          movie.update()
        except:
          abort(422)
      else:
        #print('1')
        # The movie going to be modified does not exist
        abort(404)
    else:
      #print('2')
      # Some or all actors_id do not exist
      abort(404)

  return jsonify({
        'success': True,
        'movie_id': movie.id,
  })

#
# Error handler to format error as JSON object
#

@APP.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "bad request"
                    }), 400

@APP.errorhandler(404)
def resouce_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@APP.errorhandler(405)
def method_not_allow(error):
    return jsonify({
		                "success": False,
		                "error": 405,
		                "message": "method not allow"
		                }), 405

@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@APP.errorhandler(500)
def internal_server_error(error):
    return jsonify({
                		"success": False,
		                "error": 500,
 		                "message": "internal server error"
 		                }), 500 

@APP.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False,
                    "error": error.status_code,
                    "message": error.error['description']
                    }), error.status_code

if __name__ == '__main__':
#    APP = create_app(os.environ['DATABASE_URL'])
    APP.run(host='0.0.0.0', port=8080, debug=True)