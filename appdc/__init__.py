import os
from flask import Flask, request, current_app
from appdc.config_default import Config as defaultConfig

def create_path(app):  # 创建运行中需要使用的目录
    paths = []
    logPath, _ = os.path.split(app.config["ERROR_LOG"])
    paths.append(os.path.join(app.root_path, logPath))
    paths.append(os.path.join(app.static_folder, app.config["AVATAR_PATH"]))
    paths.append(os.path.join(app.static_folder, app.config["TMP_PATH"]))
    paths.append(os.path.join(app.static_folder, app.config["IMAGE_PATH"]))
    for path in paths:
        if not os.path.exists(path):
            print("makedirs:{path}")
            os.makedirs(path)

def loadConfigCustom(app):
    def exist_config(app):
        filename = "{}/config.py".format(app.root_path)
        return os.path.exists(filename)
    app.start = False
    if exist_config(app):
        from appdc.config import Config
        app.config.from_object(Config)
        '''
        if start.exist_table(app):
            start.load_site(app)
            app.start = True
            return
        '''

def create_app():
    app = Flask(__name__)
    app.config.from_object(defaultConfig)
    app.site = {}
    def site_context_processor():
        return dict(site=app.site)
    app.context_processor(site_context_processor)
    
    loadConfigCustom(app)
    create_path(app)
    
    @app.before_request
    def _request_check_start():
        request_check_start(app)

    from appdc.web import web
    from appdc.webapi import webapi
    from appdc.log  import init_logging

    import appdc.webapi.userAuth as userAuth

    userAuth.userAuthInit(app)

    app.register_blueprint(web)
    app.register_blueprint(webapi, url_prefix="/api")
    init_logging(app)
    return app

def request_check_start(app):
    if app.start: # 在start模块中设置
        return
