import views, auth
from app import app

if __name__ == '__main__':
    app.register_blueprint(views.bp)
    app.register_blueprint(auth.bp)
    app.run(debug=True) 