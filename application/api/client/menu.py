# @api.route('/api/v1/getMenu', methods=['POST'])
from ...models import Menu
from ..utils import Kitchen_response, return_kr, serialize_query, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr
from flask import jsonify, request, abort, send_from_directory, current_app
from ...models import Menu
from sqlalchemy import asc
import os

def getMenu():
    menu = Menu.query.filter(Menu.balance > 0).order_by(asc(Menu.id)).all()
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

def preview_img():
    if 'p' in request.args:
        try:
            p_id = int(request.args.get('p'))
        except:
            return jsonify(return_kr(kr.PARSE_ERROR))
    else:
        return jsonify(return_kr(kr.EMPTY))
    
    if p:= Menu.query.get(p_id):
        return send_from_directory('product_imgs', p.img, as_attachment=False)
    else:
        return jsonify(return_kr(kr.EMPTY))