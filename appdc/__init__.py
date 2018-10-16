from flask import Flask, redirect, url_for, request
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()

def check_start(app):
    '''
    from app.includes.start import _exist_config, exist_table, load_site, create_path
    create_path(app)
    app.start = False
    if _exist_config(app):
        from app.config import Config
        app.config.from_object(Config)
        if exist_table(app):
            load_site(app)
            app.start = True
            return

    @app.before_request
    def request_check_start():
        if app.start:
            return
        ends = frozenset(["admin.setup", "admin.install", "static"])
        if request.endpoint in ends:
            return
        if not _exist_config(app):
            return redirect(url_for("admin.setup"))
        return redirect(url_for("admin.install"))
    '''

def create_app():
    app = Flask(__name__)

    from appdc.config_default import Config
    app.config.from_object(Config)

    bootstrap.init_app(app)
    
    app.site = {}
    def site_context_processor():
        return dict(site=app.site)
    app.context_processor(site_context_processor)
    check_start(app)

    from appdc.web import web
    from appdc.api import api
    from appdc.log  import init_logging
    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix="/api")
    init_logging(app)
    return app
