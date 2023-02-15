import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from application.app import create_app
from application.database.models import setup_db, Movie, Actor
from dotenv import load_dotenv
load_dotenv()


class FinalProjectTestCase(unittest.TestCase):
    """This class represents the final project test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_movie = {
            'title': 'Avatar',
            'release_date': '2023-01-01'
        }

        self.new_invalid_movie = {
            'title': 'Avatar',
            'release_date': 'This is string'
        }

        self.new_actor = {
            'name': 'Ryan Gosling',
            'age': 42,
            'gender': 'Male'
        }

        self.new_invalid_actor = {
            'name': 'Ryan Gosling',
            'age': 'This is string',
            'gender': 'Male'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_movies(self):
        headers = {"authorization": "{}".format(os.environ.get('ASSISTANT_TOKEN'))}
        response = self.client().get('/movies', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors(self):
        headers = {"authorization": "{}".format(os.environ.get('DIRECTOR_TOKEN'))}
        response = self.client().get('/actors', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_delete_movie(self):
        headers = {"authorization": "{}".format(os.environ.get('PRODUCER_TOKEN'))}
        response = self.client().delete('/movies/1', headers=headers)
        data = json.loads(response.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], '1')
        self.assertEqual(movie, None)

    def test_delete_movie_not_auth(self):
        headers = {"authorization": "{}".format(os.environ.get('DIRECTOR_TOKEN'))}
        response = self.client().delete('/movies/1', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'authorization error')

    def test_delete_actor(self):
        headers = {"authorization": "{}".format(os.environ.get('PRODUCER_TOKEN'))}
        response = self.client().delete('/actors/1', headers=headers)
        data = json.loads(response.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], '1')
        self.assertEqual(actor, None)

    def test_delete_actor_not_auth(self):
        headers = {"authorization": "{}".format(os.environ.get('ASSISTANT_TOKEN'))}
        response = self.client().delete('/actors/1', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'authorization error')

    def test_404_actor_not_exist(self):
        headers = {"authorization": "{}".format(os.environ.get('PRODUCER_TOKEN'))}
        response = self.client().delete('/actors/1000000', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_404_movie_not_exist(self):
        headers = {"authorization": "{}".format(os.environ.get('DIRECTOR_TOKEN'))}
        response = self.client().delete('/movies/1000000', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_create_new_movie(self):
        headers = {"authorization": "{}".format(os.environ.get('PRODUCER_TOKEN'))}
        response = self.client().post('/movies', json=self.new_movie, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_create_movie_not_auth(self):
        headers = {"authorization": "{}".format(os.environ.get('DIRECTOR_TOKEN'))}
        response = self.client().post('/movies', json=self.new_movie, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'authorization error')

    def test_modify_movie(self):
        headers = {"authorization": "{}".format(os.environ.get('DIRECTOR_TOKEN'))}
        response = self.client().patch('/movies/1', json=self.new_movie, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["modified"])

    def test_invalid_new_movie(self):
        headers = {"authorization": "{}".format(os.environ.get('PRODUCER_TOKEN'))}
        response = self.client().post('/movies', json=self.new_invalid_movie, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_modify_not_exist_movie(self):
        headers = {"authorization": "{}".format(os.environ.get('PRODUCER_TOKEN'))}
        response = self.client().patch('/movies/100000', json=self.new_movie, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_create_new_actor(self):
        headers = {"authorization": "{}".format(os.environ.get('PRODUCER_TOKEN'))}
        response = self.client().post('/actors', json=self.new_actor, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_modify_actor(self):
        headers = {"authorization": "{}".format(os.environ.get('PRODUCER_TOKEN'))}
        response = self.client().patch('/actors/1', json=self.new_actor, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["modified"])

    def test_invalid_new_actor(self):
        headers = {"authorization": "{}".format(os.environ.get('PRODUCER_TOKEN'))}
        response = self.client().post('/actors', json=self.new_invalid_actor, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_modify_not_exist_actor(self):
        headers = {"authorization": "{}".format(os.environ.get('PRODUCER_TOKEN'))}
        response = self.client().patch('/actors/100000', json=self.new_actor, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()