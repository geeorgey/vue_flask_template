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
from .models import ToDo

main = Blueprint('main', __name__)

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def index(path):
    return render_template('index.html')
    
def get_my_todos(user_id):
    todos = []
    todos = ToDo.query.filter_by(user_id=user_id).all()
    res_todos = []
    for todo in todos:
        todo_dict = {}
        todo_dict['id'] = todo.id
        todo_dict['user_id'] = todo.user_id
        todo_dict['name'] = todo.name
        res_todos.append(todo_dict)
    return res_todos
    
@main.route('/addtodo', methods=['POST'])
def addtodo():
    print('Start addtodo-----')
    todo = request.json.get("todo", None)
    user_id = request.json.get("user_id", None)
    new_todo = ToDo(name=todo,user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'todo_list': get_my_todos(user_id)}), 200

@main.route('/deleteToDo', methods=['POST'])
def deleteToDo():
    print('Start deleteToDo-----')
    delete_todos = request.json.get("delete_todos", None)
    user_id = request.json.get("user_id", None)

    todo_ids = []
    for todo in delete_todos:
        print(todo)
        todo_ids.append(todo['id'])

    print('keyword_ids')
    print(todo_ids)
    db.session.query(ToDo).filter(ToDo.id.in_(todo_ids)).delete(synchronize_session='fetch')
    db.session.commit()

    return jsonify({'todo_list': get_my_todos(user_id)}), 200

@main.route('/fetchTodo', methods=['POST'])
def fetchTodo():
    print('Start deleteToDo-----')
    user_id = request.json.get("user_id", None)
    return jsonify({'todo_list': get_my_todos(user_id)}), 200

if __name__ == '__main__':
    app.run()