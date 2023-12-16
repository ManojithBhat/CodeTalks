import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
db_key = os.getenv("DB_KEY")
secret_key = os.getenv("SECRET_KEY")


class Config:
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = db_key

