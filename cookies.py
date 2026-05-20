from flask import Flask, redirect, url_for, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    username = request.cookies.get('username')
    if username:
        return f"Logged in as {username}"
    return 'Not logged in'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        resp = make_response(f"Hello, {username}! Click <a href='{url_for('index')}'>here</a>!")
        resp.set_cookie('username', username)
        return resp
    return """
        <form method="post">
            <p><input type="text" name="username">
            <p><input type="submit" value="Login">
        </form>
    """

@app.route('/logout')
def logout():
    resp = make_response(f"Logged out, cookie cleared. Click <a href='{url_for('index')}'>here</a>!")
    resp.delete_cookie('username')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
