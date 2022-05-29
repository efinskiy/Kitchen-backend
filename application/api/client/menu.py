# @api.route('/api/v1/getMenu', methods=['POST'])
from ...models import Category, Menu
from ..utils import Kitchen_response, return_kr, serialize_query, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr
from flask import jsonify, request, abort, send_from_directory, current_app
from ...models import Menu
from sqlalchemy import and_, asc, and_, desc
import os

def getMenu():
    try:
        catId = int(request.json['id'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    category = Category.query.filter_by(id=catId).first()
    if not category:
        return jsonify(return_kr(kr.PARSE_ERROR))

    # Проверка, запрашиваются ли популярные товары, если да, первые 10 
    if category.title == "Популярное":
        menu = Menu.query.filter(Menu.balance > 0).order_by(desc(Menu.sells)).all()
        # если товаров меньше 10 возвращаем все
        if len(menu)<10:
            # len(menu)-1 потому что, len возвращает кол-во начиная с 1, а срез работает по индексам начиная с 0
            menu = menu[0:len(menu)-1]
        else:
            menu = menu[0:9]
    else:
        # Возвращаем товары с балансом > 0 из запрашиваемой категории, сортируя по уменьшению id
        menu = Menu.query.filter(and_(Menu.balance > 0, Menu.category_id == catId)).order_by(asc(Menu.id)).all()

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

# Deprecated, use /api/v1/files/{img_name}
def preview_img():
    if 'p' in request.args:
        try:
            p_id = int(request.args.get('p'))
        except:
            return jsonify(return_kr(kr.PARSE_ERROR))
    else:
        return jsonify(return_kr(kr.EMPTY))
    
    if p:= Menu.query.get(p_id):
        return current_app.send_static_file(p.img)
        # return send_from_directory('product_imgs', p.img, as_attachment=False)
    else:
        return jsonify(return_kr(kr.EMPTY)) 