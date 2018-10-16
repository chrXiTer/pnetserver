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
        sshObj = pxssh.pxssh(timeout=300,options={
                    "StrictHostKeyChecking": "no",
                    "UserKnownHostsFile": "/dev/null"})
        sshObj.login(host, username, password)
        return sshObj

    def execCmdRoot(self, host, username, password, cmd=''):
        try:
            print('---execCmdRoot-11---%s' % host)
            sshObj = self.sshLogin(host, username, password)
            self.sudo_i(sshObj, password, host)
            sshObj.sendline(cmd)
            for i in range(0, 18):
                ret = sshObj.prompt(10)
                print("--execCmdRoot --exec--%d--%s--%s" % (i, str(ret), host))
                if ret == True:
                    break
                sshObj.sendline('')
            #print(str(sshObj.before))
            #print(str(sshObj.buffer))
            #print(str(sshObj.after))
        except Exception as e:
            print('--execCmdRoot--error-- %s' % str(e))
        print('--execCmdRoot--ok--')

    def execCmd(self, host, username, password, cmd='', asRoot=False):
        if asRoot:
            return self.execCmdRoot(host, username, password, cmd)
        try:
            ssh = pxssh.spawn('ssh %s@%s %s' % (username, host, cmd), timeout=300)
            i = ssh.expect(['[P|p]assword:', 'continue connecting'])   
            if i == 0:                                              
                ssh.sendline(password)                                 
            elif i == 1:                                               
                ssh.sendline('yes')                              
                ssh.expect('[P|p]assword:')                            
                ssh.sendline(password)
            if cmd == '':                                             
                ssh.waitnoecho()                                       
            else:                                                     
                ssh.expect(pxssh.EOF)
            print('--execCmd--**--')
        except Exception as e:
            print('--execCmd-error- %s %s %s' % (host, cmd, str(e)))
        print('--execCmd-ok- %s "%s"' % (host, cmd))
        return '--execCmd-ok- %s "%s"' % (host, cmd)

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

