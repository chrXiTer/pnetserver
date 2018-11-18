# coding: utf-8

# 在th节点执行通过 ssh 执行相关命令

import base64, hashlib, os
import simplejson as json
from flask import current_app, url_for, render_template, Markup
from flask_cors import cross_origin
from . import dispatcher, message
from multiprocessing import Pool

from appdc.includes.ssh import SshClient
import appdc.includes.th as thM 

@dispatcher.action("execCmd")
@cross_origin()
def execCmd(jsonStr):
    jo = json.loads(jsonStr)
    retStr = thM.execCmd(jo['hosts'], jo['dict1'], jo['cmdStr'], asRoot=True)
    return retStr

@dispatcher.action("scpDir")
@cross_origin()
def scpDir(jsonStr):
    jo = json.loads(jsonStr)
    thM.scpDir(jo['hosts'], jo['dict1'], jo['parentDir'], jo['DirName'])

@dispatcher.action("scpFile")
@cross_origin()
def scpFile(jsonStr):
    jo = json.loads(jsonStr)
    thM.scpFile(jo['hosts'], jo['dict1'], jo['DirPath'], jo['filename'])





