import base64, hashlib, os
import simplejson as json
from flask import current_app, url_for, render_template, Markup
from multiprocessing import Pool

from .ssh import SshClient

# th 节点处理专用共享库

sshClient = SshClient()

def _execCmdToAHost(jsonStr, asRoot=False):
    jo = json.loads(jsonStr)
    resultStr = ""
    if asRoot:
        resultStr = sshClient.execCmdRoot(jo['host'], jo['username'], jo['password'], jo['cmd'])
    else:
        resultStr = sshClient.execCmdCurrUser(jo['host'], jo['username'], jo['password'], jo['cmd'])
    return {resultStr:resultStr}

# 作为子进程执行函数，一个字符串参数方便传参数
def _scpFToAHost(jsonStr):
    jo = json.loads(jsonStr)
    resultStr = sshClient.scpFileToAHost(\
        jo['username'], jo['host'], jo['password'], jo['srcResDir'], jo['destResDir'])
    return {resultStr:resultStr}

def _scpDirOrFile(hosts, dict1):
    po=Pool(len(hosts))
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)
        po.apply_async(_scpFToAHost, args=(jsonStr,))
    po.close() 
    po.join()

def execCmd(hosts, dict1, cmdStr, asRoot=True):
    retStrP = ""
    def cb(retStr):
        global retStrP
        retStrP = retStrP + retStr[0:1000]
    dict1['cmd']=cmdStr
    po=Pool(len(hosts))
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)
        po.apply_async(_execCmdToAHost, args=(jsonStr,asRoot), callback=cb)
    po.close() 
    po.join() 
    retStr = "%s --crun.py execCmd %s -- complete" % (retStrP, cmdStr)
    print(retStr)
    return retStr

def scpDir(hosts, dict1, parentDir, DirName):
    execCmd(hosts, dict1, '/bin/rm -rf '+ parentDir + DirName)
    dict1['srcResDir'] = parentDir + DirName
    dict1['destResDir'] = parentDir
    _scpDirOrFile(hosts, dict1)
    print("-- scpDir -- complete")

def scpFile(hosts, dict1, DirPath, filename):
    execCmd(hosts, dict1, '/bin/rm -rf ' + DirPath + filename)
    dict1['srcResDir']= DirPath + filename
    dict1['destResDir']= DirPath + filename
    _scpDirOrFile(hosts, dict1)
    print("-- scpFile -- complete")
