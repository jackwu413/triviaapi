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

        #Sample Trivia Question to be used for testing  
        self.sample_question = {
            'question': 'In what year did Nixon resign?',
            'answer': '1974', 
            'difficulty': 3, 
            'category': 2
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

    def test_get_paginated_questions(self): 
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_delete_question(self): 

        question = Question(
            question = self.sample_question['question'], 
            answer = self.sample_question['answer'], 
            difficulty = self.sample_question['difficulty'], 
            category = self.sample_question['category']
        )

        question.insert()

        q_id = question.id 

        questions_before = Question.query.all() 
        response = self.client().delete('questions/{}'.format(q_id))
        data = json.loads(response.data)
        questions_after = Question.query.all() 

        #Deleted question 
        deleted_question = Question.query.get(q_id)

        self.assertEqual(deleted_question, None)
        self.assertTrue(len(questions_before) - len(questions_after) == 1)
        self.assertEqual(data['response.status_code'], 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], q_id) 
    
    def test_post_new_question(self): 
        questions_before = Question.query.all() 

        #response data sent from endpoint 
        response = self.client().post('/questions', json=self.sample_question)
        data = json.loads(response.data)

        questions_after = Question.query.all()

        question = Question.query.filter_by(id=data['created']).one_or_none() 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(questions_after) - len(questions_before) == 1) 
        self.assertIsNotNone(question)
    def test_422_question_creation_fails(self): 
        questions_before = Question.query.all()
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        questions_after = Question.query.all()

        self.assertEqual(response.status_code, 422) 
        self.assertEqual(data['success'], False)
        self.assertTrue(len(questions_before) == len(questions_after))

    def test_search_questions(self): 
        response = self.client().post('/questions/search', json={'searchTerm': 'Tom Hanks'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
    def test_404_search_questions_fails(self): 
        response = self.client().post('/questions/search', json={'searchTerm': 'jdfksafjdksl'})
        data = json.loads(response.data) 

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_category(self): 
        response = self.client().get('/categories/2/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 'Art')
    def test_400_get_questions_by_category_fails(self): 
        response = self.client().get('/categories/20/questions')
        data = json.loads(response.data) 

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()