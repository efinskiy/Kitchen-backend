from flask import jsonify, request
from flask_login import current_user
from sqlalchemy import asc
from ...models import Customer, User
from ... import db
from ..utils import db_commit, return_kr
from ..utils import Kitchen_response as kr
from werkzeug.security import generate_password_hash
from hashlib import pbkdf2_hmac
from datetime import datetime


def get_users():
    users_list = User.query.order_by(asc(User.id)).all()

    users_tuple = []

    for user in users_list:
        users_tuple.append({
            'id': user.id,
            'login': user.login,
            'is_kitchen': user.is_kitchen,
            'is_admin': user.is_admin
        })
    
    return jsonify({
        'users': users_tuple
    })

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
                'response': 200,
                'id': u.id
            })
        else:
            return jsonify(return_kr(kr.PARSE_ERROR)), 400
    except:
        return jsonify(return_kr(kr.PARSE_ERROR)), 400






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
        return jsonify(return_kr(kr.PARSE_ERROR)), 400

    if c:= Customer.query.get(customer):
        salt = bytes(int(datetime.now().timestamp()))
        key = pbkdf2_hmac('sha256', bytes(c.id), salt, 1).hex()
        c.recoveryLink = key
        db_commit(c)
        return jsonify(
            {
                'key': key
            }
        )
    else:
        return jsonify(return_kr(kr.EMPTY)), 400

def changePassword():
    try:
        currentPassword = request.json['currentPassword']
        newPassword = request.json['newPassword']
    except:
        return jsonify(return_kr(kr.PARSE_ERROR)), 400
    
    user = User.query.get(current_user.id)

    if not user.verify_password(currentPassword):
        return jsonify(return_kr(kr.BAD_PASSWORD)), 400
    else:
        user.password = generate_password_hash(newPassword)

    db_commit(user)

    return jsonify({
        'response': 200
    })

def editUser():
    try:
        user = int(request.json['user'])
        is_admin = bool(request.json['is_admin'])
        is_kitchen = bool(request.json['is_kitchen'])
        if 'newPassword' in request.json: newPassword = request.json['newPassword']
    except:
        return jsonify(return_kr(kr.PARSE_ERROR)), 400

    user = User.query.get(user)

    if not user:
        return jsonify(return_kr(kr.EMPTY)), 400

    if is_admin:
        user.is_admin = True
        user.is_kitchen = False
    elif is_kitchen:
        user.is_admin = False
        user.is_kitchen = True
    
    if 'newPassword' in request.json:
        user.password = generate_password_hash(newPassword)

    db_commit(user)

    return jsonify({
        'response': 200
    })
        


def deleteUser():
    try:
        userId = int(request.json['id'])
    except:
        return return_kr(kr.PARSE_ERROR), 400

    if not (deletingUser:= User.query.get(userId)):
        return return_kr(kr.EMPTY), 400
    
    if deletingUser.is_admin == True:
        allAdmin = User.query.filter_by(is_admin = True).all()
        if len(allAdmin) == 1:
            return jsonify({
                'response': 999
            })
    
    db.session.delete(deletingUser)
    db.session.commit()

    return jsonify({
        'response': 200
    })