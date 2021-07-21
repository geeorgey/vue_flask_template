import flask
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user
import os
import json
import random
import ast
from flask_cors import CORS, cross_origin

auth = Blueprint('auth', __name__)

@auth.route("/auth/login", methods=["POST"])
def login():
    email = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.select_by_email(email)
    print('/auth/login')
    print(user)
    if user and user.check_password(password):
        """ ユーザに対してログイン処理を施す """
        return jsonify(
            access_token='test'
            ,expires_in=3600
            ,user_id=user.id
            ), 200
    elif user:
        return jsonify({"message": "メールアドレスとパスワードの組み合わせが間違っています。"}), 400
    else:
        return jsonify({"message": "存在しないユーザです"}), 400

@auth.route("/auth/register", methods=["POST"])
def register():
    email = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()

    if not user:#ユーザが登録前の場合はDBに登録する
        # add the new user to the database
        new_user = User(email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        #/ add the new user to the database
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(
            {
                "message": "登録完了しました。ログインしてください。",
                "access_token": "test",
                "expires_in": 3600
            }
            ), 200
    else:
        return jsonify({"message": "メールアドレスとパスワードの組み合わせが間違っている、もしくはリバネスIDが存在しません。"}), 400

@auth.route("/me", methods=["POST"])
def getme():
    email = request.json.get("username", None)
    print(email)
    user = User.query.filter_by(email=email).first()
    print(user.email)
    return jsonify(
        username=user.email
        ), 200



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
