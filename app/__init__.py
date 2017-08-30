from eve import Eve
from flask_pymongo import PyMongo
from flask_socketio import SocketIO

from settings import SETTINGS

mongo = PyMongo()
io = SocketIO()


def create_app():
    """Create an application."""
    app = Eve(settings=SETTINGS)
    app.config['MONGO_DBNAME'] = SETTINGS['MONGO_DBNAME']
    app.config['SECRET_KEY'] = '2f_0-+d*evl$@ci%&-ruodtr43=$nru!)wayh=l$n(*$+94gx9'

    from .websockets import main as main_blueprint
    app.register_blueprint(main_blueprint)
    mongo.init_app(app)
    io.init_app(app)
    return app
