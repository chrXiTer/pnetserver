#coding:utf-8
from flask_sqlalchemy import Pagination
from flask_sqlalchemy import SQLAlchemy
import flask

db = SQLAlchemy()

def paginate(query, page, per_page=20, error_out=True):
    if error_out and page < 1:
        flask.abort(404)
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    if not items and page != 1 and error_out:
        flask.abort(404)
    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = query.order_by(None).count()
    return Pagination(query, page, per_page, total, items)