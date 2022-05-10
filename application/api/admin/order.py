from flask import jsonify, request
from ..utils import return_response, return_kr, db_commit, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr
from ..utils import Order_status as status
from sqlalchemy import and_
import json

from ...models import Menu, Order

def getNotCompleted():
    notCompletedOrders = serialize_query_w0_dumps(Order.query.filter(and_(Order.status != status.not_payed, Order.status<=status.wait_for_recieve)).all())
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