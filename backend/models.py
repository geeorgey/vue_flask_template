from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_utils

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(1000))

def init_db(app):
    db.init_app(app)
    Migrate(app, db)