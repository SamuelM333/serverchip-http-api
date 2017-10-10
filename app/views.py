from bson.objectid import ObjectId, InvalidId
from bson.json_util import loads, dumps
from flask import Blueprint, jsonify
from mongoengine import DoesNotExist

from settings import GPIO_PORTS
from models import Microchip, User, Task

views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/microchip/<microchip_id>/ports', methods=['GET'])
def get_available_ports(microchip_id):
    # Find the microchip or give a 404 right away

    try:
        microchip = Microchip.objects.get(_id=ObjectId(microchip_id))
        available_ports = list(GPIO_PORTS)
        tasks = Task.objects(microchip=ObjectId(microchip_id))

        for task in tasks:
            if task.output_port.number in available_ports:
                available_ports.remove(task.output_port.number)

            for condition in task.conditions:
                if condition.input_port:
                    if condition.input_port.number in available_ports:
                        available_ports.remove(condition.input_port.number)

        return jsonify(available_ports=available_ports)

    except (DoesNotExist, InvalidId) as e:
        print type(e)
        if type(e) == InvalidId:
            return 'InvalidId'  # TODO Return error
        else:
            return 'document not found'  # TODO Return 404
