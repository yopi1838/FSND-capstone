import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor

# token from environment
ASSISTANT_TOKEN = str('Bearer '+ os.environ['ASSISTANT_TOKEN'])
CD_TOKEN = str('Bearer ' + os.environ['DIRECTOR_TOKEN'])
EP_TOKEN = str('Bearer ' + os.environ['EP_TOKEN'])

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = "postgres://{}@{}/{}".format('yopiprabowooktiovan','localhost:5432', self.database_name)

        #Ideas from https://github.com/Onnys/Capstone/blob/master/test_app.py
        #Extract the token for header check
        self.casting_assistant = {'Content-Type': 'application/json',
                                  'Authorization': ASSISTANT_TOKEN}
        self.casting_director = {'Content-Type': 'application/json',
                                  'Authorization': CD_TOKEN}
        self.executive_producer = {'Content-Type': 'application/json',
                                  'Authorization': EP_TOKEN}
        setup_db(self.app, self.database_path)
        
        #binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            #Create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    Write test method for each endpoints. Consider both successful operations and expected errors
    """
    #PUBLIC ERROR TEST
    #public test. Test 401 error for each endpoints
    def test_401_error_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #Test 401 error for get actors endpoint without permission
    def test_401_error_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #Test 401 error to post actors endpoint without permission
    def test_401_error_post_actors(self):
        new_actor_name = 'Robert De Niro'
        new_actor_age = 77
        new_actor_gender = 'Male'
        res = self.client().post('/actors', json={"name": new_actor_name, "age": new_actor_age, "gender":new_actor_gender})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #Test 401 error to post movies endpoint without permission
    def test_401_error_post_movies(self):
        new_movie_title = 'Shawshank Redemption'
        new_movie_release_date = '2014-03-29 21:37:24'
        res = self.client().post('/movies', json={"title": new_movie_title, "release_date": new_movie_release_date})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #Test 401 error to patch movies endpoint without permission
    def test_401_error_patch_movies(self):
        update_movies_title = 'Back to The Future'
        update_movies_release_date = '1985-12-7 21:37:24'
        res = self.client().patch('movies/1',
                json={'title': update_movies_title, 'release_date': update_movies_release_date})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    
    #Test 401 error to patch actors endpoint without permission
    def test_401_error_patch_actors(self):
        update_actors_name= 'Jessica Alba'
        update_actors_age = 40
        update_actors_gender = 'Female'
        res = self.client().patch('/actors/1',
                json={'name': update_actors_name, 'age': update_actors_age, 'gender': update_actors_gender})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #Test for CASTING ASSISTANT's role (GET, POST, PATCH, DELETE)
    #Test GET actors endpoint
    def test_return_actors_CA(self):
        res = self.client().get('/actors', headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    #Test GET movies endpoint with CA role
    def test_return_movies_CA(self):
        res = self.client().get('/movies', headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Error 403 POST actors with CA role
    def test_error_403_post_actors_CA(self):
        new_actor_name = 'Jason Bateman'
        new_actor_age = 42
        new_actor_gender = 'Male'
        res = self.client().post('/actors', json={"name": new_actor_name, "age": new_actor_age, "gender":new_actor_gender}, headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    #Error 403 POST movies with CA role
    def test_error_403_post_movies_CA(self):
        new_movie_title = 'Shawshank Redemption'
        new_movie_release_date = '2014-03-29 21:37:24'
        res = self.client().post('/movies', 
                json={"title": new_movie_title, "release_date": new_movie_release_date}, 
                headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    #Error 403 PATCH actors with CA role
    def test_error_403_patch_actors_CA(self):
        update_actors_name= 'Jessica Alba'
        update_actors_age = 40
        update_actors_gender = 'Female'
        res = self.client().patch('/actors/2',
                json={'name': update_actors_name, 'age': update_actors_age, 'gender': update_actors_gender}, 
                headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    #Error 403 PATCH movies with CA role
    def test_error_403_patch_movies_CA(self):
        update_movies_title = 'Harry Potter and The Prisoner of Azkaban'
        update_movies_release_date = '2004-06-26 10:45:24'
        res = self.client().patch('movies/6',
                json={'title': update_movies_title, 'release_date': update_movies_release_date},
                headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    #Error 403 DELETE actors with CA role
    def test_403_delete_actors_CA(self):
        res = self.client().delete('/actors/3', headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    #Error 403 DELETE movies with CA role
    def test_403_delete_movies_CA(self):
        res = self.client().delete('/movies/2', headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    
    #Test for CASTING DIRECTOR's role (GET, POST, PATCH, DELETE)
    #Test GET actors endpoint using CD's role
    def test_return_actors_CD(self):
        res = self.client().get('/actors', headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    #Test GET movies endpoint using CD's role
    def test_return_movies_CD(self):
        res = self.client().get('/movies', headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test POST actors endpoint using CD's role
    def test_post_actors(self):
        new_actor_name = 'Robert De Niro'
        new_actor_age = 77
        new_actor_gender = 'Male'
        res = self.client().post('/actors', json={"name": new_actor_name, "age": new_actor_age, "gender":new_actor_gender}, headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test POST movies error endpoint for Casting Director's roles
    def test_403_error_post_movies_CD(self):
        new_movie_title = 'Shawshank Redemption'
        new_movie_release_date = '2014-03-29 21:37:24'
        res = self.client().post('/movies', 
                json={"title": new_movie_title, "release_date": new_movie_release_date}, 
                headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    #Test PATCH actors endpoint using Casting Director's roles
    def test_patch_actors_CD(self):
        update_actors_name= 'Jessica Alba'
        update_actors_age = 40
        update_actors_gender = 'Female'
        res = self.client().patch('/actors/2',
                json={'name': update_actors_name, 'age': update_actors_age, 'gender': update_actors_gender}, 
                headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test PATCH movies endpoint using Casting Director's roles
    def test_patch_movies_CD(self):
        update_movies_title = 'Back to The Future'
        update_movies_release_date = '1985-12-7 21:37:24'
        res = self.client().patch('movies/3',
                json={'title': update_movies_title, 'release_date': update_movies_release_date},
                headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    #Test DELETE actors from database using Casting Director's role
    def test_delete_actors_CD(self):
        res = self.client().delete('/actors/1', headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    #Test DELETE movies from database using Casting Director's role
    def test_error_403_delete_movies_CD(self):
        res = self.client().delete('/movies/3', headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    #Test for EXECUTIVE PRODUCER's role (GET, POST, PATCH, DELETE)
    #Test GET actors using EP's role
    def test_return_actors_EP(self):
        res = self.client().get('/actors', headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    #Test GET movies using EP's role
    def test_return_movies_EP(self):
        res = self.client().get('/movies', headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test POST actors using EP's role
    def test_post_actors_EP(self):
        new_actor_name = 'Gerald Butler'
        new_actor_age = 40
        new_actor_gender = 'Male'
        res = self.client().post('/actors', json={"name": new_actor_name, "age": new_actor_age, "gender":new_actor_gender}, headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test POST movies using EP's role
    def test_post_movies_EP(self):
        new_movie_title = 'Get Out'
        new_movie_release_date = '2017-02-24 18:37:24'
        res = self.client().post('/movies', 
                json={"title": new_movie_title, "release_date": new_movie_release_date}, 
                headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test PATCH movies using EP's role
    def test_patch_movies_EP(self):
        update_movies_title = 'Harry Potter and The Prisoner of Azkaban'
        update_movies_release_date = '2004-06-26 10:45:24'
        res = self.client().patch('movies/6',
                json={'title': update_movies_title, 'release_date': update_movies_release_date},
                headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test PATCH actors using EP's role
    def test_patch_actors_EP(self):
        update_actors_name = 'James McAvoy'
        update_actors_age = '35'
        update_actors_gender = 'Male'
        res = self.client().patch('/actors/2',
                json={'name': update_actors_name, 'age': update_actors_age, 'gender': update_actors_gender}, 
                headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test DELETE actors endpoint using EP's role
    def test_delete_actors_EP(self):
        res = self.client().delete('/actors/5', headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    #Test DELETE movies from database using EP's role
    def test_delete_movies_EP(self):
        res = self.client().delete('/movies/4', headers=self.executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

#Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()