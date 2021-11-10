#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import generate_password_hash, check_password_hash
from slack_sdk.oauth.installation_store.models.bot import Bot
from slack_sdk.oauth.installation_store.models.installation import Installation
from sqlalchemy.types import Float
from sqlalchemy.types import TIMESTAMP


# 実行されるファイル(test_flask-migrate.py)の置き場所をbasedirに保存
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# データベースファイルは実行ファイルと同じ場所にapp.dbという名前で作成
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///app.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

db = SQLAlchemy(app)
# migrateインスタンスを定義
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.Text)
    # この関数は、インタープリタ(コンソール)からこのクラス(からできたインスタンス)を読んだ際に、どのように表示されるかを定義している。ここではusernameを表示させている。
    def __repr__(self):
        return '<User {}>'.format(self.username)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    def __repr__(self):
        return '<ToDo {}>'.format(self.name)

class InstalledWorkSpace(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    slack_ws_id = db.Column(db.String(100))
    slack_ws_name = db.Column(db.String(100))
    enterprise_id = db.Column(db.String)
    user_num = db.Column(db.Integer, default=0)
    plan = db.Column(db.String(2000))
    free_expired_at = db.Column(db.DateTime) #試用期間 登録の翌月末に設定すること
    plan_expired_at = db.Column(db.DateTime) #プラン期限
    is_active = db.Column(db.Boolean, default=True)
    installed_at = db.Column(db.DateTime)
    channel_joined_at = db.Column(db.DateTime)
    def __repr__(self):
        return '<InstalledWorkSpace {}>'.format(self.slack_ws_name)


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
    def __repr__(self):
        return '<SlackInstallations {}>'.format(self.id)

class SlackBots(Bot, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.String)
    enterprise_id = db.Column(db.String)
    bot_token = db.Column(db.String(200))
    bot_refresh_token = db.Column(db.String(200))
    bot_token_expires_at = db.Column(db.DateTime)  
    bot_id = db.Column(db.String(200))
    def __repr__(self):
        return '<SlackBots {}>'.format(self.id)
