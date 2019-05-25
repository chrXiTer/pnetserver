#coding: utf-8
from datetime import datetime

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from appdc.models.model import db
from cxshare import file 
import cxshare.dbTool as dbTool
from werkzeug.security import safe_str_cmp
import uuid

def __getDBConn(app):
    host = app.config["DBHost"]
    DBUser = app.config["DBUser"]
    DBPassword = app.config["DBPassword"]
    DBName = app.config["DBName"]
    conn = dbTool.getDBConnect(host, DBUser, DBPassword, DBName)
    return conn

class User():
    id =        0
    account =   ""
    username =  ""
    phone =     ""
    email =     ""
    password =  ""
    nickname =  ""
    userface =  "resource/image/avatar/default"
    usertype =   3
    status =   1

    def __init__(self, initInfoDic):
        self.id = initInfoDic["id"] or self.id
        self.account = ""
        self.phone = initInfoDic["phone"] or self.phone
        self.email = initInfoDic["email"] or self.email
        self.username = initInfoDic["username"] or self.account
        self.password = initInfoDic["password"] or self.password
        self.nickname = initInfoDic["nickname"] or self.nickname 
        self.userface = initInfoDic["userface"] or self.userface
        self.usertype = initInfoDic["usertype"] or self.usertype
        self.status = initInfoDic["usertype"] or self.status

    @staticmethod
    def initUserAuth(app):
        conn = __getDBConn(app)
        dbTool.execSqlFile(conn, "{}/staticp/rbac.sql".format(app.root_path))

    @staticmethod
    def getUserById(userId):
        #return User.query.filter_by(id=id).first()
        conn = __getDBConn(current_app)
        sql = "select id, userName, password From ua_user where id = %s" % userId
        user = dbTool.selectOne(conn, sql)
        return user

    @staticmethod
    def getUserByName(userName):
        conn = __getDBConn(current_app)
        sql = "select id, username, password From ua_user where username = %s" % userName
        user = dbTool.selectOne(conn, sql)
        return user

    @staticmethod
    def getUserByEmail(email):
        conn = __getDBConn(current_app)
        sql = "select id, userName, password From ua_user where email = %s" % email
        user = dbTool.selectOne(conn, sql)
        return user

    @staticmethod
    def getUserByPhone(phone):
        conn = __getDBConn(current_app)
        sql = "select id, userName, password From ua_user where phone = %s" % phone
        userDBDic = dbTool.selectOne(conn, sql)
        user = User(userDBDic)
        return user

    @staticmethod
    def saveUser(user):
        conn = __getDBConn(current_app)
        email = None if(user.email == '') else user.email
        phone = None if(user.phone == '') else user.phone
        if(user.id == 0): #新增加用户
            if user.account == "":
                user.account == str(uuid.uuid1())
            if user.username == "":
                user.username = user.account
        argList = [user.id, user.account, user.username, email, phone,
            user.password, user.nickname, user.userface, user.usertype, user.status]
        argList2 = ['`%s`' if x != None else '`null`' for x in argList]
        ",".join(argList2)
        if(user.id == 0): #新增加用户
            strToUpdate = '%s, %s, %s, %s, %s, %s, %s' % (user.name, user.password, user.showname, 
                user.email, user.phone, user.userface, user.enabled)
            sql = 'replace into ua_user(account, username, email, phone, password, nickname, userface, usertype, status) values(%s)' % strToUpdate
        else:
            strToUpdate = '%s, %s, %s, %s, %s, %s, %s, %s' % (user.id, user.name, user.password, user.showname, 
                user.email, user.phone, user.userface, user.enabled)
            sql = 'replace into ua_user(id, account, username, email, phone, password, nickname, userface, usertype, status) values(%s)' % strToUpdate
        dbTool.execUpdate(conn, sql)

    @staticmethod
    def authenticate(username, password):
        user = User.getUserByName(username)
        if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
            return user

    def change_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)






'''
class User(db.Model):
    """ user table """
    db.PREFIX = current_app.config["DB_PREFIX"]
    __tablename__ = db.PREFIX + "user"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
    id =        db.Column(db.Integer, primary_key = True, nullable=False)
    name =      db.Column(db.String(255), unique=True, nullable=False, index=True, default="")
    password =  db.Column(db.String(255), default="")
    showname =  db.Column(db.String(255), nullable = False, default="")
    phone =     db.Column(db.String(255), default="")
    email =     db.Column(db.String(255), default="")
    userface =  db.Column(db.String(255),  default="")
    enabled =   db.Column(db.String(255), default=1)

    @staticmethod
    def add(username, password):
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return
        user = User()
        user.username = username
        user.password = generate_password_hash(password)
        #user.avatar = file.new_avatar()
        db.session.add(user)
        db.session.commit()
        return user
'''