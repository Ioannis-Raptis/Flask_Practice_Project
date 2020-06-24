from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from passlib.hash import sha256_crypt

from flaskapp import db
from flaskapp.main.routes import login_required
from flaskapp.models import User
from flaskapp.users.forms import LoginForm, RegisterForm

users = Blueprint('users', __name__)

# User register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = sha256_crypt.encrypt(str(form.password.data))
        new_user = User(name=form.name.data, email=form.email.data,
                        username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

# User login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        # Get form fields without WTForms
        username = form.username.data
        password_candidate = form.password.data

        # Get user by username
        result = User.query.filter_by(username=username).first_or_404()
        # Get stored hash
        password = result.password

        # Compare passwords
        if sha256_crypt.verify(password_candidate, password):
            # Passed
            session['logged_in'] = True
            session['username'] = username

            flash('You are now logged in', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            error = 'Invalid login'
            return render_template('login.html', title='Login', form=form, error=error)

    return render_template('login.html')

# Logout
@users.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('users.login'))
