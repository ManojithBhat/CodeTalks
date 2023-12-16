from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField,SubmitField,BooleanField,FileField
from wtforms.validators import DataRequired,Email,ValidationError,EqualTo,Length
from flask_login import current_user
from app.models import User
from flask_wtf.file import FileField,FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField("Email",
                        validators=[DataRequired(),Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",
                                   validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    #a function for validating that the username won't already exist in our database 
    def validate_username(self,username):

        user = User.query.filter_by(username=username.data).first()
        #return the value if the user is present and none when it is not there hence not evaluated
        if user:
            raise ValidationError('That username is taken. Please choose a differnet username')
        
    #function name is important here      
    def validate_email(self,email):

        user = User.query.filter_by(email=email.data).first()
        #return the value if the user is present and none when it is not there hence not evaluated
        if user:
            raise ValidationError('That email is taken. Please choose a differnet email')


class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(),Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login Up')



class UpdateForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField("Email",
                        validators=[DataRequired(),Email()])
    picture = FileField('update profile pic',validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField('Update')

    #to check whether the username updated by the user is already taken or not
    def validate_username(self,username):
        #they can take the username that they have already taken hence this if condition 
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            #return the value if the user is present and none when it is not there hence not evaluated
            if user:
                raise ValidationError('That username is taken. Please choose a differnet username')

        
    #function name is important here      
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            #return the value if the user is present and none when it is not there hence not evaluated
            if user:
                raise ValidationError('That email is taken. Please choose a differnet email')


