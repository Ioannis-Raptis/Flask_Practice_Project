import datetime


from flask import (
    flash, jsonify, logging, redirect, render_template, request, session,
    url_for, abort, Blueprint)


from flaskapp import db
from flaskapp.users.forms import LoginForm, RegisterForm
from flaskapp.articles.forms import ArticleForm
from flaskapp.models import Article, User
from flaskapp.main.routes import login_required

articles = Blueprint('articles', __name__)

# Articles
@articles.route('/articles')
def all_articles():
    articles = Article.query.all()
    if articles:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('articles.html', msg=msg)

# Single Article
@articles.route('/article/<string:id>/')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', article=article)

# Article creation
@articles.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm()
    if form.validate_on_submit():
        user_id = User.query.filter_by(
            username=session['username']).first().id
        new_article = Article(title=form.title.data, body=form.body.data,
                              user_id=user_id, creation_date=datetime.datetime.now())

        db.session.add(new_article)
        db.session.commit()

        flash('Article created', 'success')

        return redirect(url_for('main.dashboard'))
    return render_template('add_article.html', form=form, legend='Add Article')

# Article editing
@articles.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    current_user_id = User.query.filter_by(
        username=session['username']).first().id
    if article.author.id != current_user_id:
        abort(403)
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.body = form.body.data
        db.session.commit()
        flash('Your article has been updated!', 'success')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.title.data = article.title
        form.body.data = article.body
    return render_template('add_article.html', form=form, legend='Update Article')

# Article deletion
@articles.route('/delete_article/<string:id>', methods=['POST'])
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)
    current_user_id = User.query.filter_by(
        username=session['username']).first().id
    print(article.author.id, current_user_id)
    if article.author.id != current_user_id:
        abort(403)
    db.session.delete(article)
    db.session.commit()
    flash('Your article has been deleted!', 'success')
    return redirect(url_for('main.dashboard'))
