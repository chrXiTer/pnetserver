from flask import Flask, redirect, url_for, request
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()

import appdc.includes.start as start

def create_app():
    app = Flask(__name__)
    start.loadConfigDefault(app)
    bootstrap.init_app(app)
    
    app.site = {}
    def site_context_processor():
        return dict(site=app.site)
    app.context_processor(site_context_processor)
    
    start.create_path(app)
    start.loadConfigCustom(app)

    @app.before_request
    def request_check_start():
        start.request_check_start(app)

    from appdc.web import web
    from appdc.api import api
    from appdc.log  import init_logging

    from appdc.api.userAuth import init as userAuthInit
    userAuthInit(app)

    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix="/api")
    init_logging(app)
    return app
