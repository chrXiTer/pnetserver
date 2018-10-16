import simplejson as json
import appdc.api.ssh_th as ssh_th
import appdc.cmd.hosts as hostsM
from multiprocessing import Pool

# 001
def scpThFile(dict1):
    po=Pool(len(hosts))
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)
        po.apply_async(ssh_th.scpFileToAHost, args=(jsonStr,))
    po.close() 
    po.join() 
    print("-- scp th -- complete")

def scpDirS(dict1, parentDir, DirName):
    execCmd(dict1, '/bin/rm -rf '+ parentDir + DirName)
    dict1['srcResDir'] = parentDir + DirName
    dict1['destResDir'] = parentDir
    jsonStr = json.dumps(dict1)
    ssh_th.scpFileToHosts(jsonStr)
    print("-- scpDirS -- complete")

def scpFileS(dict1, DirPath, filename):
    execCmd(dict1, '/bin/rm -rf ' + DirPath + filename)
    dict1['srcResDir']= DirPath + filename
    dict1['destResDir']= DirPath + filename
    jsonStr = json.dumps(dict1)
    ssh_th.scpFileToHosts(jsonStr)
    print("-- scpFileS -- complete")


def _scpDirOrFile(dict1):
    po=Pool(len(hosts))
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)
        po.apply_async(ssh_th.scpFileToAHost, args=(jsonStr,))
    po.close() 
    po.join()

def scpDir(dict1, parentDir, DirName):
    execCmd(dict1, '/bin/rm -rf '+ parentDir + DirName)
    dict1['srcResDir'] = parentDir + DirName
    dict1['destResDir'] = parentDir
    _scpDirOrFile(dict1)
    print("-- scpDir -- complete")

def scpFile(dict1, DirPath, filename):
    execCmd(dict1, '/bin/rm -rf ' + DirPath + filename)
    dict1['srcResDir']= DirPath + filename
    dict1['destResDir']= DirPath + filename
    _scpDirOrFile(dict1)
    print("-- scpFile -- complete")

def execCmd(dict1, cmdStr, asRoot=True):
    dict1['cmd']=cmdStr
    po=Pool(len(hosts))
    for i in range(0, len(hosts)):
        dict1["host"] = hosts[i]
        jsonStr = json.dumps(dict1)
        po.apply_async(ssh_th.execCmdToAHost, args=(jsonStr,asRoot))
    po.close() 
    po.join() 
    print("--crun.py execCmd %s -- complete" % cmdStr)

if __name__=='__main__':
    hosts = hostsM.hosts
    dict1 = {
        'username':'nscc',
        'host':'',
        'hosts':hosts,
        'password':'nsccGZ-KD1810',
        'srcResDir':'',
        'destResDir':'',
        'cmd':''
    }
    execCmd(dict1, '', False)  #以非root用户（登录用户）执行ssh，以可能的处理第一次登录接受key的情况

    '''k8s 开启 cadvisor
    dict1['hosts'] = hostsM.hosts_k8s
    fileToEdit='/etc/systemd/system/kubelet.service.d/10-kubeadm.conf'
    cmd1="sed -i 's/$KUBELET_EXTRA_ARGS/$KUBELET_EXTRA_ARGS --cadvisor-port=4194/g' " + fileToEdit 
    execCmd(dict1, cmd1 + ';systemctl daemon-reload; systemctl restart kubelet')
    '''
    
    #dict1['hosts'] = hostsM.hosts
    scpDir(dict1, '/home/nscc/th/', 'k8s-moni')

    

    #execCmd(dict1, 'rm -rf /home/nscc/th')
    #scpDir(dict1, 'home/nscc/', 'th')
    #scpFileS(dict1, '/home/nscc/th/tar/', 'chrx_multus:v3.1.tar.gz')
    #scpFileS(dict1, '/home/nscc/th/tar/', 'quay.io_calico_kube-controllers:v3.2.3.tar.gz')
    #execCmd(dict1, 'chown -R nscc /home/nscc/')
    #scpFile(dict1, '/home/nscc/th/', 'tar')
    #execCmd(dict1, '/home/nscc/th/sh/loadDockerImage.sh')
    #execCmd(dict1, 'service docker stop && /home/nscc/th/sh/setupSoft.sh')
    #execCmd(dict1, 'service docker stop ; /home/nscc/th/sh/setupSoft.sh && /home/nscc/th/sh/setSwap.sh && /home/nscc/th/sh/loadDockerImage.sh')
