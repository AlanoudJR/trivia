import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question= {
            'question': 'This is the question',
            'answer': 'This is the answer',
            'category': 3,
            'difficulty':2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #Created a test case for 200 status code and for 422/404 for all endpoints on the __init__.py
    # Each TC must start with test_/// then write the description of each one.
    # get the response from each endpoing and store it
    #Assert as suitable (assert equal/greaterthan/ True/False) to make sure that it passes the TC
    #Assert and take the values from the data that has the JSON values (based on what is specified in your endpoint)
    #Those are generally the main steps in creating a test case but it would differ slightly based on the type (post/get/delete)


    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        
    #Testing getting categories 200
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['success'])
        self.assertGreater(data['total_categories'],0)

    #To Get the questions 200 Status code
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertGreater(data['total_questions'],0)
        self.assertIsNone(data['current_category'])

    #To Get an Error on getting questions 404 Status code
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['Message'], 'not found')

    #To delete the questions 200 Status code (deleting an exsiting question)    
    def test_delete_question(self):
        res = self.client().delete('/questions/44')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 44).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 25)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)
        

    #To Get an Error on deleting a questions 422 Status code
    def test_422_delete_if_question_does_not_exist(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['Message'], 'unprocessable')
    
    #Create a new question 200 
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['Questions']))
        
    #Error on creating a questions Method not allowed
    def test_405_if_question_creation_is_not_allowed(self):
        res = self.client().post('/questions/32', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['Message'], 'method not allowed')
   
    #Search for an exisiting question term 200
    def test_search_question(self):        

        res = self.client().post('/search', json =  {"searchTerm": "action"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertGreater(data['total_questions'],0)

    #Search for non exisiting question term 404
    def test_404_if_no_search_results(self):        
        res = self.client().post('/search', json =  {"searchTerm": "xyz" })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['Message'], 'not found')

    #Test the quizzes 200 
    def test_get_quiz(self):
        #Create a data variable with values to pass to quizzes endpoint 
        data = {"previous_questions": [10, 13],
                "quiz_category": 
                {"type": "Science", "id": "1"}
        } 

        res = self.client().post('/quizzes', json=data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

   #Test 422 unporccassable when json body is missing 
    def test_422_get_quiz(self):
        #Create a data variable with values to pass to quizzes endpoint 
        data = {}
        
        res = self.client().post('/quizzes', json=data)
        
        #Here we used res.get_json() instead of loading the json response in data variable as done in the previous test cases
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()["Message"], "unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()