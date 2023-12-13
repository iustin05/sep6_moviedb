from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Association tables
movies_directors = db.Table('directors',
                            db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                            db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
                            )

movies_stars = db.Table('stars',
                        db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                        db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
                        )


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Date(), nullable=False)
    directors = db.relationship('People', secondary=movies_directors, backref=db.backref('directed', lazy='dynamic'))
    stars = db.relationship('People', secondary=movies_stars, backref=db.backref('starred', lazy='dynamic'))

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth = db.Column(db.String(10), nullable=True)


class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    rating = db.Column(db.Float, nullable=False)
    votes = db.Column(db.Integer, nullable=False)
    movie = db.relationship('Movies', backref='rating', lazy=True)
