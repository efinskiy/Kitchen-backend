from dataclasses import replace
from datetime import datetime as dt
import json
from sqlalchemy import desc, and_, or_
from ...models import Basket, CancelReason, Menu, Order
from ..utils import return_kr, serialize_query, db_commit, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr
from ..utils import Order_status as status
from ... import db
from flask import jsonify, session, request
from flask_login import current_user
import random

def createOrder():
    user = int(session['customer'])

    try:
        payment_type = int(request.json['ptype'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    # BACKEND-4
    try:
        totalOrders = len(Order.query.filter(
            and_(
                Order.customer_id == user,
                or_(
                    Order.status == status.not_payed,
                    Order.status == status.wait_for_confirmation,
                    Order.status == status.wait_for_recieve
                )
            )
        ).all())
        if totalOrders >= 3:
            return jsonify(return_kr(kr.ORDERS_LIMIT_REACH))
    except Exception as e:
        return jsonify({
            'exception': e
        })

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
        payment_type = payment_type,
        is_payed = True if payment_type==0 else False,
        status=0 if payment_type==1 else 1,
        date=dt.now())
    
    db_commit(new_order)
    for item in basket_items: db.session.delete(item)
    db.session.commit()

    return jsonify({'response': 200, 'oid': new_order.id})

def ordersGet():
    try:
        user = int(session['customer'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    try:
        orders = serialize_query_w0_dumps(Order.query.filter_by(customer_id = user).order_by(desc(Order.id)).all())
        for o in orders:
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
            if o['status'] in [0, 1, 3, 4]:
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
    
def orderCancel():
    try:
        orderId = int(request.json['oid'])
        userId = int(session['customer'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    cancelReason = CancelReason.query.filter_by(text="Отменен покупателем").first()
    if not (order:= Order.query.get(orderId)):
        return jsonify(return_kr(kr.EMPTY))

    if order.customer_id != userId:
        return jsonify(return_kr(kr.NOT_ENOUGH_PERMISSIONS))


    if order.status == status.wait_for_recieve:
        orderItems = json.loads(order.items.replace("'", '"'))
        for k, v in orderItems.items():
                    i = Menu.query.get(int(k))
                    i.reserved -= int(v)
                    db_commit(i)

    order.status = status.canceled
    order.cancelReason = cancelReason.id

    db_commit(order)

    return jsonify({
        'code': 200
    })

def getPaymentLink():
    try:
        orderId = int(request.args['oid'])
        userId = int(session['customer'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    if not (order:= Order.query.get(orderId)):
        return jsonify(return_kr(kr.EMPTY))
    
    if order.customer_id != userId:
        return jsonify(return_kr(kr.NOT_ENOUGH_PERMISSIONS))
    
    if order.status != status.not_payed:
        return jsonify(return_kr(kr.EXECUTION_ERROR))

    # DEV ENV ONLY!!!
    # order.status = status.wait_for_confirmation
    # order.is_payed = True
    # db_commit(order)
    # # # # # # # # # # # # # # # # # # # # 

    return jsonify({
        'url': 'https://google.com',
        'code': 200
    })
    