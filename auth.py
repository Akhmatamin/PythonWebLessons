from flask import Blueprint, make_response, request, Response
from hashlib import sha1
from db import users
import jwt
from app import app

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.post('/sign_up')
def sign_up():
    username = request.json.get('username')
    password = request.json.get('password')
    error = None

    status_code = 204

    if not username:
        error, status_code = "Username is required", 400
    elif not password:
        error, status_code = "Password is required", 400
    elif username in users:
        error, status_code = "User already exists", 409

    if error:
        make_response({"message": error}, status_code)

    users[username] = sha1(password.encode()).hexdigest()

    return Response(status=status_code)


@bp.post('/login')
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    error = None
    status_code = 200

    if not username:
        error, status_code = "Username is required", 400
    elif not password:
        error, status_code = "Password is required", 400
    elif username not in users or sha1(password.encode()).hexdigest() != users[username]:
        error, status_code = "Invalid credentials", 401
    if error:
        make_response({"message": error}, status_code)

    token = jwt.encode({'username': username}, app.secret_key)

    return make_response({"token": token}, status_code)
