"""""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DB_NAME = diet.db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jsjhjhjsdh jhshjfh'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

"""