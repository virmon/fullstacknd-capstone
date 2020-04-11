import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from models import Actor, Movie, setup_db
from flask_cors import CORS
import json
from auth import AuthError, requires_auth

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # @app.route('/')
  # def index():
  #   return jsonify({
  #     'login': "https://fullstacknd-capstone.auth0.com/authorize?audience=movie&response_type=token&client_id=LNlBEBoUOOHQgDeh51TVaYlogoZT8FAG&redirect_uri=http://localhost:5000",
  #     'logout': "https://fullstacknd-capstone.auth0.com/v2/logout"
  #   })

  '''
  Actor Endpoint
  GET
    - retrieve all actors

  '''
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(jwt):
    result = Actor.query.all()

    data = [actor.format() for actor in result]
    
    if not data:
      not_found(404)
      
    return jsonify({
      'success': True,
      'actors': data
    }), 200

  '''
  GET
    - retrieve one actor by id
    
  '''
  @app.route('/actors/<int:id>', methods=['GET'])
  @requires_auth('get:actors')
  def get_actor_by_id(jwt, id):
    result = Actor.query.get(id)
    
    if not result:
      not_found(404)
    else:
      return jsonify({
        'success': True,
        'actor': result.format()
      }), 200

  '''
  POST
    - insert new actor
    
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actor')
  def add_actor(jwt):
    data = request.get_json()

    name = data.get('name', '')
    age = data.get('age', '')
    gender = data.get('gender', '')

    new_actor = Actor(name=name, age=age, gender=gender)
    try:
        new_actor.insert()
        return jsonify({
            'success': True,
            'actor': new_actor.format()
        }), 201
    except():
        abort(500)

  '''
  PATCH
    - update actor details
    
  '''
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def update_actor(jwt, id):
    data = request.get_json()

    actor = Actor.query.filter(Actor.id == id).first()

    if not actor:
      not_found(404)
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
  @requires_auth('delete:actor')
  def delete_actor(jwt, id):
    actor = Actor.query.get(id)

    if actor is None:
      not_found(404)
    else:
      actor.delete()

      return jsonify({
        'success': True
      }), 200

  '''
  Movie Endpoint
  GET
    - retrieve all actors

  '''
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(jwt):
    result = Movie.query.all()

    data = [movie.format() for movie in result]
    
    if not data:
      not_found(404)
      
    return jsonify({
      'success': True,
      'movies': data
    }), 200

  '''
  GET
    - retrieve one movie by id
    
  '''
  @app.route('/movies/<int:id>', methods=['GET'])
  @requires_auth('get:movies')
  def get_movie_by_id(jwt, id):
    result = Movie.query.get(id)
    
    if not result:
      not_found(404)
    else:
      return jsonify({
        'success': True,
        'movie': result.format()
      }), 200

  '''
  POST
    - insert new movie
    
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movie')
  def add_movie(jwt):
    data = request.get_json()

    title = data.get('title', '')
    release_date = data.get('release_date', '')

    new_movie = Movie(title=title, release_date=release_date)
    try:
        new_movie.insert()
        return jsonify({
            'success': True,
            'movie': new_movie.format()
        }), 201
    except():
        abort(500)

  '''
  PATCH
    - update movie details
    
  '''
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def update_movie(jwt, id):
    data = request.get_json()

    movie = Movie.query.filter(Movie.id == id).first()

    if not movie:
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
  @requires_auth('delete:movie')
  def delete_movie(jwt, id):
    movie = Movie.query.get(id)

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