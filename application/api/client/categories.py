from sqlalchemy import asc, desc
from ...models import Category
from flask import jsonify, request, current_app
from ..utils import return_kr, db_commit, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr


def get():
    categories = Category.query.filter_by(visible=True).order_by(asc(Category.priority)).all()

    # current_app.logger.info(categories.products)

    output = {'categories': []}
    for category in categories:
        if not category.avaliableOnly():
            continue
        if category.is_default == True:
            output['categories'].append({
                'id': category.id,
                'title': category.title,
                'is_default': True
            })
        else:
            output['categories'].append({
                'id': category.id,
                'title': category.title,
                'is_default': False
            })

    return jsonify(output)

    