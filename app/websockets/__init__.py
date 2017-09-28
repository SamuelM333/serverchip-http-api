from flask import Blueprint

websockets_blueprint = Blueprint('websockets', __name__)

from app.websockets import events
