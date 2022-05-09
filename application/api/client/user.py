from ...models import RecoveryLink
from ..utils import return_kr
from ..utils import Kitchen_response as kr
from flask import jsonify, session, request
RecoveryLink

def return_userid():
    return jsonify({'uid': int(session['customer'])})

def recovery():
    if 'key' in request.args:
        key = request.args['key']
    else:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    if rl:= RecoveryLink.query.filter_by(link=key).first():
        session['customer'] = rl.customer
        return jsonify({
            "response": 200,
            "new_id": str(rl.customer)
        })
    else:
        return jsonify(return_kr(kr.EMPTY))
    

