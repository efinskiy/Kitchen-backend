import json, hashlib
from collections.abc import Iterable
from flask import Response, jsonify, request, session
from sqlalchemy import desc
from ..models import Logging
from .. import db

class Kitchen_response:
    """ERRORS\n
    1xx - `Auth` \n
    200 - `Product` \n
    300 - `Free` \n
    400 - `Database` \n
    500 - `Request` \n
    """
    class PARSE_ERROR:
        code = 500
        desc = 'Ошибка чтения данных запроса'
    
    class EXECUTION_ERROR:
        code = 501
        desc = 'Ошибка при выполнении запроса'

    class ORM_ERROR:
        code = 400
        desc = 'Ошибка выполнения запроса к БД'

    class EMPTY:
        code = 401
        desc = 'Пустой ответ от БД'

    class BAD_PASSWORD:
        code = 100
        desc = 'Неправильный логин/пароль'

    class AUTH_SUCCESS:
        code = 101
        desc = 'Авторизация прошла успешно'
    
    class AUTH_YET:
        code = 102
        desc = 'Уже авторизован'

    class DEAUTH_SUCCESS:
        code = 103
        desc = 'Выход совершен успешно'
    
    class NOT_ENOUGH_PERMISSIONS:
        code = 104
        desc = "Not enough permissions"
    
    class NOT_ENOUGH:
        code = 201
        desc = "Недостаточно товара"

    class NOT_FOUND: 
        code = 504
        desc = 'Not found'
    
    class METHOD_NOT_ALLOWED:
        code = 505
        desc = 'Method not allowed'


def return_not_json(response, code=200):
    return Response(response=json.dumps(response), status=code)

# deprecated -> use jsonify(res) 
def return_response(response, code=200):
    log_request(1)
    return jsonify(response)
    # return Response(response=json.dumps(response), status=code, mimetype='application/json')

def return_kr(reason : Kitchen_response):
    hash = log_request(0, error=reason.desc)
    return {
        'response': reason.code,
        'desc':  reason.desc,
        'hash': hash
        }

def serialize_query(items):
    if isinstance(items, Iterable):
        r = []
        for item in items:
            r.append(item.as_dict())
        return json.dumps(r)
    else:
        json.dumps(items.as_dict())

def serialize_query_w0_dumps(items):
    if isinstance(items, Iterable):
        r = []
        for item in items:
            r.append(item.as_dict())
        return r
    else:
        items.as_dict()

def db_commit(query):
    db.session.add(query)
    db.session.commit()
    return query

def verify_order(order_id, s):
    pass

def log_request(type, error=None):
    try:
        req = request.get_json()
        if req == None: req = 'No data'
    except:
        req = 'get_json() caught exception'
    hash = hashlib.md5(f'{str(request.path)} {str(request.headers)} {str(req)} {str(request.referrer)} {str(request.remote_addr)}'.encode()).hexdigest()

    match type:
        case 0:
            log = Logging(
                user_id = int(session['customer']),
                path = request.path,
                headers = str(request.headers),
                request = str(req),
                referrer = str(request.referrer),
                ip = str(request.headers['X-Real-Ip']),
                error = error,
                hash = hash
            )
        case 1:
            log = Logging(
                user_id = int(session['customer']),
                path = request.path,
                headers = str(request.headers),
                request = str(req),
                referrer = str(request.referrer),
                ip = str(request.headers['X-Real-Ip']),
                hash = hash
            )
    db_commit(log)
    return hash

