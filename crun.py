
# 001

dict1 = {
    'username':'nscc',
    'host':'',
    'password':'nsccGZ-KD1810',
    'srcResDir':'',
    'destResDir':'',
    'cmd':''
}

def func_chgHostName(hosts): # 修改主机名
    for host in hosts:
        hosts2 = [host]
        hostnameOld='kickseed'
        hostname='n-%s-%s' % (host[3:6], host[9:])
        cmd1='echo %s > /etc/hostname' % hostname
        cmd2='sed -i s/%s/%s/ /etc/hosts' % (hostnameOld, hostname)
        cmd3='hostname %s' % hostname
        ssh_th.execCmd(hosts2, dict1, '%s;%s;%s' % (cmd1, cmd2, cmd3))
        #ssh_th.execCmd(hosts, dict1, '/etc/init.d/hostname.sh start')

def func_initInstallSoft_setSwap(hosts):
    cmdInstallSoft='''service docker stop;\
        cd /home/nscc/th/deb/vim-curl-unzip.deb;\
        dpkg -i --force-all -B *.deb;\
        cd /home/nscc/th/deb/docker-17.03.2.deb;\
        dpkg -i --force-all -B *.deb;\
        cd /home/nscc/th/deb/k8s-1.11.3-adm.deb;\
        dpkg -i --force-all -B *.deb'''
    cmdSetSwap="swapoff -a; sed -i '/swap/s/^/#/' /etc/fstab"
    ssh_th.execCmd(hosts, dict1, '%s && %s' % (cmdInstallSoft, cmdSetSwap))

def func_cfgDocker(hosts): # 配置docker使用试验特征、以及使用etcd存储(用于2.6.11)
    cmd='cp /home/nscc/th/calico-2.6.11/daemon.json /etc/docker/; systemctl daemon-reload; systemctl restart docker'
    ssh_th.execCmd(hosts, dict1, cmd)

def func_RunCalico2Node(): # 运行 calico node 2.6.11 容器
    hosts=hostsM.hosts_cal
    cmd='/home/nscc/th/calico-2.6.11/calicoctl node run --node-image=quay.io/calico/node:v2.6.11 --config=/home/nscc/th/calico-2.6.11/calico-1.cfg'
    ssh_th.execCmd(hosts, dict1, cmd)

def func_setK8sCadvisor(): #k8s 开启 cadvisor (自能执行一次)
    hosts=hostsM.hosts_k8s2
    fileToEdit='/etc/systemd/system/kubelet.service.d/10-kubeadm.conf'
    cmd1="sed -i 's/$KUBELET_EXTRA_ARGS/$KUBELET_EXTRA_ARGS --cadvisor-port=4194/g' " + fileToEdit 
    ssh_th.execCmd(hosts, dict1, cmd1 + ';systemctl daemon-reload; systemctl restart kubelet')

def func_resetK8s():
    hosts=hostsM.hosts_k8s
    cmd='kubeadm reset -f;rm -r $HOME/.kube;rm -r /var/etcd/calico-data;ip link delete flannel.1;ip link delete cni0'
    ssh_th.execCmd(hosts, dict1, cmd)

###################

def func_loadImage(hosts): #复制文件和安装docker，k8s等软件
    #ssh_th.scpDir(hosts, dict1, '/home/nscc/', 'th')
    cmdLoadDockerImage1='cd /home/nscc/th/tar && ls | xargs -n 1 docker load -i'
    #cmdLoadDockerImage2='cd /home/nscc/th/tar.o && ls | xargs -n 1 docker load -i'
    cmdLoadDockerImage2='docker load -i /home/nscc/th/tar.o/gcr.io_google-containers_heapster-grafana-amd64%3Av4.4.3.tar'
    ssh_th.execCmd(hosts, dict1, cmdLoadDockerImage1 + ";" + cmdLoadDockerImage2 )



def func_JoinK8s(): # 加入集群
    #hosts = [host for host in hostsM.hosts_k8s if host != '10.129.48.3']
    hosts=hostsM.hosts_k8s2
    cmd1='kubeadm join 10.144.0.21:6443 --token 19318j.6mb3ls3vsfhdczo4 --discovery-token-ca-cert-hash sha256:e1b1b046eda0ebaa58f939e8e02de97f60b99b37792d36f531fe12e99032347c'
    cmd2="sed -i 's/10.96.0.10/10.190.96.10/g' /var/lib/kubelet/config.yaml"
    cmd3="systemctl daemon-reload; systemctl restart kubelet"
    ssh_th.execCmd(hosts, dict1, '%s;%s;%s' % (cmd1, cmd2, cmd3))

def funcScpFile(hosts): # 复制,某个文件夹
    ssh_th.scpDir(hosts, dict1, '/home/nscc/th/', 'sh')
    #ssh_th.execCmd(hosts, dict1, 'cd /home/nscc/th/tar.o; ls | xargs -n 1 docker image load -i')
    #ssh_th.scpDir(hosts, dict1, '/home/nscc/th/', 'calico-2.6.11')
    #ssh_th.scpDir(hosts, dict1, '/home/nscc/th/', 'calico-3.3.0')

if __name__=='__main__':
    #func_chgHostName(hostsM.hosts2)
    #ssh_th.scpDir(hostsM.hosts2, dict1, '/home/nscc/', 'th')
    #func_initInstallSoft_setSwap(hostsM.hosts2)

    #func_loadImage(hostsM.hosts2)
    func_JoinK8s()
    # func_setK8sCadvisor() 一个主机只能执行一次
    #func_resetK8s()
    #
    #func_cfgDocker(hostsM.hosts_cal2)
    #ssh_th.execCmd(hostsM.hosts, dict1, 'rm -r /var/etcd/calico-data')
    #ssh_th.execCmd(hostsM.hosts, dict1, 'chown -R nscc /home/nscc')
    #ssh_th.scpFile(hostsM.hosts, dict1, '/home/nscc/th/calico-3.3.0/', 'calicoctl')
    #ssh_th.scpFile(hostsM.hosts, dict1, '/home/nscc/th/calico-3.3.0/', 'etcdctl')

