from flask import request, jsonify
from ..utils import return_kr, db_commit, serialize_query_w0_dumps
from ..utils import Kitchen_response as kr
from ...models import CancelReason

def reasons_get():
    reasons = serialize_query_w0_dumps(CancelReason.query.filter_by(isAdminReason = True).all())
    r_out = {'reasons': reasons}
    return jsonify(r_out)