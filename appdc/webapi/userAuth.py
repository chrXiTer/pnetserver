import json
from . import dispatcher
from appdc.models.user import User
#from flask_jwt import JWT

def identity(payload):
    userId = payload['identity']
    return User.getUserById(userId)

jwt = None
def userAuthInit(app):
    global jwt
    #jwt = JWT(app, User.authenticate, identity)

@dispatcher.action("addUser")
def addUser(jsonStr):
    jo = json.loads(jsonStr)
    newUser = User(jo)
    username = User.getUserByName(newUser.username)
    password = User.getUserByName(newUser.password)
    user = User.authenticate(username, password)
    User.saveUser(user)
    return {"code": "ok"}

@dispatcher.action("sendRegCodeToMail")
def sendRegCodeToMail(jsonStr):
    jo = json.loads(jsonStr)
    email = jo["email"]
    return {"code": "1234"}

@dispatcher.action("mailReg")
def mailReg(jsonStr):
    jo = json.loads(jsonStr)
    newUser = User(jo)
    User.saveUser(newUser)
    return {"code": "ok"}

@dispatcher.action("login")
def login():
    jwt.auth_request_callback()

@dispatcher.action("/protected")
def protected_test():
    return '%s' % "current_identity"


