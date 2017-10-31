# -*- coding: utf-8 -*-
from eve import Eve
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_mail import Mail
from flask_security import Security, MongoEngineUserDatastore

from models import db, User
from settings import SETTINGS
from views import post_tasks_insert_callback, pre_tasks_insert_callback

io = SocketIO()
user_datastore = MongoEngineUserDatastore(db, User, None)


def create_app():
    """Create an application"""
    app = Eve(settings=SETTINGS)
    # MongoDB setup
    app.config['MONGO2_DBNAME'] = SETTINGS['MONGO_DBNAME']  # TODO Needed?
    app.config['MONGODB_DB'] = SETTINGS['MONGO_DBNAME']
    app.config['SECRET_KEY'] = 'secret!'
    # TODO Mail setup
    app.config['MAIL_SERVER'] = 'smtp.example.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'username'
    app.config['MAIL_PASSWORD'] = 'password'

    mail = Mail(app)
    CORS(app)

    from app.websockets import websockets_blueprint
    from app.views import views_blueprint
    # Setup Flask-Security
    security = Security(app, user_datastore)
    app.register_blueprint(websockets_blueprint)
    app.register_blueprint(views_blueprint)

    # Eve event hooks
    # app.on_insert_task += pre_tasks_insert_callback
    # app.on_inserted_task += post_tasks_insert_callback

    db.init_app(app)
    io.init_app(app)

    return app
