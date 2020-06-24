from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Init app
app = Flask(__name__)

# Create a db connection with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myflaskapp.db'
app.config['SECRET_KEY'] = '1d020fe81a05f53499389ad4473993b9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Disable pep8 on these lines to avoid circular import issues
from flaskapp.users.routes import users  # nopep8
from flaskapp.articles.routes import articles  # nopep8
from flaskapp.main.routes import main  # nopep8
from flaskapp.errors.handlers import errors  # nopep8
app.register_blueprint(users)
app.register_blueprint(articles)
app.register_blueprint(main)
app.register_blueprint(errors)
