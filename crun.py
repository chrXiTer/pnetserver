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

    #复制文件和安装docker，k8s等软件
    '''
    hosts=hostsM.hosts2
    ssh_th.scpDir(hosts, dict1, '/home/nscc/', 'th')
    cmd1='service docker stop ; /home/nscc/th/sh/setupSoft.sh && /home/nscc/th/sh/setSwap.sh && /home/nscc/th/sh/loadDockerImage.sh'
    ssh_th.execCmd(hosts, dict1, cmd1)
    '''

    # 配置docker使用试验特征、以及使用etcd存储
    '''
    hosts=hostsM.hosts_cal2
    ssh_th.execCmd(hosts, dict1, 'cp /home/nscc/th/calico-2.6.11/daemon.json /etc/docker/; systemctl daemon-reload; systemctl restart docker')
    '''

    # 运行 calico node 容器

    hosts=hostsM.hosts_cal
    ssh_th.execCmd(hosts, dict1, '/home/nscc/th/calico-2.6.11/calicoctl node run --node-image=quay.io/calico/node:v2.6.11 --config=/home/nscc/th/calico-2.6.11/calico-1.cfg')

    # 修改主机名
    '''
    for host in hostsM.hosts_cal2:
        hosts = [host]
        hostnameOld='n-%s-%s' % (host[3:5], host[10:])
        hostname='n-%s-%s' % (host[3:6], host[10:])
        ssh_th.execCmd(hosts, dict1, 'echo %s > /etc/hostname; sed -i s/%s/%s/ /etc/hosts; hostname %s' % (hostname, hostnameOld, hostname, hostname))
    ssh_th.execCmd(hostsM.hosts_cal2, dict1, '/etc/init.d/hostname.sh start')
    '''

    #k8s 开启 cadvisor (自能执行一次)
    '''
    fileToEdit='/etc/systemd/system/kubelet.service.d/10-kubeadm.conf'
    cmd1="sed -i 's/$KUBELET_EXTRA_ARGS/$KUBELET_EXTRA_ARGS --cadvisor-port=4194/g' " + fileToEdit 
    ssh_th.execCmd(hostsM.hosts_k8s2, dict1, cmd1 + ';systemctl daemon-reload; systemctl restart kubelet')
    '''
    
    # 加入集群
    '''
    hosts = [host for host in hostsM.hosts_k8s2 if host != '10.129.48.3']
    cmd1='kubeadm join 10.139.48.3:6443 --token 0j6p7w.tgie7rpflc9gxcor --discovery-token-ca-cert-hash sha256:2e0c39cf6e9684a673fe2d41a8bd56a98bfa3ef04c45ca4e2d827ab6eb2c1a7c'
    cmd2="sed -i 's/10.96.0.10/10.190.96.10/g' /var/lib/kubelet/config.yaml"
    cmd3="systemctl daemon-reload; systemctl restart kubelet"
    ssh_th.execCmd(hosts, dict1, '%s;%s;%s' % (cmd1, cmd2, cmd3))
    '''
    # 复制,某个文件夹
    #ssh_th.scpDir(hostsM.hosts, dict1, '/home/nscc/th/', 'calico-2.6.11')
    #ssh_th.scpDir(hostsM.hosts, dict1, '/home/nscc/th/', 'sh')

    #ssh_th.execCmd(hostsM.hosts, dict1, 'cd /home/nscc/th/tar.o; ls | xargs -n 1 docker image load -i')
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

