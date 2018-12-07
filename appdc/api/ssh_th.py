# coding: utf-8

# 在th节点执行通过 ssh 执行相关命令

import base64, hashlib, os
import simplejson as json
from flask import current_app, url_for, render_template, Markup
from flask_cors import cross_origin
from . import dispatcher, message
from multiprocessing import Pool

import pexpect

from appdc.includes.ssh import SshClient
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

@dispatcher.action("scpDir")
@cross_origin()
def scpDir(jsonStr):
    jo = json.loads(jsonStr)
    retStr = thM.scpDir(jo['hosts'], jo['dict1'], jo['parentDir'], jo['dirName'])
    return (retStr)

@dispatcher.action("scpFile")
@cross_origin()
def scpFile(jsonStr):
    jo = json.loads(jsonStr)
    retStr = thM.scpFile(jo['hosts'], jo['dict1'], jo['dirPath'], jo['filename'])
    return (retStr)

def genSnapshot_(jo): # srcHost 生成快照并停止
    cmd = 'docker checkpoint create --checkpoint-dir=/root/tmp %s checkpoint2', jo['containerName']
    resultStr, cmdOut = thM.sshClient.execCmdRoot(jo['srcHost'], jo['username'], jo['password'], cmd) 
    return resultStr, cmdOut

def restore_(jo):
    cName = jo['containerName']
    cmd = "docker create --name %s --security-opt seccomp:unconfined alpine:3.8 \
         /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done;\n' \
         docker start --checkpoint-dir=/root/tmp --checkpoint=checkpoint2 %s" , (cName, cName)
    resultStr, cmdOut = thM.sshClient.execCmdRoot(jo['descHost'], jo['username'], jo['password'], cmd) 
    return resultStr, cmdOut


@dispatcher.action("liveMigration")
@cross_origin()
def liveMigration(jsonStr):
    jo = json.loads(jsonStr)
    ret = []
    retStr, cmdOut = genSnapshot_(jo)
    ret.append({"retStr":retStr, "out":cmdOut})

    # 复制文件
    cmd=""
    retStr, cmdOut = thM.sshClient.execCmdRoot(jo['descHost'], jo['username'], jo['password'], cmd)
    # TODO

    retStr, cmdOut = restore_(jo)
    ret.append({"retStr":retStr, "out":cmdOut})
    return json.dumps(ret)

@dispatcher.action("genSnapshot")
@cross_origin()
def genSnapshot(jsonStr):
    jo = json.loads(jsonStr)
    retStr, cmdOut = genSnapshot_(jo)
    return json.dumps({"retStr":retStr, "out":cmdOut})


@dispatcher.action("restoreSnapshot")
@cross_origin()
def restoreSnapshot(jsonStr):
    jo = json.loads(jsonStr)
    retStr, cmdOut = restore_(jo)
    return json.dumps({"retStr":retStr, "out":cmdOut})
    #ret = []
    #retStr, cmdOut = runSameContainer_(jo)
    #ret.push({"retStr":retStr, "out":out})
    #retStr, cmdOut = applySnapshot_(jo)
    #ret.push({"retStr":retStr, "out":out})
    #return json.dumps(ret)

""" def runSameContainer_(jo)
    cmd = "docker create --name %s --security-opt seccomp:unconfined alpine:3.8 \
         /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'" , jo['containerName']
    resultStr, cmdOut = thM.sshClient.execCmdRoot(jo['descHost'], jo['username'], jo['password'], cmd) 
    return resultStr, cmdOut

def applySnapshot_(jo)
    cmd = "docker start --checkpoint-dir=/root/tmp --checkpoint=checkpoint2 %s", jo['containerName']
    resultStr, cmdOut = thM.sshClient.execCmdRoot(jo['descHost'], jo['username'], jo['password'], cmd) 
 """
"""  
docker run -d --network L2onet --name loop --security-opt seccomp:unconfined alpine:3.8 \
    /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'" 
"""
         


""" 
--ip 10.0.1.13

docker run -d --network L2onet  --name looper --security-opt seccomp:unconfined alpine:3.8 \
    /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'

docker exec -it looper ip addr # 10.0.1.5
docker logs looper


docker checkpoint create --checkpoint-dir=/tmp looper checkpoint3
docker logs looper   #在131结束

scp -r ./checkpoint3 nscc@10.144.0.27:/home/nscc


docker create --network L2onet --name looper --security-opt seccomp:unconfined alpine:3.8 \
    /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'
docker start --checkpoint-dir=//home/nscc --checkpoint=checkpoint3 looper

docker logs looper  #从132开始
docker exec -it looper ip addr # 10.0.1.5

"""



