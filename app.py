import os
import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Gender, Movie

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app, os.getenv('SQLALCHEMY_DATABASE_URI'))

  return app

APP = create_app()

# ADD PAGINATION??

@APP.route('/actors', methods=['GET'])
def get_actors():

  try:
    ans = Actor.query.all()
    formatted_ans = []
    for i in ans:
      formatted_ans.append(i.format())
  except:
    abort(422)
  return jsonify({
          'actors': formatted_ans,      # Add page
          'total_actors': len(formatted_ans),
          'success': True,
  })

@APP.route('/movies', methods=['GET'])
def get_movies():

  try:
    ans = Movie.query.all()
    formatted_ans = []
    for i in ans:
      formatted_ans.append(i.format())
  except:
    abort(422)
  return jsonify({
          'movies': formatted_ans,    # Add page
          'total_movies': len(formatted_ans),
          'success': True,
  })

@APP.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
  
  try:
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
  except:
    # processing error
    abort(422)
  
  if actor:
    print('if')
    try:
      actor.delete()
    except:
      # processing error
      abort(422)
  else:
    # actor not found
    print('else')
    abort(404)

  return jsonify({
            'actor_id': actor_id,
            'success': True,
  })
    
@APP.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
  
  try:
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
  except:
    # processing error
    abort(422)
  
  if movie:
    print('if')
    try:
      movie.delete()
    except:
      # processing error
      abort(422)
  else:
    # movie not found
    print('else')
    abort(404)

  return jsonify({
            'movie_id': movie_id,
            'success': True,
  })

def check_movies_exist(movies_id):

  movies = Movie.query.filter(Movie.id.in_(movies_id)).all()
  #print(movies_id)
  #print(movies)
  if len(movies) == len(movies_id):
    return movies
  else:
    return None 

@APP.route('/actors', methods=['POST'])
def add_actor():
  body = request.get_json()

  if not body:
    abort(400)
  else:
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')
    movies_id = list(set(body.get('movies_id', [])))

  if name is None or age is None:
    abort(400)
  else:
    # determine all the movies exist
    movies = check_movies_exist(movies_id)
    #print(movies)
    if movies:
      try:
        print(f'{name} {age} {gender} {movies}')
        actor = Actor(name=name, age=age, gender=Gender(gender))
        actor.movies = movies
        actor.insert()
      except:
        abort(422)
    else:
      abort(404)

  return jsonify({
        'success': True,
        'actor_id': actor.id,
  })

def check_actors_exist(actors_id):

  actors = Actor.query.filter(Actor.id.in_(actors_id)).all()
  if len(actors) == len(actors_id):
    return actors
  else:
    return None

@APP.route('/movies', methods=['POST'])
def add_movie():
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
        abort(422)
    else:
      abort(404)

  return jsonify({
      'success': True,
      'movie_id': movie.id,
  })

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

@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)