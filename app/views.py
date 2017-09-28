from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from flask import Blueprint, jsonify

from settings import GPIO_PORTS
from app import mongo

views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/microchip/<microchip_id>/ports', methods=['GET'])
def get_available_ports(microchip_id):
    # Find the microchip or give a 404 right away
    # TODO test if microchip_id.type is ObjectId
    microchip = mongo.db.microchip.find_one_or_404({'_id': ObjectId(microchip_id)})
    available_ports = list(GPIO_PORTS)
    tasks = mongo.db.task.find({'microchip': ObjectId(microchip_id)})

    for task in tasks:
        if task['output_port']['number'] in available_ports:
            available_ports.remove(task['output_port']['number'])

        for condition in task['conditions']:
            if condition.get('input_port'):
                if condition['input_port']['number'] in available_ports:
                    available_ports.remove(condition['input_port']['number'])

    return jsonify(available_ports=available_ports)
