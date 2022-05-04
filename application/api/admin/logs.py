from ...models import Logging
from flask import current_app, request, jsonify
from ..utils import return_kr, serialize_query, serialize_query_w0_dumps
from ..wrappers import is_admin
from ..utils import Kitchen_response as kr


def log_get():
    if 'hash' in request.json:
        error = Logging.query.filter_by(hash=request.json['hash']).all()
        return jsonify({
            'error': serialize_query_w0_dumps(error)
        })
    elif 'code' in request.json:
        errors = Logging.query.filter_by(error=request.json['code'])
        # current_app.logger.info(q for q in serialize_query_w0_dumps(errors))

        errs = {}
        i=0
        for error in errors:
            errs[i] = error.as_dict()
            i+=1

        return jsonify({
            'errors': errs
        })
    else:
        return jsonify(return_kr(kr.PARSE_ERROR))

def get_ip():
    return jsonify({
        'ip': request.headers['X-Real-Ip']
    })