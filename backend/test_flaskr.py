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
        # self.database_path = "postgres://{}/{}".format(
        #     "postgres", "postgres", 'localhost:5432', self.database_name)

        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "postgres", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

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

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_non_existing_category(self):
        res = self.client().get('/categories/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):

        res = self.client().delete('/questions/26')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(data['deleted'], str(24))
        self.assertEqual(question, None)



    def test_add_question(self):
        new_question = {

            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 1,
            'category': 1
        }
        total_questions_before = len(Question.query.all())
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions_after, total_questions_before + 1)

    def test_search_questions(self):
        new_search = {'searchTerm': 'dfdfdfdfdf'}
        res = self.client().post('/questions/search', json=new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_play_quiz(self):
        new_quiz_round = {'previous_questions': [],
                          'quiz_category': {'type': 'Entertainment', 'id': 5}}

        res = self.client().post('/quizzes', json=new_quiz_round)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_play_quiz(self):
        new_quiz_round = {'previous_questions': []}
        res = self.client().post('/quizzes', json=new_quiz_round)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()