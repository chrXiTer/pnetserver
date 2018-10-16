# coding: utf-8

# 在th节点执行通过 ssh 执行相关命令


import base64, hashlib, os
import simplejson as json
from flask import current_app, url_for, render_template, Markup
from . import dispatcher, message
from multiprocessing import Pool

from appdc.includes.ssh import SshClient

sshClient = SshClient()


@dispatcher.action("execCmdToAHost")
def execCmdToAHost(jsonStr, asRoot=False):
    jo = json.loads(jsonStr)
    if asRoot:
        resultStr = sshClient.execCmdRoot(jo['host'], jo['username'], jo['password'], jo['cmd'])
    else:
        resultStr = sshClient.execCmdCurrUser(jo['host'], jo['username'], jo['password'], jo['cmd'])
    return {resultStr:resultStr}

@dispatcher.action("scpFileToAHost")
def scpFileToAHost(jsonStr):
    jo = json.loads(jsonStr)
    resultStr = sshClient.scpFileToAHost(\
        jo['username'], jo['host'], jo['password'], jo['srcResDir'], jo['destResDir'])
    return {resultStr:resultStr}

def _scpDirOrFile(hosts, dict1):
    po=Pool(len(hosts))
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)
        po.apply_async(scpFileToAHost, args=(jsonStr,))
    po.close() 
    po.join()

def execCmd(hosts, dict1, cmdStr, asRoot=True):
    dict1['cmd']=cmdStr
    po=Pool(len(hosts))
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)
        po.apply_async(execCmdToAHost, args=(jsonStr,asRoot))
    po.close() 
    po.join() 
    print("--crun.py execCmd %s -- complete" % cmdStr)

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



