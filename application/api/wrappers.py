from functools import wraps
from .. import db
from ..models import User
from flask_login import current_user
from flask import jsonify
import werkzeug.exceptions as we

def is_admin(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return function(*args, **kwargs)
            else:
                return jsonify({
                    'error': we.Forbidden.code,
                    'desc': we.Forbidden.description
                })
        else:
            return jsonify({
                    'error': we.Forbidden.code,
                    'desc': we.Forbidden.description
                })     
    return wrapper

def is_kitchen(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.is_admin or current_user.is_kitchen:
                return function(*args, **kwargs)
            else:
                return jsonify({
                    'error': we.Forbidden.code,
                    'desc': we.Forbidden.description
                })
        else:
            return jsonify({
                    'error': we.Forbidden.code,
                    'desc': we.Forbidden.description
                })     
    return wrapper
