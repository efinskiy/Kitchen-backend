from ...models import Category
from flask import jsonify, request, current_app
from ..utils import return_kr, db_commit
from ..utils import Kitchen_response as kr


# TODO: Need QA.
def category_create():
    new_category = Category()
    # current_app.logger.info('8str')
    if 'title' in request.json:
        new_category.title = request.json['title']
    else:
        current_app.logger.info(str(return_kr(kr.PARSE_ERROR)))
        return jsonify(return_kr(kr.PARSE_ERROR))
    
    if 'icon' in request.json: new_category.icon = request.json['icon']
    
    if 'visible' in request.json: new_category.visible = bool(int((request.json)))
    else: new_category.visible = True

    new_category = db_commit(new_category)

    return jsonify({
        'status': 200,
        'id': new_category.id
    })

