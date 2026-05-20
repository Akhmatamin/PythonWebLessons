from flask import Flask, make_response, request

app = Flask(__name__)

api_keys = {
    "123456": "Application A",
    "abcdef": "Application B",
}

def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key not in api_keys:
            return make_response({"message": "Unauthorized"}, 401)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/public')
def public():
    return make_response({"message": "Hello World!"}, 200)

@app.route('/private')
@require_api_key
def private():
    return make_response({"message": "Hello World!"}, 200)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001)