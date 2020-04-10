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
    
    if data is None:
      abort(404)
    else:
      actors = [actor.format() for actor in data]
      
      return jsonify({
        'success': True,
        'actors': actors
      })

  '''
  GET
    - retrieve one actor by id
    
  '''
  @app.route('/actors/<int:id>', methods=['GET'])
  def get_actor_by_id(id):
    data = Actor.query.filter(Actor.id == id).one_or_none()
    
    if data is None:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'actor': data.format()
      })

  '''
  POST
    - insert new actor
    
  '''
  @app.route('/actors', methods=['POST'])
  def add_actor():
    data = request.get_json()
    
    name = data.get('name')
    genres = data.get('genres')
    role = data.get('role')

    if 'name' in data and 'genres' in data and 'role in data':
      if name != '' and genres != '' and role != '':
        actor = Actor(name=name, genres=genres, role=role)
        actor.insert()

        return jsonify({
          'success': True,
          'actor': actor.format()
        })
    else:
      abort(401)

  '''
  PATCH
    - update actor details
    
  '''
  @app.route('/actors/<int:id>', methods=['PATCH'])
  def update_actor(id):
    data = request.get_json()

    actor = Actor.query.filter(Actor.id == id).one_or_none()

    if actor is None:
      abort(404)
    else:
      actor.name = data.get('name')
      actor.genres = data.get('genres')
      actor.role = data.get('role')

      actor.update()

      return jsonify({
        'success': True,
        'updated': id
      })

  '''
  DELETE
    - delete actor
    
  '''
  @app.route('/actors/<int:id>', methods=['DELETE'])
  def delete_actor(id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()

    if actor is None:
      abort(404)
    else:
      actor.delete()

    return jsonify({
      'success': True,
      'deleted': id
    })

  return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)