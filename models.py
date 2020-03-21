import enum
#from sqlalchemy import Column, String, Integer, DateTime, Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

class Gender(enum.Enum):
    male = 'M'
    female = 'F'

association_table = db.Table('association',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
)

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date_release = db.Column(db.Date)
    actors = db.relationship('Actor', secondary=association_table, 
                                backref=db.backref('movies'))

    def __init__(self, title, date_release, actors):
        self.title = title
        self.date_release = date_release
        self.actors = actors

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_actors(self):
        actors = []
        for i in self.actors:
            actors.append(i.id)
        return actors

    def format(self):
        return {
            'id': self.id, 
            'title': self.title,
            'date_release': self.date_release.strftime('%Y%m%d'),
            'actors_id': self.get_actors(),
        }

class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum(Gender))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_movies(self):
        movies = []
        for i in self.movies:
            movies.append(i.id)
        return movies

    def format(self):
        return {
            'id': self.id, 
            'name': self.name,
            'age': self.age,
            'gender': self.gender.value,
            'movies_id': self.get_movies(),
        }

@db.event.listens_for(db.session, "after_flush")
def after_flush(session, flush_context):
    print("After flush.......")
    session.query(Movie).\
        filter(~Movie.actors.any()).\
        delete(synchronize_session=False)