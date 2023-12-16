from flask import (Blueprint,render_template,url_for,flash,
                   redirect,request,abort)
from flask_login import current_user,login_required
from app.models import Post,Comment,User,Question
from app.posts.forms import PostForm,CommentForm,SearchForm
from app import db
import markdown
from pygments.formatters import HtmlFormatter
from markdown.extensions.codehilite import CodeHiliteExtension
from sqlalchemy.sql import union


posts = Blueprint('posts',__name__)

#Post.query has a method called paginate() which helps in pagination
#it has many useful methods which can be seen by dir(posts)
#posts.per_page - default is 20
#posts.page  - current page no.
#posts = post.query.paginate(per_page=5,page=2) - per pge is 5 and move to page 2
#posts.item - to display the items of the page in lists format
#post.query.paginate(per_page=no.)
#posts.total - to view total pages 
# pages.iter_pages() and for loop

@posts.route('/post/new',methods=['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    description=form.description.data,
                    )
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created','success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html',title='New Post',form=form,
                            legend='New Post' )

@posts.route('/post/<int:post_id>',methods=['GET','POST'])    
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.datecreated.desc()).all()
    post_content = markdown.markdown(post.content,extensions=['nl2br','codehilite','fenced_code'])
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(body=form.body.data, user_id=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been posted!', 'success')
            return redirect(url_for('posts.post', post_id=post.id))
        else:
            flash('You need to be logged in to comment.', 'danger')
    # comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('post.html', title=post.title, post=post,post_content=post_content, form=form,comments=comments)


@posts.route('/post/<int:post_id>/update',methods=['POST','GET'])
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.description = form.description.data
        #no need of adding as it is already present in the database
        db.session.commit()
        flash('Post has been updated!','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method=='GET':
        #to update the content in the field already
        form.title.data = post.title
        form.content.data = post.content
        form.description.data=post.description
    return render_template('create_post.html',title='Update Post',
                           form=form,legend='Update Post')

@posts.route('/post/<int:post_id>/delete',methods=['POST'])
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('main.index'))


@posts.route('/searched',methods=["POST","GET"])
def searched(): 
    form = SearchForm()
    if form.validate_on_submit():
        searched = form.searched.data
        
        posts = Post.query.filter(Post.title.like('%'+searched+'%'))\
                          .order_by(Post.date_posted.desc())
                          
        questions = Question.query.filter(Question.title.like('%' + searched + '%')) \
            .order_by(Question.date_posted.desc())
                          
        return render_template('searched.html',form=form,posts = posts,searched=searched,questions=questions)
    return render_template('searched.html')


@posts.context_processor
def basde():
    form=SearchForm()
    return dict(form=form)