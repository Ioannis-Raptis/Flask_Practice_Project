from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[
                        DataRequired(), Length(min=1, max=200)])
    body = StringField('Body', validators=[DataRequired(), Length(min=30)])
