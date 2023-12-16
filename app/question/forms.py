from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,length

class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    description = StringField('description',validators=[length(max=400)])
    content = TextAreaField('Content',validators=[DataRequired()])
    topicTags = StringField('tags')
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired(), length(min=1, max=2000)])
    submit = SubmitField('Submit')