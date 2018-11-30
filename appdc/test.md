# test

## 1

```sh
/home/nscc/th/calico-2.6.11/calicoctl node run --node-image=quay.io/calico/node:v2.6.11 \
        --config=/home/nscc/th/calico-2.6.11/calico-1.cfg

cat <<EOF | /home/nscc/th/calico-2.6.11/calicoctl create \
    --config=/home/nscc/th/calico-2.6.11/calico-1.cfg -f -
apiVersion: v1
kind: ipPool
metadata:
    cidr: 10.190.160.0/19
spec:
    ipip:
        enabled: true
        mode: cross-subnet
    nat-outgoing: true
EOF

/home/nscc/th/calico-2.6.11/calicoctl get ipPool \
    --config=/home/nscc/th/calico-2.6.11/calico-1.cfg


docker network create --driver calico --ipam-driver calico-ipam \
        --subnet=10.190.160.0/19 L3net
# 10.144.0.26
docker run -itd --network L3net --name c11 alpine:3.8 sh
docker run -itd --network L3net --name c12 alpine:3.8 sh
docker exec -it c11 ip addr # 10.190.184.192/32
docker exec -it c12 ip addr # 10.190.184.193/32

# 10.144.0.27
docker run -itd --network L3net --name c21 alpine:3.8 sh
docker exec -it c21 ip addr # 10.190.166.64/32

docker exec -it c11 ping c12
docker exec -it c11 ping c21

```

## 2

```sh

docker network create --driver overlay --attachable  L2onet

# 10.144.0.26
docker run -itd --network L2onet --name o11 alpine:3.8 sh
docker run -itd --network L2onet --name o12 alpine:3.8 sh
docker exec -it o11 ip addr # 10.0.1.2/24
docker exec -it o12 ip addr # 10.0.1.3/24

# 10.144.0.27
docker run -itd --network L2onet --name o21 alpine:3.8 sh
docker exec -it o21 ip addr # 10.0.1.4/24

docker exec -it o11 ping o12
docker exec -it o11 ping 10.0.1.4  #o21   开始测得时候是通的，后来不通了

```

## 3

```sh
# 10.144.0.26
docker network create --driver macvlan \
            --subnet=10.190.32.0/19 --gateway=10.190.32.1 \
            -o parent=enp8s0f0 L2mnet
docker run -itd --network L2onet --name m11 alpine:3.8 sh
docker run -itd --network L2onet --name m12 alpine:3.8 sh
docker exec -it m11 ip addr # 10.190.32.2/19
docker exec -it m12 ip addr # 10.190.32.3/19

# 10.144.0.27
docker network create --driver macvlan \
            --subnet=10.190.32.0/19 --gateway=10.190.32.1 \
            -o parent=enp8s0f0 L2mnet   # macvlan是主机内网络，需要在每个主机都运行
docker run -itd --network L2onet ip 10.190.32.4 --name m21 alpine:3.8 sh   # 需要指定ip否则会从2开始
docker exec -it m21 ip addr # 10.190.32.4/19

docker exec -it m11 ping m12
docker exec -it m11 ping 10.190.32.4   # 不能使用 m21, macvlan 未提供 DNS

```

## 4

```sh

docker network create --driver calico --ipam-driver calico-ipam L3net-1
docker network create --driver calico --ipam-driver calico-ipam L3net-1
```

### 运行容器

```sh
#---10.144.0.26
docker run -itd --name g1111 --network L3net-1 nginx:1.15-alpine sh
docker run -itd --name g2111 --network L3net-2 nginx:1.15-alpine sh
docker exec -it g1111 ip addr  # 10.190.184.202/32
docker exec -it g2111 ip addr  # 10.190.184.203/32

#--10.144.0.27
docker run -itd -name g2121 --network L3net-2 nginx:1.15-alpine sh
docker exec -it g2121 ip addr # 10.190.166.66/32

#--10.145.0.26
docker run -itd --name g1231 --network L3net-2 nginx:1.15-alpine sh
docker exec -it g1231 ip addr # 10.190.177.214/32
```

###　测试联通性1

