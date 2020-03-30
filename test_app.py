import os
import unittest
import json
import datetime
#from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Actor, Movie, Gender

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app(os.environ['TEST_DATABASE_URL'])
        self.client = self.app.test_client
        self.assistant_jwt = os.environ['ASSISTANT_JWT']
        self.director_jwt = os.environ['DIRECTOR_JWT']
        self.producer_jwt = os.environ['PRODUCER_JWT']

        a = Actor(name='Kenneth Torkel', age='30', gender=Gender('M'))
        a.insert()

        m = Movie(title='Genesis', date_release='20200328', actors=[a])
        m.insert()

    def tearDown(self):

        actors = Actor.query.all()
        [a.delete() for a in actors]

        movies = Movie.query.all()
        [m.delete() for m in movies]

        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def add_jwt_header(role):
        def add_jwt_header_decorator(f):
            def wrapper(self):
                if role == 'assistant':
                    h = ['bearer', self.assistant_jwt]
                elif role == 'director':
                    h = ['bearer', self.director_jwt]
                elif role == 'producer':
                    h = ['bearer', self.producer_jwt]
                else:
                    h = ['bearer', self.assistant_jwt]
                headers = {'Authorization': ' '.join(h)}
                f(self, headers)
            return wrapper
        return add_jwt_header_decorator
    
    def test_base(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    '''

    Test for success behavior of each endpoint

    '''

    @add_jwt_header('assistant')
    def test_get_actors(self, headers):

        res = self.client().get('/actors', headers=headers)
        self.assertEqual(res.status_code, 200)

    @add_jwt_header('assistant')
    def test_get_movies(self, headers):

        res = self.client().get('/movies', headers=headers)
        self.assertEqual(res.status_code, 200)

    @add_jwt_header('director')
    def test_delete_actor(self, headers):

        a_id = Actor.query.all()[0].id
        res = self.client().delete(f'/actors/{a_id}', headers=headers)
        data = json.loads(res.data)
        a = Actor.query.filter(Actor.id == f'{a_id}').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(a, None)

    @add_jwt_header('producer')
    def test_delete_movie(self, headers):

        m_id = Movie.query.all()[0].id
        res = self.client().delete(f'/movies/{m_id}', headers=headers)
        data = json.loads(res.data)
        m = Movie.query.filter(Movie.id == f'{m_id}').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(m, None)

    @add_jwt_header('director')
    def test_add_actor(self, headers):

        res = self.client().post('/actors', headers=headers,
                                            data=json.dumps({
                                                'name': 'Lars Larsson', 
                                                'age': 38,
                                                'gender': 'M'}), 
                                            content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        a_id = data['actor_id']
        a = Actor.query.filter(Actor.id == a_id).one_or_none()
        self.assertIsNotNone(a)
    
    @add_jwt_header('producer')
    def test_add_movie(self, headers):

        a = Actor(name='Lars Larsson', age=38, gender=Gender('M'))
        a.insert()
        
        res = self.client().post('/movies', headers=headers,
                                            data=json.dumps({
                                                'title': 'Genesis II',
                                                'date_release': '20200328',
                                                'actors_id': [a.id]
                                            }),
                                            content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        m_id = data['movie_id']
        m = Movie.query.filter(Movie.id == m_id).one_or_none()
        self.assertIsNotNone(m)
    
    @add_jwt_header('director')
    def test_patch_actor(self, headers):

        a = Actor(name='Lars Larsson', age=38, gender=Gender('M'))
        a.insert()
        a_id = a.id

        #
        # change age to 40
        #
        res = self.client().patch(f'/actors/{a_id}', headers=headers,
                                                     data=json.dumps({
                                                        'name': 'Lars Larsson',
                                                        'age': 40,
                                                        'gender': 'M'
                                                     }),
                                                     content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(a_id, data['actor_id'])

        #
        # check age is changed
        #
        a = Actor.query.filter(Actor.id == a_id).one_or_none()
        self.assertEqual(a.age, 40)

    @add_jwt_header('director')
    def test_patch_movie(self, headers):

        a = Actor(name='Lars Larsson', age=38, gender=Gender('M'))
        a.insert()

        m = Movie(title='Genesis II', date_release='20200320', actors=[a])
        m.insert()

        #
        # change date_release
        #
        res = self.client().patch(f'/movies/{m.id}', headers=headers,
                                                      data=json.dumps({
                                                            'title': 'Genesis II',
                                                            'date_release': '20200328',
                                                            'actors_id': [a.id]
                                                      }),
                                                      content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(m.id, data['movie_id'])

        # 
        # check date is changed
        #
        m1 = Movie.query.filter(Movie.id == m.id).one_or_none()
        self.assertEqual(m1.date_release, datetime.datetime.strptime('20200328', '%Y%m%d').date())

    '''

    Test of error behavior of each end point

    '''

    def test_401_authorization_header_missing_get_actors(self):

        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    def test_401_authorization_header_missing_get_movies(self):

        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    @add_jwt_header('director')
    def test_404_actor_does_not_exist_delete_actor(self, headers):

        #
        # delete actor with actor id = 10000
        #
        res = self.client().delete('/actors/10000', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    @add_jwt_header('producer')
    def test_404_movie_does_not_exist_delete_movie(self, headers):

        #
        # delete movie with movie id = 10000
        #
        res = self.client().delete('/movies/10000', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    @add_jwt_header('director')
    def test_400_bad_input_request_post_actor(self, headers):

        #
        # post actor but with missing name
        #
        res = self.client().post('/actors', headers=headers,
                                            data=json.dumps({
                                                 'age': 45,
                                                 'gender': 'M'
                                            }),
                                            content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    @add_jwt_header('producer')
    def test_400_bad_input_request_post_movie(self, headers):

        #
        # post movie but with missing title
        #
        a = Actor.query.all()[0]
        res = self.client().post('/movies', headers=headers,
                                            data=json.dumps({
                                                'release_date': '20200329',
                                                'actors_id': [a.id]
                                            }),
                                            content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    @add_jwt_header('director')
    def test_400_bad_input_request_patch_actor(self, headers):

        #
        # patch actor but with missing name
        #
        a = Actor.query.all()[0]
        res = self.client().patch(f'/actors/{a.id}', headers=headers,
                                                     data=json.dumps({
                                                         'age': 45,
                                                         'gender': 'M'
                                                     }),
                                                     content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    @add_jwt_header('producer')
    def test_404_movie_does_not_exist_patch_movie(self, headers):

        #
        # patch movie which does not exist
        #
        res = self.client().patch('/movies/10000', headers=headers,
                                                   data=json.dumps({
                                                       'title': 'Super Hero',
                                                       'date_release': '20200329',
                                                       'actors_id': [1,2,3]
                                                   }),
                                                   content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''

    Test of correct RBAC behavior for each role

    '''

    @add_jwt_header('assistant')
    def test_rbac_get_actors(self, headers):

        #
        # Casting assistant can get a list of actors
        #
        res = self.client().get('/actors', headers=headers)
        self.assertEqual(res.status_code, 200)

    @add_jwt_header('assistant')
    def test_rbac_401_action_forbidden_delete_actor(self, headers):

        #
        # Casting assistant does not allow delete actor
        #
        a = Actor.query.all()[0]
        res = self.client().delete(f'/actors/{a.id}', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Action forbidden.')
        self.assertEqual(data['success'], False)

    '''
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], Tre)

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
