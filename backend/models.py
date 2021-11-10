from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
import sqlalchemy_utils
from slack_sdk.oauth.installation_store.models.bot import Bot
from slack_sdk.oauth.installation_store.models.installation import Installation
from sqlalchemy.types import Float
from sqlalchemy.types import TIMESTAMP

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


class InstalledWorkSpace(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    slack_ws_id = db.Column(db.String(100))
    slack_ws_name = db.Column(db.String(100))
    enterprise_id = db.Column(db.String)
    user_num = db.Column(db.Integer, default=0)
    plan = db.Column(db.String(2000))
    free_expired_at = db.Column(db.DateTime)
    plan_expired_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    installed_at = db.Column(db.DateTime)
    channel_joined_at = db.Column(db.DateTime)
    deepl_api_key = db.Column(db.String(100))
    postlimit = db.Column(db.Integer, default=0)
    timezone = db.Column(db.String(100))

class SlackInstallations(Installation, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.String, nullable=False)
    app_id = db.Column(db.String, nullable=False)
    enterprise_id = db.Column(db.String)
    enterprise_name = db.Column(db.String)
    enterprise_url = db.Column(db.String)
    team_id = db.Column(db.String)
    team_name = db.Column(db.String)
    bot_token = db.Column(db.String)
    bot_id = db.Column(db.String)
    bot_user_id = db.Column(db.String)
    bot_scopes = db.Column(db.String)
    user_id = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String)
    user_token = db.Column(db.String)
    user_scopes = db.Column(db.String)
    incoming_webhook_url = db.Column(db.String)
    incoming_webhook_channel = db.Column(db.String)
    incoming_webhook_channel_id = db.Column(db.String)
    incoming_webhook_configuration_url = db.Column(db.String)
    is_enterprise_install = db.Column(db.Boolean, default=False, nullable=False)
    token_type = db.Column(db.String)
    bot_refresh_token = db.Column(db.String(200))
    bot_token_expires_at = db.Column(db.DateTime)
    user_refresh_token = db.Column(db.String(200))
    user_token_expires_at = db.Column(db.DateTime)

class SlackBots(Bot, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.String)
    enterprise_id = db.Column(db.String)
    bot_token = db.Column(db.String(200))
    bot_refresh_token = db.Column(db.String(200))
    bot_token_expires_at = db.Column(db.DateTime)    
    bot_id = db.Column(db.String(200))

def init_db(app):
    db.init_app(app)
    Migrate(app, db)