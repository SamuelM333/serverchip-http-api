# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from bson import json_util
from flask import request
from flask_socketio import join_room, leave_room, emit, rooms
from json import dumps
from app import io, mongo

# TODO Add validators for incoming data
# TODO Classify events by namespaces

daemon_sid = None


# Helpers

def get_simple_task_dict(task):
    conditions = list()
    conditions_count = 0  # Used to calculate the JSON_ARRAY_SiZE in the micro controller
    simple_task = {
        "_id": task["_id"],
        "output_port": task["output_port"]
    }

    for condition in task["conditions"]:
        if condition.get("input_port", False):
            conditions.append({"input_port": condition["input_port"]})
            conditions_count += 1

    simple_task['conditions'] = conditions
    simple_task['conditions_count'] = conditions_count

    return simple_task





@io.on('consult')
def handle_consult(data):
    response = False
    data = mongo.db.task.find_one_or_404({'name': data})
    print data
    if data is not None:
        response = dumps(data)

    io.emit('response', response)


# Daemon events

@io.on('daemon_connected')
def handle_daemon_connected(data):
    print data
    global daemon_sid
    daemon_sid = request.sid
    join_room('daemon')


# Microchip events

@io.on('microchip_connected')
def handle_microchip_connected(data):
    print 'microchip_connected'
    print data, request.sid, rooms(request.sid)
    microchip = mongo.db.microchip.find_one({'ip': data['ip']})

    print 'microchip', microchip

    if microchip is not None:
        join_room(data['ip'])
        tasks = mongo.db.task.find({'microchip': microchip['_id']})
        simple_tasks = list()
        for task in tasks:
            simple_tasks.append(get_simple_task_dict(task))

        response = {
            'sid': request.sid,
            'tasks': simple_tasks
        }
        json_response = json_util.dumps(response).replace('"', '\'')
        print json_response
        emit('microchip_connected_ack', json_response)
    else:
        emit('microchip_connected_ack', None)


@io.on('get_port_status_response_server')
def handle_get_port_status_response(data):
    emit('get_port_status_response_daemon', data, room='daemon')


@io.on('get_port_status_request')
def handle_get_port_status_request(data):
    microchip = mongo.db.microchip.find_one({'_id': ObjectId(data['microchip_id'])})
    print 'get_port_status_request', microchip['ip']

    emit('get_port_status', {}, room=microchip['ip'])


@io.on('run_task_request_server')
def handle_run_task_request_server(task):
    # TODO Write to logs here
    # Send here Simple Task dict to microchip
    json_response = json_util.dumps(get_simple_task_dict(task)).replace('"', '\'')
    print json_response
    emit('run_task_request_microchip', json_response, room=task['microchip']['ip'])


# General events

@io.on('disconnect')
def handle_disconnected():
    if request.sid == daemon_sid:
        # TODO Throw an error here
        print 'daemon disconnected'
