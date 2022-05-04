# @api.route('/api/v1/getMenu', methods=['POST'])
from ...models import Menu
from ..utils import Kitchen_response, return_kr, serialize_query, serialize_query_w0_dumps
from flask import jsonify, request

def getMenu():
    menu = Menu.query.filter(Menu.balance > 0).all()
    return jsonify({
        "products": serialize_query_w0_dumps(menu)
    })

def getProductInfo():
    try:
        if not 'id' in request.json:
            return jsonify(return_kr(Kitchen_response.PARSE_ERROR))
    except:
        return jsonify(return_kr(Kitchen_response.PARSE_ERROR))

    if product := Menu.query.get(int(request.json['id'])):
        pass
    else: return jsonify(return_kr(Kitchen_response.EMPTY)) 

    return jsonify({
        'data': product.as_dict()
    })