import base64, hashlib, os
import simplejson as json
from flask import current_app, url_for, render_template, Markup
from multiprocessing import Pool

from .ssh import SshClient

# th 节点处理专用共享库

sshClient = SshClient()

retStrP = ""
def cb(retStr):
    global retStrP
    retStrP = retStrP + retStr[0:100]

def execToAHost(jsonStr, asRoot=False):
    print("\n*****444444***\n")
    jo = json.loads(jsonStr)
    resultStr = ""
    if asRoot:
        resultStr = sshClient.execCmdRoot(jo['host'], jo['username'], jo['password'], jo['cmd'])
    else:
        resultStr = sshClient.execCmdCurrUser(jo['host'], jo['username'], jo['password'], jo['cmd'])
    return resultStr

def execCmd(hosts, dict1, cmdStr, asRoot=True):
    print(str(hosts))
    print(str(dict1))
    print(str(cmdStr)) 
    dict1['cmd']=cmdStr
    po=Pool(len(hosts))
    global retStrP
    retStrP = ""
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)
        print("\n*****3333333***\n")
        po.apply_async(execToAHost, args=(jsonStr, asRoot, ), callback=cb)
    po.close() 
    po.join() 
    retStr0 = "--crun.py execCmd %s -- complete", cmdStr; print(retStr0)
    retStr = "%s\n%s" % (retStrP, retStr0)
    return retStr

def _scpFToAHost(jsonStr): # 作为子进程执行函数，一个字符串参数方便传参数
    print("\n*****111111****\n")
    jo = json.loads(jsonStr)
    resultStr = sshClient.scpFileToAHost(\
        jo['username'], jo['host'], jo['password'], jo['srcResDir'], jo['destResDir'])
    print("\n*****222222****\n")
    return resultStr

def _scpDirOrFile(hosts, dict1):
    po=Pool(len(hosts))
    global retStrP
    retStrP = ""
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)
        po.apply_async(_scpFToAHost, args=(jsonStr,), callback=cb)
    po.close() 
    po.join()
    retStr0 = "--_scpDirOrFile -- complete"; print(retStr0);print(len(hosts));print(hosts)
    retStr = "%s\n%s" % (retStrP, retStr0)
    return retStr

def scpDir(hosts, dict1, parentDir, DirName):
    execCmd(hosts, dict1, '/bin/rm -rf '+ parentDir + DirName)
    dict1['srcResDir'] = parentDir + DirName
    dict1['destResDir'] = parentDir
    retStrF = _scpDirOrFile(hosts, dict1)
    retStr0 = "-- scpDir -- complete"; print(retStr0)
    retStr = "%s\n%s" % (retStrF, retStr0)
    return retStr

def scpFile(hosts, dict1, DirPath, filename):
    execCmd(hosts, dict1, '/bin/rm -rf ' + DirPath + filename)
    dict1['srcResDir']= DirPath + filename
    dict1['destResDir']= DirPath + filename
    retStrF = _scpDirOrFile(hosts, dict1)
    retStr0 = "-- scpFile -- complete"; print(retStr0)
    retStr = "%s\n%s" % (retStrF, retStr0)
    return retStr
