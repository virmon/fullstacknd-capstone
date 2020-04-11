import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_app"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.casting_director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlczZUlycFpSaVJsTG1jRGg4NVB6TCJ9.eyJpc3MiOiJodHRwczovL2Z1bGxzdGFja25kLWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTkxY2QzZjU0YzMyMjBjNjk3NDU2NWEiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU4NjYzMjY0MywiZXhwIjoxNTg2NzE5MDQzLCJhenAiOiJMTmxCRUJvVU9PSFFnRGVoNTFUVmFZbG9nb1pUOEZBRyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.T29I8gHYkhP-824K-vy-zNYFTmOxzRzjZCuGbfwIBD6aHR_ZfEXdlw2DepIGyp0ffAusskig4w1grezuFfseZcOoZYN2BtRKGoVs5tzdFGx-6id5be4HFZB9rH0C3T8xdSlUSzEBb3mJ_nzcvACEHsBewHxeMI9AsPdEJiFEMLN4LuZOdISVhgBSPTEr7a8YziAz20yCNkGAidya0zeQ2YuiB9LpRjCyI9Z9EZsH7yzhwFuEMU1ND-tsMowP8gX2Rr_Daq97__0373_wnGyzcUz_JD9Zu0bD6wosUXbpIQrmrsVBe5clHhSa1TklbsqYE4IQfidqEIigLTFzn7GOWA"
        self.executive_producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlczZUlycFpSaVJsTG1jRGg4NVB6TCJ9.eyJpc3MiOiJodHRwczovL2Z1bGxzdGFja25kLWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTkxNWExYjdhNjE1MjBjNjFlNzNkMTIiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU4NjYyNDMzMSwiZXhwIjoxNTg2NzEwNzMxLCJhenAiOiJMTmxCRUJvVU9PSFFnRGVoNTFUVmFZbG9nb1pUOEZBRyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.edJcKcljpsdAhzgxHa7awpqSvQXCK4Z5fh5-vLllSJUaPcyLeqSDbkIZd8nYB6eObmdVius_UYD55Aw4TkdWeyYVdI-p1QM7JAgfm3F2P0PO9LRwoOEg_iR5oe95wx3Ww2YdLOxNpPIk029Kse-Aw-q-QVofVYmD7Wwyg1ZiOxOn4atmpmKRhqiVQsBJ3CZKO3LkpY8BKe00dtxqk5P_d2hBetAjhcefqa4dwLb47cYbuv51LSs35o1dFhKL_1Mz_exqKU2LZXlcyVopwG7x016TBwy52ejaBQxIDf7KNK2_9qDQ97oGiliBdcfGh4nn6U1F_bmPEpAE3Gotk-LVYg"
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
        res = self.client().get(
            '/actors', 
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # GET actors fail
    def test_404_actors_not_found(self):
        res = self.client().get('/actors/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # get actors by id
    def test_get_actors_by_id(self):
        res = self.client().get(
            '/actors/1', 
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    # GET actor by id fail
    def test_404_actor_by_id_not_found(self):
        res = self.client().get('/actors/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #  post new actor
    def test_post_actor(self):
        res = self.client().post('/actors', 
            json={
                'name': 'Andy',
                'age': 25, 
                'gender':'male'}, 
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    # #  update actor
    def test_update_actor(self):
        res = self.client().patch('/actors/4', 
            json={
                'name': 'Andy',
                'age': 30, 
                'gender':'male'}, 
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #  delete actor
    def test_delete_actor(self):
        res = self.client().delete('/actors/3', 
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''
    Test Movie

    '''
    # get movie
    def test_get_movie(self):
        res = self.client().get(
            '/movies', 
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # get movie by id
    def test_get_movie_by_id(self):
        res = self.client().get(
            '/movies/1', 
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
    
    #  post new movie
    def test_post_movie(self):
        res = self.client().post('/movies', 
            json={
                'title': 'Computer Geeks',
                'release_date': '01-01-2022'}, 
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    #  update movie
    def test_update_movie(self):
        res = self.client().patch('/movies/3', 
            json={
                'title': 'Space Ranger',
                'release_date':'01-01-2021'}, 
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #  delete movie
    def test_delete_movie(self):
        res = self.client().delete('/movies/2', 
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()