import os
import unittest
import json
#from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Actor, Movie, Gender

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(os.environ['TEST_DATABASE_URL'])
        self.client = self.app.test_client

        a1 = Actor(name='PPP', age=23, gender=Gender('M'))
        a1.insert()
        '''
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('pl704206:phm123@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        c1 = Category(type='science')
        c2 = Category(type='art')
        c3 = Category(type='geography')
        c4 = Category(type='history')
        c5 = Category(type='entertainment')
        c6 = Category(type='sport')
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.add(c4)
        db.session.add(c5)
        db.session.add(c6)
        db.session.commit()

        q = Question(question='where is the 2020 coronavirus outbreak started?', answer='wuhan', category=1, difficulty=1)
        q.insert()

    '''
    def tearDown(self):
        """Executed after reach test"""
        '''
        questions = Question.query.all()
        [q.delete() for q in questions]
        pass

        categories = Category.query.all()
        [db.session.delete(c) for c in categories]
        db.session.commit()
        '''
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


    def test_base(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    '''
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_method_not_allow_get_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)
     
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_get_questions(self):
        res = self.client().get('/questions?category=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['current_category'], 1)
        self.assertEqual(data['success'], True)

    def test_get_questions_with_searchTerm(self):
        res = self.client().get('/questions?searchTerm=coronavirus')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['current_category'], 0)
        
    def test_404_get_questions_with_nonexist_category(self):
        res = self.client().get('/questions?category=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
   
    def test_delete_question(self):
        q_id = Question.query.all()[0].id
        res = self.client().delete(f'/questions/{q_id}')
        data = json.loads(res.data)
        q = Question.query.filter(Question.id == f'{q_id}').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(q, None)

    def test_422_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_add_question(self):
        res = self.client().post('/questions?searchTerm=null', json={'question': 'are dogs mammals?', 'answer': 'yes', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)
        q = Question.query.filter(Question.question == 'are dogs mammals?').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(q.question, 'are dogs mammals?')

    def test_400_add_question(self):
        res = self.client().post('/questions?searchTerm=null', json={'question': 'are dogs mammals?', 'answer': '', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'virus'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)

    def test_400_no_searchTerm_search_questions(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_404_no_result_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'nonexist'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_nonexist_category_get_questions_by_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_play_quizzes(self):
        res = self.client().post('/quizzes', json={'previous_questions': [1, 2], 'quiz_category': {'type': 'science', 'id': 0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_non_exist_category_play_quizzes(self):
        res = self.client().post('/quizzes', json={'previous_questions': [1, 2], 'quiz_category': {'type': 'mathematics', 'id':10}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
    
    def test_404_no_questions_play_quizzes(self):
        res = self.client().post('/quizzes', json={'previous_questions': [1, 2], 'quiz_category': {'type': 'art', 'id':2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
