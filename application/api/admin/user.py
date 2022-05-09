from flask import jsonify, request
from flask_login import current_user
from ...models import Customer, User, RecoveryLink
from ..utils import db_commit, return_kr
from ..utils import Kitchen_response as kr
from werkzeug.security import generate_password_hash
from hashlib import pbkdf2_hmac
from datetime import datetime

def new_user():
    try:
        if (
            'login' in request.json and 
            'password' in request.json and 
            'is_admin' in request.json and
            'is_kitchen' in request.json
            ):
            u = User(
                login=request.json['login'],
                password=generate_password_hash(request.json['password']),
                is_kitchen=bool(int(request.json['is_kitchen'])),
                is_admin=bool(int(request.json['is_admin']))
                )
            u = db_commit(u)
            return jsonify({
                'code': 'success',
                'id': u.id
            })
        else:
            return jsonify(return_kr(kr.PARSE_ERROR))
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))






def whoami():
    try:
        return jsonify({
            'is_anonymous': current_user.is_anonymous,
            'user': current_user.login,
            'is_kitchen': current_user.is_kitchen,
            'is_admin': current_user.is_admin
        })
    except:
        return jsonify({
            'is_anonymous': current_user.is_anonymous
        })

def createRecoveryLink():
    try:
        customer = int(request.json['c'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    if c:= Customer.query.get(customer):
        salt = bytes(int(datetime.now().timestamp()))
        key = pbkdf2_hmac('sha256', bytes(c.id), salt, 10).hex()
        new = RecoveryLink(
            customer = c.id,
            created_by = current_user.id,
            is_used = False,
            link = key
        )
        db_commit(new)
        return jsonify(
            {
                'key': key
            }
        )
    else:
        return jsonify(return_kr(kr.EMPTY))
