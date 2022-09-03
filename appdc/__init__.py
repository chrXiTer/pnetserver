import os
from flask import Flask, redirect, url_for, request, current_app
from flask_bootstrap import Bootstrap
#from sqlalchemy import *
bootstrap = Bootstrap()

from appdc.config_default import Config as defaultConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(defaultConfig)
    bootstrap.init_app(app)
    app.site = {}
    def site_context_processor():
        return dict(site=app.site)
    app.context_processor(site_context_processor)
    
    create_path(app)
    loadConfigCustom(app)

    @app.before_request
    def _request_check_start():
        request_check_start(app)

    from appdc.web import web
    from appdc.api import api
    from appdc.log  import init_logging

    from appdc.api.userAuth import init as userAuthInit
    userAuthInit(app)

    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix="/api")
    init_logging(app)
    return app



def exist_config(app):
    filename = "{}/config.py".format(app.root_path)
    return os.path.exists(filename)


def loadConfigCustom(app):
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

def create_path(app):  # 创建系统运行中需要使用的目录
    paths, config = [], app.config
    log_path, _ = os.path.split(config["ERROR_LOG"])
    paths.append(os.path.join(app.root_path, log_path))

    paths.append(os.path.join(app.static_folder, config["AVATAR_PATH"]))
    paths.append(os.path.join(app.static_folder, config["TMP_PATH"]))
    paths.append(os.path.join(app.static_folder, config["IMAGE_PATH"]))
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

def request_check_start(app):
    if app.start: # 在start模块中设置
        return
'''
    ends = frozenset(["admin.setup", "admin.install", "static"])
    if request.endpoint in ends:
        return
    if not exist_config(app):
        return redirect(url_for("admin.setup"))
    return redirect(url_for("admin.install"))

  #########################

    def create_config(username, password, host, db):
        data = render_template("admin/start/config.html", username=username,
            password=password, host=host, db = db)
        filename = '{}/config.py'.format(current_app.root_path)
        fd = open(filename, "w")
        fd.write(data)
        fd.close()

    def connect_mysql(url):
        """1049 => 数据库不存在
        2005 => 主机地址错误
        1045 => 用户名密码错误"""
        try:
            engine = create_engine(url)
            connection = engine.connect()
        except Exception as e:
            code, _ = e.orig
            return code
        return 0

    def create_tables(db):
        db.create_all()


    def exist_table(app):
        url = app.config["SQLALCHEMY_DATABASE_URI"]
        return _exist_table(url)


    def _exist_table(url):
        from app.models.site import SiteMeta
        engine = create_engine(url)
        if engine.dialect.has_table(engine, SiteMeta.__tablename__):
            return True
        return False


    def set_site(app):
        from app.models.site import SiteMeta
        metas = SiteMeta.all()
        metas = dict([(meta.name, meta.value) for meta in metas])
        app.site = metas


    def load_site(app):
        with app.app_context():
            set_site(app)
            def site_context_processor():
                return dict(site=app.site)
            app.context_processor(site_context_processor)
'''

