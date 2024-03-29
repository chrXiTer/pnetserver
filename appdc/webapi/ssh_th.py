# coding: utf-8

# 在th节点执行通过 ssh 执行相关命令

import os
import json
from flask_cors import cross_origin
from . import dispatcher
from multiprocessing import Pool

import pexpect
import appdc.includes.th as thM 

@dispatcher.action("execCmd")
@cross_origin()
def execCmd(jsonStr):
    jo = json.loads(jsonStr)
    retStr = thM.execCmd(jo['hosts'], jo['dict1'], jo['cmdStr'], asRoot=True)
    return (retStr)

@dispatcher.action("execCmdAHost") # 会得到前10000字符的输出值
@cross_origin()
def execCmdAHost(jsonStr):
    retStr, out = thM.execToAHost(jsonStr, asRoot=True)
    return json.dumps({"retStr":retStr, "out":out})

@dispatcher.action("execCmdLocal") # 直接在服务端本地执行命令
@cross_origin()
def execCmdLocal(jsonStr):
    jo = json.loads(jsonStr)
    cmd = jo['cmd']
    (out, retStr) = pexpect.run(cmd, withexitstatus=1)
    retStr = str(retStr)
    return json.dumps({"retStr":retStr, "out":out})

@dispatcher.action("scpFile")
@cross_origin()
def scpFile(jsonStr):
    jo = json.loads(jsonStr)
    retStr = thM.scpFile(jo['hosts'], jo['dict1'], jo['dirPath'], jo['filename'])
    return (retStr)

@dispatcher.action("rsyncFile")
@cross_origin()
def rsyncFile(jsonStr):
    jo = json.loads(jsonStr)
    retStr = thM.rsyncFile(jo['hosts'], jo['dict1'], jo['dirPath'], jo['filename'])
    return (retStr)


@dispatcher.action("listDir")
@cross_origin()
def listDir(jsonStr):
    jo = json.loads(jsonStr)
    print(jsonStr)
    path = jo["dir"]
    t = jo["t"]
    dirs = []
    if os.path.isdir(path):
        parents = os.listdir(path)
        for parent in parents:
            print(path + "/" + parent)
            dirs.append({"name":parent, "isDir": os.path.isdir(path + "/" + parent)})
    return json.dumps({"t":t, "dirs":dirs})


