from flask import Blueprint, current_app, jsonify, request, session
from flask_login import current_user
import json
from .. import sock
from flask_socketio import emit, join_room, leave_room, send

@sock.on('connect')
def connected(message):
    room = 'admin'
    current_app.logger.info(f'''{request.headers['X-Real-Ip']} Connected''')
    join_room(room)
    emit('connectConfirm', {'msg': 'ok'}, room=room)

@sock.on('info')
def echo_info(message):
    room = 'admin'
    current_app.logger.info(f'''{request.headers['X-Real-Ip']} echo_info''')
    current_app.logger.info(request.event['message'])
    current_app.logger.info(request.event['args'])
    emit('connectConfirm', {'msg': 'ok'}, room=room)


