import simplejson as json
from . import dispatcher, message
from appdc.models.user import User
from appdc.includes.flask_jwt import JWT, jwt_required, current_identity

def identity(payload):
    userId = payload['identity']
    return User.getUserById(userId)

jwt = None
def init(app):
    global jwt
    jwt = JWT(app, User.authenticate, identity)

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
#@jwt_required()
def protected_test():
    return '%s' % "current_identity"


