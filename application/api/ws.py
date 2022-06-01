import json
from flask import Blueprint, current_app, jsonify, request, session
from flask_login import current_user
from sqlalchemy import and_, desc
from ..models import Order, Menu
from .utils import serialize_query_w0_dumps
from .utils import Order_status as status

from .. import sock
from flask_socketio import emit, join_room, leave_room, send

@sock.on('connect')
def test_connect():
    current_app.logger.info('CONNECT EVENT happened...')
    emit('success', {'data': 'Connected'})


@sock.on('fetchNotCompleted')
def fetch_all_records():
    # current_app.logger.info(current_user)
    # current_app.logger.info(f'ws.py:21 {current_user.is_admin} {current_user.is_kitchen}')
    if not current_user.is_admin and not current_user.is_kitchen:
        emit('sendingNotCompleted', {'orders': []})
    else:
        notCompletedOrders = serialize_query_w0_dumps(Order.query.filter(and_(Order.status != status.not_payed, Order.status<=status.wait_for_recieve)).order_by(desc(Order.id)).all())
        for o in notCompletedOrders:
                orderItems = json.loads(o["items"].replace("'", '"'))
                replacebleItems = []
                o['date'] = o['date'].strftime("%d/%m/%Y, %H:%M:%S")
                for k, v in orderItems.items():
                    i = Menu.query.get(int(k))
                    replacebleItems.append({
                        'id': k,
                        'title': i.name,
                        'img': i.img,
                        'amount': v,
                        'summ': round(i.price*v, 2),
                        'price': i.price
                    })
                o["items"] = replacebleItems
        emit('sendingNotCompleted', {'orders': notCompletedOrders})
