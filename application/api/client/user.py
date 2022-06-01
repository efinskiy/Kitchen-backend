# from tkinter import N
import json
from flask_login import current_user
from sqlalchemy import null
from ...models import Customer
from ..utils import return_kr, db_commit, email_sendRecovery
from ..utils import Kitchen_response as kr
from flask import jsonify, redirect, session, request
from hashlib import pbkdf2_hmac
from datetime import datetime
# RecoveryLink

def return_userid():
    return jsonify({'uid': int(session['customer'])})

def returnInfo():
    u = Customer.query.filter_by(id=session['customer']).first()

    return jsonify({
        'name': u.name,
        'email': u.email
    })

def returnKey():
    u = Customer.query.filter_by(id=session['customer']).first()

    if u.recoveryLink == None:
        salt = bytes(int(datetime.now().timestamp()))
        key = pbkdf2_hmac('sha256', bytes(u.id), salt, 1).hex()
        u.recoveryLink = key
        db_commit(u)
        return jsonify(
            {
                'key': key
            }
        )
    else:
        return jsonify(
            {
                'key': u.recoveryLink
            })

def recovery():
    if 'key' in request.args:
        key = request.args['key']
    else:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    if rl:= Customer.query.filter_by(recoveryLink=key).first():

        session['customer'] = rl.id
        return redirect('/')
    else:
        return jsonify(return_kr(kr.EMPTY))

def updateInfo():
    try:
        name = request.json['name']
        email = request.json['email']
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    customer = Customer.query.get(int(session['customer']))

    if customer.email != email:
        email_sendRecovery(email, customer.recoveryLink)

    customer.email = email
    customer.name = name

    db_commit(customer)

    return jsonify({'code': 'success'})
    

