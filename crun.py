import simplejson as json
import appdc.api.ssh_th as ssh_th
import appdc.cmd.hosts as hostsM

# 001

if __name__=='__main__':
    
    dict1 = {
        'username':'nscc',
        'host':'',
        'password':'nsccGZ-KD1810',
        'srcResDir':'',
        'destResDir':'',
        'cmd':''
    }

    '''k8s 开启 cadvisor (自能执行一次)
    fileToEdit='/etc/systemd/system/kubelet.service.d/10-kubeadm.conf'
    cmd1="sed -i 's/$KUBELET_EXTRA_ARGS/$KUBELET_EXTRA_ARGS --cadvisor-port=4194/g' " + fileToEdit 
    ssh_th.execCmd(hostsM.hosts_k8s, dict1, cmd1 + ';systemctl daemon-reload; systemctl restart kubelet')
    '''
    
    #ssh_th.scpDir(hostsM.hosts, dict1, '/home/nscc/th/', 'k8s-moni')

    hosts = [host for host in hostsM.hosts_k8s if host != '10.129.48.3']
    ssh_th.execCmd(hosts, dict1,
            'kubeadm join 10.139.48.3:6443 --token 0j6p7w.tgie7rpflc9gxcor --discovery-token-ca-cert-hash sha256:2e0c39cf6e9684a673fe2d41a8bd56a98bfa3ef04c45ca4e2d827ab6eb2c1a7c'
            ) 

    #ssh_th.scpDir(hostsM.hosts, dict1, '/home/nscc/th/', 'calico-3.2.3')

    #execCmd(dict1, 'rm -rf /home/nscc/th')
    #scpDir(dict1, 'home/nscc/', 'th')
    #scpFileS(dict1, '/home/nscc/th/tar/', 'chrx_multus:v3.1.tar.gz')
    #scpFileS(dict1, '/home/nscc/th/tar/', 'quay.io_calico_kube-controllers:v3.2.3.tar.gz')
    #execCmd(dict1, 'chown -R nscc /home/nscc/')
    #scpFile(dict1, '/home/nscc/th/', 'tar')
    #execCmd(dict1, '/home/nscc/th/sh/loadDockerImage.sh')
    #execCmd(dict1, 'service docker stop && /home/nscc/th/sh/setupSoft.sh')
    #execCmd(dict1, 'service docker stop ; /home/nscc/th/sh/setupSoft.sh && /home/nscc/th/sh/setSwap.sh && /home/nscc/th/sh/loadDockerImage.sh')
