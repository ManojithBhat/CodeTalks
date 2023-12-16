from datetime import datetime
from app import db,login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
#usermixin is a class that gives user authentication,isactive and other 2 methods needed for loader

#a decorator function  user id as a arguement
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),default='default.jpg',nullable=False)
    password = db.Column(db.String(60),nullable=False)
    posts= db.relationship('Post',backref='author',lazy=True)
    question= db.relationship('Question',backref='author',lazy=True)
    comments= db.relationship('Comment',backref='author',lazy=True)
    question_comments = db.relationship('Question_Comment',backref='author',lazy=True)

    def get_reset_token(self,expires_sec=str(1800)):
        s=Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id})
    #.decode('utf-8')
    
    #  a static method is bound to a class rather than the objects for that class.
    @staticmethod
    def verify_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),unique=True,nullable=False)
    content = db.Column(db.Text,nullable=False)
    description = db.Column(db.String(400),nullable=False,default='No description provided for this post')
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    comments= db.relationship('Comment',backref='post',lazy=True)

    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000), nullable=False)
    datecreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)



class Question_Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000), nullable=False)
    datecreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questoin_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),unique=True,nullable=False)
    content = db.Column(db.Text,nullable=False)
    tags = db.Column(db.String(200))
    description = db.Column(db.String(400),nullable=False,default='No description provided for this post')
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    comments= db.relationship('Question_Comment',backref='question',lazy=True)

    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"