# -*- coding: utf-8 -*-
from bson.json_util import loads, dumps
from flask import request

from app import io, mongo


@io.on('connected')
def handle_connection(data):
    print data, request.sid


@io.on('temperature_in')
def handle_distance(data):
    # TODO logging logic here
    print data
    io.emit('temperature_out', data)


@io.on('consult')
def handle_consult(data):
    response = False
    data = mongo.db.task.find_one_or_404({'name': data})
    print data
    if data is not None:
        response = dumps(data)

    io.emit('response', response)
