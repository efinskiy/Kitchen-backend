from ..utils import return_response, return_kr, serialize_query, db_commit, return_not_json, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr
from sqlalchemy import asc

from flask import jsonify, session, request
from ...models import Basket, Menu, Customer
from ... import db

# @api.route('/api/v1/basket', methods=['GET'])
def getBasket():
    try: 
        basketUserId = int(session['customer'])
    except: 
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    db_items = serialize_query_w0_dumps(Basket.query.filter_by(cust_id=basketUserId).order_by(asc(Basket.id)).all())
    basket = {
        'items': [],
        'len': 0,
        'total': 0
        }
    blen = 0
    btotal = 0

    for item in db_items:
        i = Menu.query.get(item["item"])
        btotal += i.price * item['amount']
        blen += item['amount']
        basket['items'].append({
            'amount': item['amount'],
            'name': i.name,
            'img': i.img,
            'itemid': i.id,
            'price': i.price
        })

    basket['len'] = blen
    basket['total'] = round(btotal, 2)

    return jsonify(basket)

def getBalance():
    try:
        product = int(request.json['p'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))  

    if i:= Menu.query.filter_by(id=product).first():
        return jsonify({
            'amount': i.balance
        })
    else:
        return jsonify(return_kr(kr.EMPTY))

def patchBasket():
    try:
        basketUserId = int(session['customer'])
        product = int(request.json['p'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    if customerBasketProduct:=Basket.query.filter_by(cust_id=basketUserId, item=product).first():
        if customerBasketProduct.amount-1>0: 
            customerBasketProduct.amount-=1
            db_commit(customerBasketProduct)
            return jsonify({
                "new_amount" : customerBasketProduct.amount,
                "response": 200
            })
        else:
            db.session.delete(customerBasketProduct)
            db.session.commit()
            return jsonify({
                "new_amount": 0,
                "response": 200
            })
    else:
        return jsonify(return_kr(kr.EMPTY))
        


# @api.route('/api/v1/basket', methods=['POST'])
def addProductToBasket():
    try: 
        userId = int(session['customer'])
        product = int(request.json['p'])
        amount = int(request.json['amount'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    if item := Menu.query.filter_by(id=product).first(): pass
    else: return jsonify(return_kr(kr.PARSE_ERROR))

    customer = Customer.query.filter_by(id=userId).first()

    if item.balance < amount: return jsonify(return_kr(kr.NOT_ENOUGH))
    b = Basket.query.filter_by(cust_id=customer.id, item=item.id).first()
    if b:
        if (b.amount + amount) > (item.balance): return jsonify(return_kr(kr.NOT_ENOUGH))
        b.amount += amount
        db_commit(b)
        return jsonify({'new_amount': b.amount})
    else:
        b = Basket(cust_id=customer.id, item=item.id, amount=amount)
        db_commit(b)
        return jsonify({'new_amount': b.amount})


def clear():
    try:
        userId = int(session['customer'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    items = Basket.query.filter_by(cust_id = userId).all()

    for item in items: db.session.delete(item)
    db.session.commit()

    return jsonify({
        'response': 200
    })