```sh
#---10.144.0.26
#docker exec -it g1111 ping -c 3 g2111;\
#docker exec -it g1111 ping -c 3 g2121;\
#docker exec -it g1111 ping -c 3 g1231
docker exec -it g1111 ping -c 3 10.190.184.203;\
docker exec -it g1111 ping -c 3 10.190.166.66;\
docker exec -it g1111 ping -c 3 10.190.177.214

# /home/nscc/th/calico-2.6.11/calicoctl get profile --config=/home/nscc/th/calico-2.6.11/calico-1.cfg

cat <<EOF | /home/nscc/th/calico-2.6.11/calicoctl apply --config=/home/nscc/th/calico-2.6.11/calico-1.cfg -f -
- apiVersion: v1
  kind: profile
  metadata:
    name: L3net-1
    tags:
    - L3net-1
  spec:
    egress:
    - action: allow
      destination: {}
      source: {}
    ingress:
    - action: allow
      destination: {}
      source:
        tag: L3net-1
        ingress:
    - action: allow
      destination: {}
      source:
        tag: L3net-2
EOF

docker exec -it g1111 ping -c 3 g2111;\
docker exec -it g1111 ping -c 3 g2121;\
docker exec -it g1111 ping -c 3 g1231

```

###　测试联通性2

```sh
#---10.144.0.26
docker exec -it g2111 ping -c 3 g2121


cat <<EOF | /home/nscc/th/calico-2.6.11/calicoctl apply --config=/home/nscc/th/calico-2.6.11/calico-1.cfg -f -
- apiVersion: v1
  kind: profile
  metadata:
    name: L3net-1
    tags:
    - L3net-1
  spec:
    egress:
    - action: allow
      destination: {}
      source: {}
    ingress:
    - action: allow
      destination: {}
      source:
        tag: L3net-1
        ingress:
    - action: allow
      destination: {}
      source:
        tag: L3net-2
    - action: deny
      destination: {
        nets: 
        - 10.0.
      }
      source:
        nets: 
        - 10.0.20.0/24
EOF
```



## 5

```sh
#----10.144.0.26
# 不能指定ip地址，否则运行会失败，docker 会提示错误
docker run -d --network L2onet  --name looper --security-opt seccomp:unconfined alpine:3.8 \
    /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'

docker exec -it looper ip addr # 10.0.1.5
docker logs looper # 可以看到从1开始的计数

docker checkpoint create --checkpoint-dir=/tmp looper checkpoint3
docker logs looper   #在131结束

scp -r ./checkpoint3 nscc@10.144.0.27:/home/nscc

#----10.144.0.27
date "+%Y-%m-%d %H:%M:%S %N";\
docker create --network L2onet --name looper --security-opt seccomp:unconfined alpine:3.8 \
    /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done';\
docker start --checkpoint-dir=//home/nscc --checkpoint=checkpoint3 looper;\
date "+%Y-%m-%d %H:%M:%S %N"

## 输出
#2018-11-30 09:23:43 752522643
#ddcfbeaea5a2ce354891212605eba76c993654706f87710bb559f8d692ed980d
#2018-11-30 09:23:45 346482491

docker logs looper  #从132开始
docker exec -it looper ip addr # 10.0.1.5
```

## 6

```sh
#---10.145.0.27

# 创建网络
docker network create --driver calico --ipam-driver calico-ipam L3net-z

# 运行1k容器
cat << EOF | sh -
exec 1>logRun1kNginx.log
date "+%Y-%m-%d %H:%M:%S %N"
for i in \$(seq 1 1000)
do
docker run -itd --network none --name nn_\$i nginx:1.15-alpine sh
done
date "+%Y-%m-%d %H:%M:%S %N"
EOF

# 将1k容器加入到网络
cat << EOF | sh -
exec 1>logConToNet.log
date "+%Y-%m-%d %H:%M:%S %N"
for i in \$(seq 1 1000)
do
docker network disconnect none nn_\$i
docker network connect L3net-z nn_\$i
done
date "+%Y-%m-%d %H:%M:%S %N"
EOF
```

## 7

```sh
#---10.144.0.26

docker run -itd --network none --name z-11 alpine:3.8 sh

date "+%Y-%m-%d %H:%M:%S %N";\
docker network disconnect none z-11;\
docker network connect L3net-z z-11;\
date "+%Y-%m-%d %H:%M:%S %N"

#2018-11-30 10:08:42 763160170
#2018-11-30 10:08:44 321455066

docker exec -it z-11 ip addr  # 10.190.184.201/32
docker exec -it z-11 ping 10.144.0.26 # 可以ping通
docker exec -it z-11 ping 10.145.0.26 # 可以ping通

