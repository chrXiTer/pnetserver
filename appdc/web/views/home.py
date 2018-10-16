#coding: utf-8
import os
from flask import send_from_directory, current_app, request, redirect, url_for, abort
from appdc.web import web

def sendStaticFile(fileName, mimetype=None):
    dir = os.path.join(current_app.root_path, 'static')
    return send_from_directory(dir, fileName, mimetype=mimetype)

@web.route("/")
def index():
    return sendStaticFile('index.html')

@web.route("/static/<path:action>", methods=["GET"])
def index2(action):
    return sendStaticFile(action)

@web.route('/favicon.ico')
def favicon():
    return sendStaticFile('favicon.ico', 'image/vnd.microsoft.icon')

@web.route("/book/<int:id>")
@web.route("/book/<int:id>-<int:catalog_id>")
def reader(id, catalog_id=None):
    return "-web/index:" + id + ":" + catalog_id