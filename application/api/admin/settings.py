from flask_login import current_user
from ...models import Settings
from flask import request, jsonify
from ..utils import return_kr, serialize_query, db_commit, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr


# QA - OK

def settingsGet():
    q = serialize_query_w0_dumps(Settings.query.all())
    if not q:
        return jsonify({'settings': []})

    
    settings = {}
    for setting in q:
        settings[setting['key']] = {
         'id': setting['id'],
         'key': setting['key'],
         'value': setting['value']   
        }
    return jsonify({
        'settings': settings
        })

def statusGet():
    if q:=Settings.query.filter_by(key='kitchenStatus').first():
        if not current_user.is_anonymous:
            return jsonify({
                'key': 'kitchenStatus',
                'value': 'available'
            })
        return jsonify(q.as_dict())
    else:
        return jsonify({
            'key': 'kitchenStatus',
            'value': 'not_available'
        })

def settingsSet():
    try:
        key = request.json['key']
        new_value = request.json['value']
    except:
        return return_kr(kr.PARSE_ERROR)

    settingsQuery = Settings.query.filter_by(key=key).first()
    settingsQuery.value = new_value

    db_commit(settingsQuery)

    return jsonify({'code': 200})

def settingsNew():
    try:
        key = request.json['key']
        value = request.json['value']
    except:
        return return_kr(kr.PARSE_ERROR)

    newSettings = Settings(key=key, value=value)

    db_commit(newSettings)

    return jsonify({'code': 200})
