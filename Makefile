init:  # 在线安装python依赖
	pip3 install -r requirements.txt

getoffline:  # 下载需要的python依赖包
	pip3 download -r requirements.txt -d ./packages/

loadoffline:  # 从离线依赖包中安装python依赖
	pip3 install –no-index –find-links=./packages -r requirements.txt 

run: # 启动服务器
	python3 -B manage.py runserver -h 0.0.0.0

build: # DockerImage:
	docker build -t chrx/pnet .
	#docker save chrx/pnet | gzip -> chrx_pnet.tar.gz  # -o chrx_pnet.tar

