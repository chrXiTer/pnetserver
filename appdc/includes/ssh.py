import pexpect
from pexpect import pxssh, TIMEOUT
#001
class SshClient(object):
    def scpFileToAHost(self, username, host, password, srcResDir, destResDir,timeout=None):
        try:                                                                                                  
            child = pexpect.spawn('scp -r {srcResDir} {username}@{host}:{destResDir} '\
                .format(srcResDir=srcResDir, username=username, host=host, destResDir=destResDir),
                timeout=timeout) 
            child.expect("password:")
            child.sendline(password)     
            ret = child.read().decode()
            child.close()     
            resultStr='--scpFileToAHost-ok- %s --%s' % (host, ret)
            print(resultStr)
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
            ret = sshObj.expect(['~# ', TIMEOUT], timeout=10)
            if ret == 1:
                print("--sudo_i--error--11-")
            else:
                sshObj.set_unique_prompt()
        except Exception as e:
            print('--sudo_i-error- %s %s' % (host, str(e)))
        print('--sudo_i-ok- %s' % host)
    
    def execCmd(self, sshObjRoot, cmd):
        sshObjRoot.sendline(cmd)
        for i in range(0, 18):
            ret = sshObjRoot.prompt(10)
            print("--execCmdRoot --exec--%d--%s--%s" % (i, str(ret), host))
            if ret == True:
                break
            sshObjRoot.sendline('')
        #print(str(sshObjRoot.before))
        #print(str(sshObjRoot.buffer))
        #print(str(sshObjRoot.after))

    def execCmdRoot(self, host, username, password, cmd):
        try:
            print('---execCmdRoot-11---%s' % host)
            sshObj = self.sshLogin(host, username, password)
            self.execCmd(sshObj, cmd)
        except Exception as e:
            print('--execCmdRoot--error-- %s' % str(e))
        print('--execCmdRoot--ok--')
    
    def execCmdCurrUser(self, host, username, password, cmd):
        try:
            print('---execCmdRoot-11---%s' % host)
            sshObj = self.sshLogin(host, username, password)
            self.sudo_i(sshObj, password, host)
            self.execCmd(sshObj, cmd)
        except Exception as e:
            print('--execCmdRoot--error-- %s' % str(e))
        print('--execCmdRoot--ok--')


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

    

