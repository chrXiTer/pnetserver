#coding:utf-8
from flask import Blueprint
webapi = Blueprint("webapi", __name__)

from flask import request
from flask_cors import cross_origin

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
            return func(**params)

dispatcher = Dispatcher()

@webapi.route("/<path:action>", methods=["GET", "POST"])
@cross_origin()
def index(action):
    params = request.values.to_dict()
    resultObj = dispatcher.dispatch(action, params)
    print("\n********\n"); print(str(resultObj)); print(type(resultObj))
    return resultObj

import appdc.webapi.ssh_th
import appdc.webapi.userAuth
