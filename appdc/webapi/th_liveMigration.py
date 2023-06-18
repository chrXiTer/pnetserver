
import json
from flask_cors import cross_origin
from multiprocessing import Pool
import appdc.includes.th as thM 

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
         




