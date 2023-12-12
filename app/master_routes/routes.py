from flask import render_template, url_for, flash, redirect, request
from werkzeug.security import generate_password_hash

from app.master_routes import bp
from app.extensions import db
from app.models import User, Movie
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


@bp.route('/movie/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie_detail.html', title=movie.title, movie=movie)
