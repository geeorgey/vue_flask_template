from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
import sqlalchemy_utils

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.Text)
    #参考：https://qiita.com/revvve44/items/b91e0a1fc6d5eb9a31c8
    def __init__(self, email, password):
        """ ユーザ名、メール、パスワードが入力必須 """
        self.email = email
        self.password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """ パスワードをチェックしてTrue/Falseを返す """
        return check_password_hash(self.password, password)

    def reset_password(self, password):
        """ 再設定されたパスワードをDBにアップデート """
        self.password = generate_password_hash(password).decode('utf-8')

    @classmethod
    def select_by_email(cls, email):
        """ UserテーブルからemailでSELECTされたインスタンスを返す """
        return cls.query.filter_by(email=email).first()

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

def init_db(app):
    db.init_app(app)
    Migrate(app, db)