from flask import current_app, jsonify, request
from ..utils import Order_status, return_response, return_kr, db_commit, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr
from ..utils import Order_status as status
from sqlalchemy import and_, desc, or_
import json

from ...models import CancelReason, Menu, Order

def getNotCompleted():
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
    
    return jsonify({
        'orders': notCompletedOrders
    })

def historyGet():
    historyOrders = serialize_query_w0_dumps(Order.query.filter(or_(Order.status == status.canceled, Order.status==status.recieved)).order_by(desc(Order.id)).all())
    for o in historyOrders:
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

    return jsonify({
        'orders': historyOrders
    })

def cancelOrder():
    try:
        orderId = int(request.json['oid'])
        reason = int(request.json['reason'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    if not (order:= Order.query.get(orderId)):
        return jsonify(return_kr(kr.EMPTY))
    
    cancelReason = CancelReason.query.get(reason)
    order.status = status.canceled
    order.cancelReason = cancelReason.id
    db_commit(order)
    return jsonify({
        'code': 200
    })

def confirmOrder():
    try:
        orderId = int(request.json['oid'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    if not (order:= Order.query.get(orderId)):
        return jsonify(return_kr(kr.EMPTY))

    if order.status > 1:
        return jsonify(return_kr(kr.EXECUTION_ERROR))
    
    order.status = status.wait_for_recieve
    
    db_commit(order)

    return jsonify({
        'code': 200
    })

def closeOrder():
    try:
        orderId = int(request.json['oid'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    if not (order:= Order.query.get(orderId)):
        return jsonify(return_kr(kr.EMPTY))

    order.status = status.recieved

    db_commit(order)

    return jsonify({
        'code': 200
    })