from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.config import Config

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' #same the one that we are passing for url_for
login_manager.login_message_category = 'info' #to give the classname to the toggle message when we try to access that page

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from app.user.routes import users #name of the variable in the Blueprint
    from app.posts.routes import posts #name of the variable in the Blueprint
    from app.main.routes import main #name of the variable in the Blueprint
    from app.errors.handlers import errors  #name of the variable in the Blueprint
    from app.question.routes import question
    app.register_blueprint(question)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app