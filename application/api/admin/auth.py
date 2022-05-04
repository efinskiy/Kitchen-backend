from ... import db
from ...models import User
from flask import jsonify, request
from flask_login import current_user, login_user, logout_user
from ..utils import return_kr
from ..utils import Kitchen_response as kr

def login():
    if current_user.is_authenticated:
        return jsonify(return_kr(kr.AUTH_YET))
    try:
        if 'login' in request.json and 'password' in request.json:
            login = request.json['login']
            password = request.json['password']
        else:
            return jsonify(return_kr(kr.PARSE_ERROR))
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    if u:=User.query.filter_by(login=login).first():
        if u.verify_password(password):
            login_user(u, remember=True)
            return jsonify(return_kr(kr.AUTH_SUCCESS))
        else:
            return jsonify(return_kr(kr.BAD_PASSWORD))
    else:
        return jsonify(return_kr(kr.BAD_PASSWORD))

def logout():
    logout_user()
    return jsonify(return_kr(kr.DEAUTH_SUCCESS))
