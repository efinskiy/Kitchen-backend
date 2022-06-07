from unicodedata import category
from webbrowser import get

from sqlalchemy import asc
from ...models import Category
from ... import db
from flask import jsonify, request, current_app
from ..utils import return_kr, db_commit, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr


# TODO: Need QA.
def category_create():
    new_category = Category()
    # current_app.logger.info('8str')
    try:
        if 'title' in request.json: new_category.title = request.json['title']
        else: return jsonify(return_kr(kr.PARSE_ERROR)), 400
        
        if 'icon' in request.json: new_category.icon = request.json['icon']
        
        if 'visible' in request.json: new_category.visible = bool((request.json['visible']))
        else: new_category.visible = True

        if 'priority' in request.json: new_category.priority = int(request.json['priority'])
        else: new_category.priority = 2
    except:
        return jsonify(return_kr(kr.PARSE_ERROR)), 400

    new_category = db_commit(new_category)

    return jsonify({
        'code': 200,
        'id': new_category.id
    })

def category_list():
    categories = serialize_query_w0_dumps(Category.query.filter_by(is_system = False).order_by(asc(Category.priority), asc(Category.id)).all())

    return jsonify({'categories': categories})

def patchCategory():
    try:
        category_id = int(request.json['id'])
        title = request.json['title']
        priority = int(request.json['priority'])
        visible = bool(request.json['visible'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR)), 400

    if not (category:=Category.query.get(category_id)):
        return jsonify(return_kr(kr.EMPTY)), 400
    
    category.title = title
    category.priority = priority
    category.visible = visible

    db_commit(category)

    return jsonify({
        'code': 200
    })

def categoryDelete():
    try:
        category_id = int(request.json['id'])
        transferId = int(request.json['transferId'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR)), 400

    if not (category:=Category.query.get(category_id)):
        return jsonify(return_kr(kr.EMPTY)), 400
    
    if not (transferCategory:=Category.query.get(transferId)):
        return jsonify(return_kr(kr.EMPTY)), 400

    transferableProducts = category.products

    for product in transferableProducts:
        product.category_id = transferCategory.id
        db.session.add(product)
    db.session.commit()

    db.session.delete(category)
    db.session.commit()

    return jsonify({
        'code': 200
    })
