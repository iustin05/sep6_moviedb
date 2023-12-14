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
    favorite_movies = db.relationship('MovieDetails', secondary='favorites',
                                      backref=db.backref('favorited_by', lazy='dynamic'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_favorite(self, movie):
        return movie in self.favorite_movies


#
#
# # Association tables
# movies_directors = db.Table('directors',
#                             db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
#                             db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
#                             )
#
# movies_stars = db.Table('stars',
#                         db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
#                         db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
#                         )
#
favorites = db.Table('favorites', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('movie_id', db.Integer, db.ForeignKey('moviedetails.id'), primary_key=True))


# #
# #
# class Movies(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     year = db.Column(db.Date(), nullable=False)
#     directors = db.relationship('People', secondary=movies_directors, backref=db.backref('directed', lazy='dynamic'))
#     stars = db.relationship('People', secondary=movies_stars, backref=db.backref('starred', lazy='dynamic'))
#
#     def serialize(self):
#         return {
#             'id': self.id,
#             'title': self.title,
#         }


class MovieDetails(db.Model):
    __tablename__ = 'moviedetails'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Date(), nullable=False)
    directors = db.Column(db.String(300), nullable=True)
    stars = db.Column(db.String(300), nullable=True)
    votes = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    poster_url = db.Column(db.String(500), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
        }

#
# class People(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     birth = db.Column(db.String(10), nullable=True)
#
#
# class Ratings(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
#     rating = db.Column(db.Float, nullable=False)
#     votes = db.Column(db.Integer, nullable=False)
#     movie = db.relationship('Movies', backref='rating', lazy=True)
