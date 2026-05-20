from datetime import datetime
from functools import wraps
from hashlib import sha1
from uuid import uuid4

import jwt
from flask import Blueprint, make_response, request, render_template, session, redirect, url_for

from app import app
from db import task_storage, users
bp = Blueprint("tasks", __name__, template_folder="templates/tasks")

def get_user_tasks(username):
    return {
        task_id: task_info for task_id, task_info in task_storage.items()
        if task_info['username'] == username
    }

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = session.get("token")
        if not token:
            return redirect(url_for("auth.login"))

        try:
            payload = jwt.decode(token, app.secret_key, 'HS256')
            username = payload['username']

            if username not in users:
                return redirect(url_for("auth.login"))

            session['username'] = username

        except jwt.exceptions.DecodeError:
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)
    return wrapper

@bp.get("/")
@auth_required
def list_tasks():
    completed_flag = request.args.get("completed")  # fetch the query parameter
    if completed_flag and completed_flag.lower() not in ("true", "false"):
        completed_flag = None

    flag_mapping = {"true": True, "false": False}

    # return all tasks if query parameter was not provided
    tasks = get_user_tasks(session["username"])
    if completed_flag:
        # filter only not completed tasks
        tasks = {
            task_id: task_info for task_id, task_info in task_storage.items()
            if task_info["is_completed"] == flag_mapping[completed_flag.lower()]
        }

    return render_template("dashboard.html", tasks=tasks)  # return tasks

@bp.get('/new_task')
@auth_required
def get_create_task_page():
    return render_template("new_task.html")


@bp.post("/new_task")
@auth_required
def create_task():
    task_id = uuid4().hex
    task_info = {
        'title': request.form.get("title", 'Missed title'),
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'is_completed': False,
        'username': session['username'],
    }
    task_storage[task_id] = task_info
    return redirect(url_for('tasks.list_tasks'))

# @bp.post("/")
# @auth_required
# def create_task():
#     task_id = uuid4().hex  # generate task ID
#     task_info = {
#         "title": request.json.get("title", "Missed title"),  # get `title` from the request body
#         "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # get current time
#         "is_completed": False,  # by default a new task is not completed
#         "username": request.authorization.username,
#     }
#
#     task_storage[task_id] = task_info  # save the task in the storage
#
#     return make_response({"id": task_id})  # return ID of the new task


@bp.put("/<task_id>")
@auth_required
def mark_completed(task_id):
    tasks = get_user_tasks(session["username"])
    task = tasks.get(task_id)  # try to find task by the provided ID from the path
    if not task:
        # say to a user that the task with provided ID doesn't exist
        return make_response({"message": "Task not found"}, 404)

    if task['username'] != session["username"]:
        return make_response({"message": "Access denied"}, 403)

    task["is_completed"] = True  # mark the task as completed

    return redirect(url_for('tasks.list_tasks'))


@bp.delete("/<task_id>")
@auth_required
def delete(task_id):
    task = task_storage.get(task_id)
    if not task:
        # say to a user that the task with provided ID doesn't exist
        return redirect(url_for('delete'))

    if task['username'] != session["username"]:
        return redirect(url_for('delete', task_id=task_id))

    task_storage.pop(task_id)

    return make_response({"deleted": True})
