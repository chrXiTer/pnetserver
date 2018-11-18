#coding:utf-8
from flask import Blueprint
api = Blueprint("api", __name__)

#import appdc.api.views


from flask import request, jsonify, current_app
from flask_cors import cross_origin
from appdc.api import api

def message(status, value, msg=""):
    return {"status": status, "value": value, "msg": msg}

class Dispatcher(object):
    def __init__(self):
        self._funcs = {}

    def _action(self, name, auth):
        def decorate(fn):
            if name in self._funcs:
                raise ValueError("action is exists")
            self._funcs[name] = (fn, auth)
            return fn
        return decorate

    def auth_action(self, name):
        return self._action(name, True)

    def action(self, name):
        return self._action(name, False)

    def dispatch(self, name, params):   # 根据name找到处理器，并调用得到结果
        func = self._funcs.get(name)
        if not func:
            return message("error", "", "not exists action")
        func, auth = func
        return func(**params)

dispatcher = Dispatcher()

@api.route("/<path:action>", methods=["GET", "POST"])
@cross_origin()
def index(action):
    params = request.values.to_dict()
    resultObj = dispatcher.dispatch(action, params)
    return jsonify({"ret":resultObj})

import appdc.api.ssh_th
