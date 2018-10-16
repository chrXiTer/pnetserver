# coding: utf-8

# 在th节点执行通过 ssh 执行相关命令


import base64, hashlib, os
import simplejson as json
from flask import current_app, url_for, render_template, Markup

from . import dispatcher, message

from appdc.includes.ssh import SshClient

sshClient = SshClient()

@dispatcher.action("scpFileToHosts")
def scpFileToHosts(jsonStr):
    jo = json.loads(jsonStr)
    resultStrs = []
    for host in jo['hosts']:
        resultStrTmp = sshClient.scpFileToAHost(\
            jo['username'], host, jo['password'], jo['srcResDir'], jo['destResDir'])
        resultStrs.append(resultStrTmp)
    resultStr = ''.join(resultStrs)
    return {resultStr:resultStr}

def execCmdToHosts(jsonStr, asRoot=False):
    jo = json.loads(jsonStr)
    resultStrs = []
    for host in jo['hosts']:
        resultStrTmp = sshClient.execCmd(host, jo['username'], jo['password'], jo['cmd'], asRoot)
        resultStrs.append(resultStrTmp)
    resultStr = ''.join(resultStrs)
    return {resultStr:resultStr}

def execCmdToAHost(jsonStr, asRoot=False):
    jo = json.loads(jsonStr)
    resultStr = sshClient.execCmd(jo['host'], jo['username'], jo['password'], jo['cmd'], asRoot)
    return {resultStr:resultStr}

@dispatcher.action("scpFileToAHost")
def scpFileToAHost(jsonStr):
    jo = json.loads(jsonStr)
    resultStr = sshClient.scpFileToAHost(\
        jo['username'], jo['host'], jo['password'], jo['srcResDir'], jo['destResDir'])
    return {resultStr:resultStr}

@dispatcher.action("installDebInADir")
def installDebInADir(jsonStr):
    jo = json.loads(jsonStr)
    sshObj = sshClient.sshLogin(jo['host'], jo['username'], jo['password'])
    resultStr = sshClient.sudo_i(sshObj, jo['password'], jo['host'])
    resultStr2 = sshClient.installDebInADir(sshObj, jo['dirPath'])
    return resultStr + "\n--**--\n" + resultStr2

