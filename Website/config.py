from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_database(app):
    with app.app_context():
        db.create_all()
    
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "123456abc"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///StudentAttendance.db'
    db.init_app(app)
    create_database(app)
    
    return app
