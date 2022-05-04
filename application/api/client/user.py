from ..utils import return_response, return_not_json
from ..utils import Kitchen_response as kr
from flask import jsonify, session


def return_userid():
    return jsonify({'uid': int(session['customer'])})
