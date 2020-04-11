
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

database_name = "casting"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
Cast

'''
class Cast(db.Model):
    __tablename__ = 'casts'

    actor_id = Column(Integer, db.ForeignKey('actors.id'), primary_key=True)
    movie_id = Column(Integer, db.ForeignKey('movies.id'), primary_key=True)
    movie = db.relationship("Movie", back_populates="actor")
    actor = db.relationship("Actor", back_populates="movie")

    def __repr__(self):
        return f'<Cast {self.actor.name} {self.movie.title}>'


'''
Actor

'''
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    movie = db.relationship('Cast', back_populates='actor')

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return f'<Actor {self.name}>'

'''
Movie

'''
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(db.Date)
    actor = db.relationship('Cast', back_populates='movie')

    def __init__(self, title, release_date):
        self.title = title,
        self.release_date = release_date
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
    
    def __repr__(self):
        return f'<Movie {self.title}>'