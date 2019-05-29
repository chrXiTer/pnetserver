import base64, hashlib, os
import simplejson as json
from flask import current_app, url_for, render_template, Markup
from multiprocessing import Pool

from cxshare.ssh import SshClient

# th 节点处理专用共享库

sshClient = SshClient()

def hostToPasswod(host):
    print(host)
    n2Str = host.split('.')[2]
    n2 = int(n2Str)
    if n2 == 0 :
        return 'nsccGZ-KD1810'
    else:
        return 'nsccGZ-KD1812'

G_username = "nscc"

retStrP = ""
def cb(retStr):
    global retStrP
    retStrP = retStrP + retStr[1][0:100]

def execToAHost(jsonStr, asRoot=False):
    jo = json.loads(jsonStr)
    resultStr = ""
    cmdOut = ""
    host = jo['host']
    password = hostToPasswod(host)
    if asRoot:
        resultStr, cmdOut = sshClient.execCmdRoot(host, G_username, password, jo['cmd'])
    else:
        resultStr, cmdOut = sshClient.execCmdCurrUser(host, G_username, password, jo['cmd'])
    return resultStr, cmdOut

def execCmd(hosts, dict1, cmdStr, asRoot=True):
    dict1['cmd']=cmdStr
    po=Pool(len(hosts))
    global retStrP
    retStrP = ""
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)  #print("\n*****3333333***\n")
        po.apply_async(execToAHost, args=(jsonStr, asRoot, ), callback=cb)
    po.close() 
    po.join() 
    retStr0 = "--crun.py execCmd %s -- complete" % cmdStr; print(retStr0)
    retStr = "%s\n%s" % (retStrP, retStr0)
    return retStr

def _scpFToAHost(jsonStr): # 作为子进程执行函数，一个字符串参数方便传参数
    jo = json.loads(jsonStr)
    host = jo['host']
    resultStr = sshClient.scpFileToAHost(\
        G_username, host, hostToPasswod(host), jo['srcResDir'], jo['destResDir'], jo['isRsync'])
    return resultStr, ""

def _scpDirOrFile(hosts, dict1, srcDir, destDir, isRsync=False):
    po=Pool(len(hosts))
    global retStrP
    retStrP = ""
    dict1['srcResDir'] = srcDir
    dict1['destResDir'] = destDir
    dict1['isRsync'] = isRsync
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)
        po.apply_async(_scpFToAHost, args=(jsonStr,), callback=cb)
    po.close() 
    po.join()
    retStr0 = "--_scpDirOrFile -- complete"; print(retStr0);print(len(hosts));print(hosts)
    retStr = "%s\n%s" % (retStrP, retStr0)
    return retStr

def scpFile(hosts, dict1, dirPath, filename):
    execCmd(hosts, dict1, '/bin/rm -rf ' + dirPath + filename)
    retStrF=''
    if os.path.isdir(dirPath + filename):
        retStrF = _scpDirOrFile(hosts, dict1, dirPath + filename, dirPath)
    else:
        retStrF = _scpDirOrFile(hosts, dict1, dirPath + filename, dirPath + filename)
    retStr0 = "-- scpFile -- complete"; print(retStr0)
    retStr = "%s\n%s" % (retStrF, retStr0)
    return retStr

def rsyncFile(hosts, dict1, dirPath, filename):
    execCmd(hosts, dict1, 'echo 111')
    retStrF=''
    if os.path.isdir(dirPath + filename):
        retStrF = _scpDirOrFile(hosts, dict1, dirPath + filename, dirPath, True)
    else:
        retStrF = _scpDirOrFile(hosts, dict1, dirPath + filename, dirPath + filename, True)
    retStr0 = "-- rsyncFile -- complete"; print(retStr0)
    retStr = "%s\n%s" % (retStrF, retStr0)
    return retStr

