from flask import render_template, url_for, flash, redirect, request
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash

from app.master_routes import bp
from app.extensions import db
from app.models import User, Movies
from app.forms import LoginForm, RegistrationForm, SearchForm, MovieRatingForm
from flask_login import login_user, current_user, logout_user, login_required


@bp.route('/')
@bp.route('/home')
def home():
    print("Home route called")
    return render_template('home.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('master.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists!', 'danger')
            return render_template('register.html', title='Register', form=form)
        hashed_password = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created for {}!'.format(form.email.data), 'success')
        return redirect(url_for('master.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('master.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('master.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
        return redirect(url_for('master.home'))
    return render_template('login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('master.home'))


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('master.search_results', query=form.title.data))
    return render_template('search.html', title='Search', form=form)


@bp.route('/movies', methods=['GET', 'POST'])
def display_movies():
    return render_template('movies.html', title='Movies', movies=Movies.query.options(
        joinedload(Movies.stars),
        joinedload(Movies.directors),
        joinedload(Movies.rating)
    ).limit(30).all())


@bp.route('/movie/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    movie = Movies.query.options(
        joinedload(Movies.stars),
        joinedload(Movies.directors),
        joinedload(Movies.rating)
    ).get_or_404(movie_id)
    return render_template('movie_detail.html', title=movie.title, movie=movie)


@bp.route('/movie/<int:movie_id>/rate', methods=['GET', 'POST'])
@login_required
def rate_movie(movie_id):
    movie = Movies.query.options(
        joinedload(Movies.stars),
        joinedload(Movies.directors),
        joinedload(Movies.rating)
    ).get_or_404(movie_id)
    form = MovieRatingForm()
    if form.validate_on_submit():
        movie.rating[0].rating = (movie.rating[0].rating * movie.rating[0].votes + form.rating.data) / (movie.rating[0].votes + 1)
        movie.rating[0].votes += 1
        db.session.commit()
        flash('Your rating has been updated!', 'success')
        return redirect(url_for('master.movie_detail', movie_id=movie.id))
    elif request.method == 'GET':
        form.rating.data = 0  # movie.rating[0].rating
        form.rating.votes = movie.rating[0].votes
    return render_template('rate_movie.html', title='Rate Movie', form=form, movie=movie)
