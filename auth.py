from flask import Blueprint, make_response, request, Response, session, render_template, redirect, url_for
from hashlib import sha1
from db import users
import jwt
from app import app

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates/auth')


@bp.get('/sign_up')
def get_sign_up_page():
    message = session.get('message')
    session.clear()

    return render_template(('sign_up.html'), message=message)

@bp.post('/sign_up')
def sign_up():
    username = request.form.get('username')
    password = request.form.get('password')
    error = None

    if not username:
        error, status_code = "Username is required", 400
    elif not password:
        error, status_code = "Password is required", 400
    elif username in users:
        error, status_code = "User already exists", 409

    if error:
        session['message'] = {'content':error, 'is_error': True}
        return redirect(url_for('.sign_up'))

    session['message'] = {'content': 'User successfully created', 'is_error': False}

    users[username] = sha1(password.encode()).hexdigest()
    return redirect(url_for('.login'))


@bp.get('/login')
def get_login_page():
    message = session.get('message')
    session.clear()
    return render_template(('login.html'), message=message)


@bp.post('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    error = None

    if not username:
        error = "Username is required"
    elif not password:
        error = "Password is required"

    elif username not in users or sha1(password.encode()).hexdigest() != users[username]:
        error, status_code = "Invalid credentials", 401
    if error:
        session['message'] = {'content': error, 'is_error': True}
        return redirect(url_for('.login'))

    token = jwt.encode({'username': username}, app.secret_key)
    session['token'] = token
    return redirect(url_for('tasks.list_tasks'))


@bp.post('/logout')
def logout():
    session.clear()
    return redirect(url_for('.login'))
