# -*- coding: utf-8 -*-
from eve import Eve
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_security import (
    Security,
    MongoEngineUserDatastore,
    UserMixin,
    RoleMixin,
    login_required
)

from models import db, User
from settings import SETTINGS

# mongo = PyMongo()
io = SocketIO()
user_datastore = MongoEngineUserDatastore(db, User, None)


def create_app():
    """Create an application."""
    app = Eve(settings=SETTINGS)
    app.config['MONGO2_DBNAME'] = SETTINGS['MONGO_DBNAME']
    app.config['MONGODB_DB'] = SETTINGS['MONGO_DBNAME']
    app.config['SECRET_KEY'] = 'secret!'
    CORS(app)

    from app.websockets import websockets_blueprint
    from app.views import views_blueprint
    # Setup Flask-Security
    security = Security(app, user_datastore)
    app.register_blueprint(websockets_blueprint)
    app.register_blueprint(views_blueprint)
    db.init_app(app)
    io.init_app(app)

    return app
