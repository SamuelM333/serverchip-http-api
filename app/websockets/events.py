# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from bson import json_util
from flask import request
from flask_socketio import join_room, leave_room, emit, rooms
from json import dumps

from app.models import Task, User, Microchip
from app import io

# TODO Add validators for incoming data
# TODO Classify events by namespaces

daemon_sid = None


# Helpers

def get_simple_task_dict(task):
    conditions = list()
    simple_task = {
        "_id": str(task["_id"]),
        "output_port": task["output_port"]
    }

    print simple_task["_id"]

    for condition in task["conditions"]:
        if condition.get("input_port", False):
            conditions.append({"input_port": condition["input_port"]})

    simple_task['conditions'] = conditions

    return simple_task


# Test events

@io.on('test_ws')
def handle_test_ws(data):
    print 'test_ws', data
    emit('test_ws_resp', 'test')


@io.on('join_room')
def on_join_room(data):
    room = data['room']
    join_room(room)


# @io.on('consult')
# def handle_consult(data):
#     response = False
#     data = mongo.db.task.find_one_or_404({'name': data})
#     print data
#     if data is not None:
#         response = dumps(data)
#
#     io.emit('response', response)


# Daemon events

@io.on('daemon_connected')
def handle_daemon_connected(data):
    print data
    global daemon_sid
    daemon_sid = request.sid
    join_room('daemon')


@io.on('add_task')
def handle_add_task(data):
    print 'add_task', data
    # task = mongo.db.task.find_one_or_404({'name': data['name']})
    task = Task.get(name=data['name'])  # TODO Handle 404 here
    emit('new_task', task, room='daemon')


# Microchip events

@io.on('microchip_connected')
def handle_microchip_connected(data):
    print 'microchip_connected'
    print data, request.sid, rooms(request.sid)
    microchip = Microchip.get(ip=data['ip'])  # TODO Handle 404 here

    print 'microchip', microchip

    if microchip is not None:
        join_room(data['ip'])
        tasks = Task.objects(microchip=microchip['_id'])
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


@io.on('new_input_port_condition')
def handle_new_input_port_condition(data):
    io.emit('add_new_input_port_condition', data, room=data['microchip_ip'])


@io.on('get_port_status_response_server')
def handle_get_port_status_response(data):
    emit('get_port_status_response_daemon', data, room='daemon')


@io.on('get_port_status_request')
def handle_get_port_status_request(data):
    microchip = Microchip.get(_id=ObjectId(data['microchip_id'])) # TODO Handle 404 here
    emit('get_port_status', {}, room=microchip['ip'])


@io.on('stop_task_request_server')
def handle_stop_task_request_server(task):
    # TODO Write to logs here
    # Send here Simple Task dict to microchip
    json_response = json_util.dumps(get_simple_task_dict(task)).replace('"', '\'')
    print json_response
    emit('stop_task_request_microchip', json_response, room=task['microchip']['ip'])


@io.on('run_task_request_server')
def handle_run_task_request_server(data):
    # TODO Write to logs here
    # Send here Simple Task dict to microchip
    json_response = json_util.dumps(data).replace('"', '\'')
    print 'handle_run_task_request_server', json_response
    emit('run_task_request_microchip', json_response, room=data['ip'])


@io.on('run_task_request_microchip_ack')
def handle_run_task_request_microchip_ack(data):
    print 'run_task_request_microchip_ack', data


@io.on('notify_port_change')
def handle_notify_port_change(data):
    # dat: task_id, port { port_number, status }
    task = Task.get(_id=ObjectId(data['task_id'])) # TODO Handle 404 here

    emit('run_task_if_conditions_match', json_util.dumps(task), room='daemon')


# General events

@io.on('disconnect')
def handle_disconnected():
    if request.sid == daemon_sid:
        # TODO Throw an error here
        print 'daemon disconnected'
