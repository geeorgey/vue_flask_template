from flask import Blueprint, render_template, request, jsonify, make_response
from dotenv import load_dotenv
from flask_login import login_required, current_user

from sqlalchemy.orm.exc import NoResultFound
import json
import random
import datetime
import os
from datetime import date

from . import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def index(path):
    return render_template('index.html')
    
# /get_members_calendarにPOSTリクエストが送られたら処理してJSONを返す
@main.route('/testclass', methods=['POST'])
def testclass():
    print('hello test')
    return jsonify(values='return testclass')

if __name__ == '__main__':
    app.run()