#coding: utf-8
import base64, hashlib, os
import simplejson as json
from flask import current_app, url_for, render_template, Markup
import pexpect
from pexpect import pxssh
from . import dispatcher, message

myHost = "192.168.147.219"
myPassword = '123'
myUsername = 'net663'

myToLinuxDir = '/home/net663/toLinux/'
myDebDir = myToLinuxDir + 'deb/'
myBinDri = myToLinuxDir + 'bin/'
myEtcdDir = myToLinuxDir + 'bin/etcd-v3.3.5-linux-amd64/'

@dispatcher.action("scpFileToLinux")
def func1(jsonStr={}):
    username = myUsername
    hostname = myHost
    return scpFileToLinux(username, hostname)

@dispatcher.action("setRootPassword")
def func2(jsonStr={}):
    hostname = myHost
    username = myUsername
    password = myPassword
    sshObj = sshLogin(hostname, username, password)
    retStr = setRootPassword(sshObj, password, password)
    sshObj.logout()
    return retStr

@dispatcher.action("installDocker")
def func3(jsonStr={}):
    hostname = myHost
    username = myUsername
    password = myPassword
    sshObj = sshLogin(hostname, username, password)
    suRoot(sshObj, myPassword)
    installDocker(sshObj)

@dispatcher.action("installEtcd")
def func4(jsonStr={}):
    hostname = myHost
    username = myUsername
    password = myPassword
    sshObj = sshLogin(hostname, username, password)
    suRoot(sshObj, myPassword)
    installEtcd(sshObj)

@dispatcher.action("installCalico")
def func5(jsonStr={}):
    hostname = myHost
    username = myUsername
    password = myPassword
    sshObj = sshLogin(hostname, username, password)
    suRoot(sshObj, myPassword)
    installCalico(sshObj)


@dispatcher.action("ssh2")
def ssh2():
    pexpect.run("ssh net663@192.168.147.30", events={'(?!)password':myPassword})

@dispatcher.action("ssh3")
def ssh3():
     sshObj = pxssh.pxssh()
     sshObj.login(myHost, myUsername, myPassword)



def scpFileToLinux(username, hostname):  #把toLinux文件夹复制到目标机用户～目录
    resDir = os.path.join(current_app.root_path, 'static', 'toLinux')
    child = pexpect.spawn('scp -r {resDir} {username}@{hostname}:~ '\
        .format(resDir=resDir, username=username,hostname=hostname)  )
    child.expect("password:")
    child.sendline(myPassword)
    resultStr = child.read().decode() + "dd<br />dd"
    child.close()
    return resultStr


def sshLogin(hostname, username, password):
     sshObj = pxssh.pxssh()
     sshObj.login(hostname, username, password)
     return sshObj

def suRoot(sshObj, rootPassword):
    sshObj.sendline('su') 
    sshObj.expect('Password:')
    sshObj.sendline('su') 
    sshObj.sendline('whoami')
    printb("@@@222@@@", sshObj.buffer)
    return sshObj #sshObjRoot


def installDocker(sshObjRoot):
    sshObjRoot.sendline('dpkg -i ' + myDebDir + 'libltdl7_2.4.6-0.1_amd64.deb') 
    sshObjRoot.sendline('dpkg -i ' + myDebDir + 'docker-ce_18.03.1~ce-0~ubuntu_amd64.deb') 

def installEtcd(sshObjRoot):
    sshObjRoot.sendline('chmod -R +x ' + myEtcdDir)
    sshObjRoot.sendline('cp -r ' + myEtcdDir + ' /usr/local/bin/')

def installCalico(sshObjRoot):
    sshObjRoot.sendline('chmod -R +x ' + myBinDri)
    sshObjRoot.sendline('cp calicoctl' + myEtcdDir + ' /usr/local/bin/')

def setRootPassword(sshObj, password, rootPassword):
    infoStr = ""
    sshObj.sendline('sudo passwd root') 
    sshObj.expect('password for')
    printbuf("", sshObj)
    sshObj.sendline(password)
    sshObj.expect('password:')
    printbuf("", sshObj)
    sshObj.sendline(rootPassword)
    sshObj.expect('password:')
    printbuf("", sshObj)
    sshObj.sendline(rootPassword)
    sshObj.prompt()             # match the prompt
    printbuf("", sshObj)
    infoStr = infoStr + str(sshObj.before, encoding='utf-8') 
    return infoStr

def printbuf(tag, sshObj):
    printb(tag, sshObj.before, sshObj.after, sshObj.buffer)
    sshObj.buffer = b""

def printb(tag, *args):
    newargs = [str(arg, encoding='utf-8') for arg in args]
    print(tag, *newargs)
    

