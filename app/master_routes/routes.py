from flask import render_template, url_for, flash, redirect, request, jsonify
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash

from app.master_routes import bp
from app.extensions import db
from app.models import User, MovieDetails
from app.forms import LoginForm, RegistrationForm, SearchForm, MovieRatingForm
from flask_login import login_user, current_user, logout_user, login_required

from app.tmdb_integration import get_movie_poster


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
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('master.home'))


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('master.search_results', query=form.title.data))
    return render_template('search.html', title='Search', form=form)


@bp.route('/search_result', methods=['GET', 'POST'])
@login_required
def search_result():
    query = request.args.get('query', '').lower()
    movies = MovieDetails.query.filter(MovieDetails.title.like(f"%{query}%")).all()
    return jsonify([movie.serialize() for movie in movies])


# @bp.route('/load_db_images', methods=['GET', 'POST'])
# def load_db_images():
#     movies = MovieDetails.query.limit(600).all()
#     for movie in movies:
#         if movie.poster_url is None or movie.poster_url == '':
#             movie.poster_url = get_movie_poster(movie.id)
#     db.session.commit()
#     return redirect(url_for('master.home'))


@bp.route('/movies', methods=['GET', 'POST'])
@login_required
def display_movies():
    page = request.args.get('page', 1, type=int)
    movies = MovieDetails.query.order_by(MovieDetails.id).paginate(page=page, per_page=18, error_out=False)

    for movie in movies.items:
        if movie.poster_url is None or movie.poster_url == '':
            movie.poster_url = get_movie_poster(movie.id)
    return render_template('movies.html', title='Movies', movies=movies)


@bp.route('/movie/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    movie = MovieDetails.query.get_or_404(movie_id)
    return render_template('movie_detail.html', title=movie.title, movie=movie, user=current_user)


@bp.route('/movie/<int:movie_id>/rate', methods=['GET', 'POST'])
@login_required
def rate_movie(movie_id):
    movie = MovieDetails.query.get_or_404(movie_id)
    form = MovieRatingForm()
    if form.validate_on_submit():
        movie.rating = (movie.rating * movie.votes + form.rating.data) / (
                movie.votes + 1)
        movie.votes += 1
        db.session.commit()
        flash('Your rating has been updated!', 'success')
        return redirect(url_for('master.movie_detail', movie_id=movie.id))
    elif request.method == 'GET':
        form.rating.data = 0  # movie.rating[0].rating
        form.rating.votes = movie.votes
    return render_template('rate_movie.html', title='Rate Movie', form=form, movie=movie)


@bp.route('/add_to_favorites/<int:movie_id>', methods=['POST'])
@login_required
def add_to_favorites(movie_id):
    movie = MovieDetails.query.get(movie_id)
    current_user.favorite_movies.append(movie)
    db.session.commit()
    return redirect(url_for('master.dashboard'))


@bp.route('/remove_from_favorites/<int:movie_id>', methods=['POST'])
@login_required
def remove_from_favorites(movie_id):
    movie = MovieDetails.query.get(movie_id)
    current_user.favorite_movies.remove(movie)
    db.session.commit()
    return redirect(url_for('master.dashboard'))


@bp.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(current_user.id)
    favorite_movies = user.favorite_movies
    return render_template('dashboard.html', favorite_movies=favorite_movies)
