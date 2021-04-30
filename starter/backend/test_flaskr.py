import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE, paginate_questions
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format(
            'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.question1 = {'question': 'Art Question?',
                          'answer': 'Art Answer!',
                          'category': 'Art',
                          'difficulty': 2}

        self.new_question = {'id': 10,
                             'question': 'Art Question?',
                             'answer': 'Art Answer!',
                             'category': 2,
                             'difficulty': 2}

        self.category = '2'
        self.bad_category = '7'
        self.total_questions = Question.query.count()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # --------------------------------------------------------------
    # ROUTE: '/categories'  METHOD: get
    # --------------------------------------------------------------

    def test_get_gategories(self):
        ''' retrives all available categories '''
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

    def test_400_bad_request_in_category_getting(self):
        ''' Tests when the user sends a json with the request'''
        res = self.client().get('/categories', json={'category': 'Art'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

    # --------------------------------------------------------------
    # ROUTE: '/categories'  METHOD: post  PURPOSE: play game
    # --------------------------------------------------------------

    def test_200_play(self):
        res = self.client().post('/categories',
                                 json={'quiz_category': {'id': 1},
                                       'previous_questions': [1, 11]})  # optional

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_unable_to_find_question_to_play(self):
        ''' request sends a category that does not exist '''
        res = self.client().post('/categories',
                                 json={'quiz_category': {'id': '10'},
                                       'previous_questions_ids': ['1', '11']})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_400_post_request_with_not_data(self):
        ''' User sends a request to play with no json data '''
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

    # --------------------------------------------------------------
    # ROUTE: '/questions'  METHOD: get
    # --------------------------------------------------------------

    def test_get_questions_with_pagination(self):
        res = self.client().get('questions?category_id={}&page={}'
                                .format(self.category, '1'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], self.total_questions)
        self.assertEqual(data['current_category'], '2')
        self.assertTrue(data['categories'])

    def test_400_questions_request_of_category_that_doesnot_exist(self):
        res = self.client().get('/questions?category_id={}'
                                .format(self.bad_category))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

    # --------------------------------------------------------------
    # ROUTE:'/questions'  METHOD: post  PURPOSE: search/new_question
    # --------------------------------------------------------------

    def test_200_search_questions(self):
        ''' tests a successful request, with or without matching questions '''

        res = self.client().post('/questions', json={'searchTerm': 'Art'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_200_post_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        test_insertion = Question.query.filter(
            Question.id == data['new_question_id']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(test_insertion)

    def test_422_unprossable_request_to_post_a_question(self):
        ''' e.g: difficulty level greater than allowed range '''
        res = self.client().post('/questions',
                                 json={'question': 'what is mining?',
                                       'answer': 'a blockchain operation',
                                       'category': 1,
                                       'difficulty': 8
                                       })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Not processable')

    def test_400_bad_request_posting_a_question(self):
        '''e.g: request is missing an argument '''
        res = self.client().post('/questions',
                                 json={'question': 'what is mining?',
                                       'answer': 'a blockchain operation',
                                       'category': 1,
                                       })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

    # --------------------------------------------------------------
    # ROUTE:'/questions/<int:question_id>'   METHOD: delete
    # --------------------------------------------------------------

    def test_delete_question(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)
        question = Question.query.filter_by(id=10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_id'], 10)
        self.assertEqual(data['total_questions'], self.total_questions - 1)
        self.assertEqual(question, None)

    def test_404_question_to_be_deleted_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    # --------------------------------------------------------------
    # ROUTE:'/categories/<int:category_id>/questions' METHOD: get
    # --------------------------------------------------------------

    def test_200_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_404_query_question_on_unexistant(self):
        ''' request questions in a category that does not exist '''

        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')


if __name__ == "__main__":
    unittest.main()
