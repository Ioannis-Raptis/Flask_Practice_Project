from flask import Blueprint, render_template, session, flash, url_for
from functools import wraps
from flaskapp.models import Article
from flaskapp import db

main = Blueprint('main', __name__)

# Index
@main.route('/')
def index():
    return render_template('home.html')

# About
@main.route('/about')
def about():
    return render_template('about.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('users.login'))
    return decorated_function


# Dashboard
@main.route('/dashboard')
@login_required
def dashboard():
    articles = Article.query.all()
    if articles:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('dashboard.html', msg=msg)
