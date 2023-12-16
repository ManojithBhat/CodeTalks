from flask import Blueprint,redirect,render_template,url_for,request,flash
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Post,Question
from app.posts.forms import SearchForm
from app import db
from app.user.form import (RegistrationForm,LoginForm,UpdateForm)
import os,secrets
from app.user.utils import save_picture
from app import bcrypt
from flask import current_app


users = Blueprint('user',__name__)  #this user in the blueprint is used everywhere


@users.context_processor
def base():
    form=SearchForm()
    return dict(form=form)
@users.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm() #make a instance of registration form as it was a class
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            email= form.email.data,
            password= hashed_password
            )
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created','success')
        return redirect(url_for('user.login'))
        #after the form is validated it will show a flash message 
        #after validation redirect the page to home

    return render_template('register.html',title="Register",form=form)

@users.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm() #make a instance of Login form as it was a class
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
    
        if user and (bcrypt.check_password_hash(user.password,form.password.data)):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash("Login Unsuccessful, Please Check email and password",'danger')
    return render_template('login.html',title="login",form=form)


@users.route('/logout')
def logout():
    logout_user() #this will logout the user/ clear cookies and removes all the data of the object from current_user 
    return redirect(url_for('main.index'))

#as the name of the profile picture could be same. we can reduce the collision by using random hex no.
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    #it separates the file name and the extension
    #it is usual practice to use _ as variable name that won't be used later on
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pic',picture_fn)
    form_picture.save(picture_path)
    #The save method is often a method provided by the FileField or FileStorage object in WTForms. This method is used to save the uploaded file to a specific location on your server.
    
    return picture_fn


#only the authenticated user can only go for account route hence we have used login required decorator from the flask_login
@users.route('/account',methods=['POST','GET'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            #this if block will remove the photo is already exists in the pics
            if current_user.image_file != 'default.jpg':
                os.remove(os.path.join(current_app.root_path, 'static/profile_pic', current_user.image_file))
            picture_file=save_picture(form.picture.data)
            current_user.image_file = picture_file
        #the photo is not directly stored in the database it is stored in the profile_pic folder
        #and only the name of the photo(that is hexed) is sent to the database
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated!','success')
        return redirect(url_for('user.account'))
    
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pic/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)  
    # the above is the arguemtn in the url
    #access the other page by ?page=2
    # getting the user--first
    user = User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
                    .order_by(Post.date_posted.desc())\
                    .paginate(page=page,per_page=5)
    questions = Question.query.filter_by(author=user)\
                    .order_by(Question.date_posted.desc())\
                    .paginate(page=page,per_page=5)
    return render_template('user_post.html',posts = posts,user=user,questions=questions)
