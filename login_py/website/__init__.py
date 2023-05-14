from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import path
from flask_login import LoginManager

database = SQLAlchemy()
DB_NAME = "databse.db" 


def create_app():
    app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    database.init_app(app)

    
    from .views import views
    from .auth import auth
    from .models import User, Note
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)   
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    with app.app_context():
        database.create_all()
    
    return app

# def creat_database(app):
#     if not path.exists('website/ + DB_NAME'):
#         database.create_all(app=app)
#         print('Database created')
