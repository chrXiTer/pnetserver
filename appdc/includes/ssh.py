import pexpect
from pexpect import pxssh, TIMEOUT
#001
class SshClient(object):
    def scpFileToAHost(self, username, host, password, srcResDir, destResDir,timeout=None):
        print("\n***12345*****")
        try:      
            cmd='scp -r {srcResDir} {username}@{host}:{destResDir} '\
                .format(srcResDir=srcResDir, username=username, host=host, destResDir=destResDir)
            child = pexpect.spawn(cmd, timeout=timeout) 
            child.expect("password:")
            child.sendline(password)     
            ret = child.read().decode()
            child.close()     
            resultStr='--scpFileToAHost-ok- %s --%s' % (host, ret)
            print(resultStr)
            print(cmd)
        except Exception as e:
            resultStr='--scpFileToAHost-error- %s --%s' % (host, str(e))
            print(resultStr)                           
        return resultStr 

    def sshLogin(self, host, username, password):
        self.checkFirst(host, username, password)
        sshObj = pxssh.pxssh(timeout=300,options={
                    "StrictHostKeyChecking": "no",
                    "UserKnownHostsFile": "/dev/null"})
        sshObj.login(host, username, password)
        return sshObj

    def sudo_i(self, sshObj, password, host):
        try:
            sshObj.sendline('sudo -i')
            #sshObj.expect('[P|p]asswrd')
            sshObj.waitnoecho()
            sshObj.sendline(password)
            ret = sshObj.expect(['~# ', TIMEOUT], timeout=20)
            if ret == 1:
                print("--sudo_i--error--11-")
            else:
                sshObj.set_unique_prompt()
        except Exception as e:
            print('--sudo_i-error- %s %s' % (host, str(e)))
        print('--sudo_i-ok- %s' % host)
    
    def _execHostCmd(self, host, sshObjRoot, cmd):
        sshObjRoot.sendline(cmd)
        retStrs = []
        for i in range(0, 2000):
            ret = sshObjRoot.prompt(15)
            retStrs.append("--execCmdRoot --exec--%d--%s--%s" % (i, str(ret), host)); print(retStrs[-1])
            if ret == True:
                break
            sshObjRoot.sendline('')
        #print(str(sshObjRoot.before))
        #print(str(sshObjRoot.buffer))
        #print(str(sshObjRoot.after))
        return "\n".join(retStrs), str(sshObjRoot.before)


    def execCmdRoot(self, host, username, password, cmd):
        retStrs = []
        cmdout = ""
        try:
            retStrs.append('---execCmdRoot-start---%s' % host); print(retStrs[-1])
            sshObj = self.sshLogin(host, username, password)
            self.sudo_i(sshObj, password, host)
            retStr2, cmdout = self._execHostCmd(host, sshObj, cmd)
            retStrs.append(retStr2) # 信息已经 print 过，不再 print
        except Exception as e:
            retStrs.append('--execCmdRoot--error-- %s' % str(e)); print(retStrs[-1])
        retStrs.append('--execCmdRoot--ok--'); print(retStrs[-1])
        #print(cmdout)
        return "\n".join(retStrs), cmdout
    
    def execCmdCurrUser(self, host, username, password, cmd):
        retStrs = []
        cmdout = ""
        try:
            retStrs.append('---execCmdCurrUser-11---%s' % host); print(retStrs[-1])
            sshObj = self.sshLogin(host, username, password)
            retStr2, cmdout = self._execHostCmd(host, sshObj, cmd)
            retStrs.append(retStr2) # 信息已经 print 过，不再 print
        except Exception as e:
            retStrs.append('--execCmdCurrUser--error-- %s' % str(e)); print(retStrs[-1])
        retStrs.append('--execCmdCurrUser--ok--'); print(retStrs[-1])
        #print(cmdout)
        return "\n".join(retStrs), cmdout

    def checkFirst(self, host, username, password):
        try:
            ssh = pxssh.spawn('ssh %s@%s' % (username, host), timeout=300)
            i = ssh.expect(['[P|p]assword:', 'continue connecting'])   
            if i == 0:                                              
                ssh.sendline(password)                                 
            elif i == 1:                                               
                ssh.sendline('yes')                              
                ssh.expect('[P|p]assword:')                            
                ssh.sendline(password)                                            
            ssh.waitnoecho()                                       
            print('--checkFirst--**--')
        except Exception as e:
            print('--checkFirst-error- %s %s' % (host, str(e)))
        print('--checkFirst-ok- %s' % host)
        return '--checkFirst-ok- %s' % host

    

