import random
import string
import os
from flask import current_app, jsonify, request, send_file
from ..utils import return_response, return_kr, db_commit, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr
from ...models import Menu

def product_updateAmount():
    try:
        product_id = int(request.json['id'])
        new_amount = int(request.json['amount'])
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))

    product = Menu.query.get(product_id)
    product.balance = new_amount
    db_commit(product)
    return jsonify({'status': 200, 'new_amount': product.balance})


# TODO: Проверить работоспособность этого куска дерьма, не уверен что заработает.
# TODO: Need QA.

def product_create():
    new_product = Menu()
    
    if 'name' in request.json: 
        product_name = request.json['name']
        new_product.name = product_name
    else:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    if 'price' in request.json:
        try:
            product_price = float(request.json['price'])
            new_product.price = product_price
        except:
            return jsonify(return_kr(kr.PARSE_ERROR))
    else:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    if 'category' in request.json:
        try:
            product_category = int(request.json['category'])
            new_product.category_id = product_category
        except:
            return jsonify(return_kr(kr.PARSE_ERROR))
    else:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    try:
        if 'weight' in request.json: new_product.weight = int(request.json['weight'])
        if 'img' in request.json: new_product.img = request.json['img']
        if 'balance' in request.json: new_product.balance = request.json['balance']
    except:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    new_product = db_commit(new_product)

    return jsonify({
        'status': 200,
        'id': new_product.id
    })

# TODO: Need QA
def product_patch():
    if 'id' in request.json:
        try:
            product = Menu.query.get(int(request.json['id']))
        except:
            return jsonify(return_kr(kr.PARSE_ERROR))

        if not product: return jsonify(return_kr(kr.EMPTY))
    else:
        return jsonify(return_kr(kr.PARSE_ERROR))

    # try:
    if 'name' in request.json: product.name = request.json['name']
    if 'weight' in request.json: product.weight = int(request.json['weight'])
    if 'img' in request.json: product.img = request.json['img']
    if 'price' in request.json: product.price = float(request.json['price'])
    if 'balance' in request.json: product.balance = int(request.json['balance'])
    if 'category' in request.json: product.category_id = int(request.json['category'])
    # except:
    #     return jsonify(return_kr(kr.PARSE_ERROR))

    db_commit(product)

    return jsonify({
        'status': 200,
    })
    
def product_list():
    if 'category_id' in request.json:
        try:
            products = serialize_query_w0_dumps(Menu.query.filter_by(category_id = int(request.json['category_id'])).all())
        except:
            return jsonify(return_kr(kr.PARSE_ERROR))
    else:
        return jsonify(return_kr(kr.PARSE_ERROR))

    return jsonify({
        'products': products
    })

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def loadImg():
    if 'img' not in request.files:
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    img = request.files['img']

    if img.filename == '':
        return jsonify(return_kr(kr.PARSE_ERROR))

    if allowed_file(img.filename):
        filename, extension = img.filename.rsplit('.', 1)

        filename = ''.join(random.choice(string.ascii_lowercase) for _ in range(15))

        newFilename = filename+'.'+extension

        img.save(os.path.join(current_app.static_folder, newFilename))

        return jsonify({
            'img': newFilename
        })


