import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from models import Cast, Actor, Movie, setup_db
from flask_cors import CORS
import json

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def index():
    return "Casting Agency API"

  '''
  GET
    - retrieve all actors

  '''
  @app.route('/actors', methods=['GET'])
  def get_actors():
    data = Actor.query.all()
    
    if len(data) == 0:
      not_found(404)
    else:
      actors = [actor.format() for actor in data]
      
      return jsonify({
        'success': True,
        'actors': actors
      }), 200

  '''
  GET
    - retrieve one actor by id
    
  '''
  @app.route('/actors/<int:id>', methods=['GET'])
  def get_actor_by_id(id):
    data = Actor.query.filter(Actor.id == id).first()
    
    if not data:
      not_found(404)
    else:
      return jsonify({
        'success': True,
        'actor': data.format()
      }), 200

  '''
  POST
    - insert new actor
    
  '''
  @app.route('/actors', methods=['POST'])
  def add_actor():
    data = request.get_json()
    
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')

    if 'name' in data and 'age' in data and 'gender' in data:
      if name != '' and age != '' and gender != '':
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
          'success': True,
          'actor': actor.format()
        }), 201
    else:
      bad_request(400)

  '''
  PATCH
    - update actor details
    
  '''
  @app.route('/actors/<int:id>', methods=['PATCH'])
  def update_actor(id):
    data = request.get_json()

    actor = Actor.query.filter(Actor.id == id).first()

    if not actor:
      abort(404)
    else:
      actor.name = data.get('name')
      actor.age = data.get('age')
      actor.gender = data.get('gender')

      actor.update()

      return jsonify({
        'success': True
      }), 200

  '''
  DELETE
    - delete actor
    
  '''
  @app.route('/actors/<int:id>', methods=['DELETE'])
  def delete_actor(id):
    actor = Actor.query.filter(Actor.id == id).first()

    if not actor:
      not_found(404)
    else:
      actor.delete()

    return jsonify({
      'success': True,
      'deleted': id
    }), 200

  '''
  GET
    - retrieve all movies

  '''
  @app.route('/movies', methods=['GET'])
  def get_movies():
    data = Movie.query.all()
    
    if len(data) == 0:
      not_found(404)
    else:
      movies = [movie.format() for movie in data]
      
      return jsonify({
        'success': True,
        'movies': movies
      }), 200

  '''
  GET
    - retrieve one movie by id
    
  '''
  @app.route('/movies/<int:id>', methods=['GET'])
  def get_movie_by_id(id):
    data = Movie.query.filter(Movie.id == id).first()
    
    if not data:
      not_found(404)
    else:
      return jsonify({
        'success': True,
        'movie': data.format()
      }), 200

  '''
  POST
    - insert new movie
    
  '''
  @app.route('/movies', methods=['POST'])
  def add_movie():
    data = request.get_json()
    
    title = data.get('title')
    release_date = data.get('release_date')

    if 'title' in data and 'release_date' in data:
      if title != '' and release_date != '':
        movie = Movie(title=title, release_date=release_date)
        movie.insert()

        return jsonify({
          'success': True,
          'movie': movie.format()
        }), 201
    else:
      bad_request(400)

  '''
  PATCH
    - update movie details
    
  '''
  @app.route('/movies/<int:id>', methods=['PATCH'])
  def update_movie(id):
    data = request.get_json()

    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if movie is None:
      not_found(404)
    else:
      movie.title = data.get('title')
      movie.release_date = data.get('release_date')

      movie.update()

      return jsonify({
        'success': True
      }), 200

  '''
  DELETE
    - delete movie
    
  '''
  @app.route('/movies/<int:id>', methods=['DELETE'])
  def delete_movie(id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if movie is None:
      not_found(404)
    else:
      movie.delete()

    return jsonify({
      'success': True
    }), 200

  
  # error handlers
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
    }), 500

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)