from datetime import datetime as dt
import json
from ...models import Basket, Order
from ..utils import return_kr, serialize_query, db_commit, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr
from ... import db
from flask import jsonify, session, request
import random

def createOrder():
    user = int(session['customer'])

    if basket_items:=Basket.query.filter_by(cust_id=user).all(): pass
    else: return jsonify(return_kr(kr.EMPTY))

    total = 0
    order_items = {}
    for position in basket_items:
        try:
            order_items[position.item] = position.amount
            total += position.amount*position.menu.price
        except:
            return jsonify(return_kr(kr.PARSE_ERROR))

    confirmation = random.randint(1000, 9999)
    new_order = Order(
        customer_id=user, 
        confirmation_code=confirmation, 
        items=json.dumps(order_items),
        ord_price=total, 
        status=0,
        date=dt.now())
    
    db_commit(new_order)
    for item in basket_items: db.session.delete(item)
    db.session.commit()

    return jsonify({'status': 200, 'oid': new_order.id})

def ordersGet():
    try:
        user = int(session['customer'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    try:
        orders = serialize_query_w0_dumps(Order.query.filter_by(customer_id = user).all())
        for o in orders:
            o["items"] = json.loads(o["items"].replace("'", '"'))
            if o['status'] == 0 or o['status'] == 2:
                o.pop('confirmation_code', None)
        return jsonify({
            "orders" : orders
        })
    except:
        return jsonify(return_kr(kr.EXECUTION_ERROR))

def orderGet():
    try:
        order_id = int(request.json['oid'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    try:
        order = Order.query.filter(Order.id==order_id).first()
        if not order: return jsonify(return_kr(kr.EMPTY))
        order_serialized = order.as_dict()
        order_serialized['items'] = json.loads(order_serialized['items'].replace("'", '"'))
        if order_serialized['status'] != 1: order_serialized.pop("confirmation_code", None)
        if order.customer_id != int(session['customer']): return jsonify(return_kr(kr.NOT_ENOUGH_PERMISSIONS))
    except:
        return jsonify(return_kr(kr.EXECUTION_ERROR))

    return jsonify(order_serialized)
    
# def confirmOrder():
    