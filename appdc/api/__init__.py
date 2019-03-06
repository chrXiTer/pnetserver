#coding:utf-8
from flask import Blueprint
api = Blueprint("api", __name__)

from flask import request, jsonify, current_app
from flask_cors import cross_origin
from appdc.includes.flask_jwt import jwt_required
from appdc.models.user import User

def message(status, value, msg=""):
    return {"status": status, "value": value, "msg": msg}

actionAuthType = {
    "login": 'noAuth', 
    "register": 'noAuth'
}

class Dispatcher(object):
    def __init__(self):
        self._funcs = {}

    def action(self, name):
        def decorate(fn):
            if name in self._funcs:
                raise ValueError("action is exists")
            self._funcs[name] = fn
            return fn
        return decorate

    def dispatch(self, name, params):   # 根据name找到处理器，并调用得到结果
        func = self._funcs.get(name)
        if not func:
            return message("error", "", "not exists action")
        authType = actionAuthType.get(name)
        if authType == 'noAuth':
            return func(**params)
        else:
            func = jwt_required()(func)
            return func(**params)

dispatcher = Dispatcher()

@api.route("/<path:action>", methods=["GET", "POST"])
@cross_origin()
def index(action):
    params = request.values.to_dict()
    resultObj = dispatcher.dispatch(action, params)
    print("\n********\n"); print(str(resultObj)); print(type(resultObj))
    return resultObj

import appdc.api.ssh_th
import appdc.api.userAuth
