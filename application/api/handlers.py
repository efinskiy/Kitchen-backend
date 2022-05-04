# need for transformate to blueprint
from .utils import return_kr, log_request
from flask import session, current_app, jsonify, request
from .. import db
from ..models import Customer, Settings
from .utils import Kitchen_response as kr

def handle_bad_request(): return return_kr(reason={'error': 'Bad Request'})

def handle_method_not_allowed(): return jsonify(return_kr(kr.METHOD_NOT_ALLOWED))

def handle_500(): return jsonify(return_kr(reason={'error': 'Internal server error'}))

def handle_404(): return jsonify(return_kr(kr.NOT_FOUND))

def checkCustomer():
    if 'customer' not in session:
        customer = Customer()
        db.session.add(customer)
        db.session.commit()
        session['customer'] = str(customer.id)
        session.permanent = True
        current_app.logger.info("New user : {}".format(customer.id))
    current_app.logger.info('Request from customer : id'+ session['customer'])

    if q:=Settings.query.filter_by(key='kitchenStatus').first():
        current_app.logger.info(q.value)
        if q.value == "not_available":
            if not "/api/v1/admin" in request.path:
                return jsonify({
                'key': 'kitchenStatus',
                'value': 'not_available'
            })
    else:
        if not "/api/v1/admin" in request.path:
            return jsonify({
                'key': 'kitchenStatus',
                'value': 'not_available'
            })