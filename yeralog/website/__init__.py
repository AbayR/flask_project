from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from flask_admin import Admin

db = SQLAlchemy()

from flask_admin.contrib.sqla import ModelView
from .models import *

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "yera1234"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment, Like, Contact

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    admin = Admin(app)
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(Like, db.session))
    admin.add_view(ModelView(Contact, db.session))
    return app


