from flask import (Blueprint,render_template,url_for,flash,
                   redirect,request,abort)
from flask_login import current_user,login_required
from app.models import Question,Question_Comment
from app.question.forms import PostForm,CommentForm
from app import db
import markdown


question = Blueprint('question',__name__)



@question.route('/question/new',methods=['POST','GET'])
@login_required
def new_question():
    form = PostForm()
    if form.validate_on_submit():
        post = Question(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    tags = form.topicTags.data,
                    description=form.description.data)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created','success')
        return redirect(url_for('main.index'))
    return render_template('create_question.html',title='New Question',form=form,
                            legend='New question')

@question.route('/question/<int:post_id>',methods=['GET','POST'])    
def questions(post_id):
    question = Question.query.get_or_404(post_id)
    comments = Question_Comment.query.filter_by(questoin_id=post_id).order_by(Question_Comment.datecreated.desc()).all()
    question_content = markdown.markdown(question.content,extensions=['nl2br','codehilite','fenced_code'])
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Question_Comment(body=form.body.data, user_id=current_user.id, questoin_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been posted!', 'success')
            return redirect(url_for('question.questions', post_id=question.id))
        else:
            flash('You need to be logged in to comment.', 'danger')
    # comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('question.html', title=question.title, question=question,question_content=question_content, form=form,comments=comments)


@question.route('/question/<int:post_id>/update',methods=['POST','GET'])
def update(post_id):
    question = Question.query.get_or_404(post_id)
    if question.author!=current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        question.title = form.title.data
        question.content = form.content.data
        question.description = form.description.data
        question.tags = form.topicTags.data
        #no need of adding as it is already present in the database
        db.session.commit()
        flash('Post has been updated!','success')
        return redirect(url_for('question.questions',post_id=question.id))
    elif request.method=='GET':
        #to update the content in the field already
        form.title.data = question.title
        form.content.data = question.content
        form.description.data= question.description
        form.topicTags.data = question.tags
    return render_template('create_question.html',title='Update Question',
                           form=form,legend='Update Question')

@question.route('/question/<int:post_id>/delete',methods=['POST'])
def delete(post_id):
    question = Question.query.get_or_404(post_id)
    if question.author!=current_user:
        abort(403)
    db.session.delete(question)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('main.index'))

