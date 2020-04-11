import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, Cast


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "app_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    Test Actor
    '''
    # get actors
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_404_actors_not_found(self):
        res = self.client().get('/actors/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # get actor by id
    def test_get_actor_by_id(self):
        res = self.client().get('/actors/4')
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_actor_does_not_exist(self):
        res = self.client().get('/actors/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #  post new actor
    def test_post_actor(self):
        res = self.client().post('/actors', json={'name': 'Andy', 'age': 25, 'gender':'male'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_400_create_question_fail(self):
        res = self.client().post('/actors', json={'name': '', 'age': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'internal server error')

    #  update actor
    def test_update_actor(self):
        res = self.client().patch('/actors/4', json={'name': 'Andi', 'age': 27, 'gender':'female'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #  delete actor
    def test_delete_actor(self):
        res = self.client().delete('/actors/21')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    '''
    Test Movie
    '''
    # get movies
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_404_movies_not_found(self):
        res = self.client().get('/movies/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # get movie by id
    def test_get_movie_by_id(self):
        res = self.client().get('/movies/17')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_movie_does_not_exist(self):
        res = self.client().get('/movies/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #  post new movie
    def test_post_movie(self):
        res = self.client().post('/movies', json={'title': 'The Great Movie', 'release_date': '01-01-2020'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_400_post_movie_fail(self):
        res = self.client().post('/actors', json={'title': 'The Great Movie'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'internal server error')

    #  update movie
    def test_update_movie(self):
        res = self.client().patch('/actors/4', json={'title': 'The Great Movie', 'release_date': '01-01-2025'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #  delete movie
    def test_delete_movie(self):
        res = self.client().delete('/movies/18')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_movie_does_not_exist(self):
        res = self.client().get('/movies/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


if __name__ == "__main__":
    unittest.main()