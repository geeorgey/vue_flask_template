#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import generate_password_hash, check_password_hash


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
