init:  # 在线安装python依赖
	pip3 install -r requirements.txt

getoffline:  # 下载需要的python依赖包
	pip3 download -r requirements.txt -d ./dfiles/packages/

loadoffline:  # 从离线依赖包中安装python依赖
	pip3 install --no-index --find-links ./dfiles/packages/ -r requirements.txt 

run: # 启动服务器
	python3 -B run.py -h 0.0.0.0

build: # DockerImage:
	docker build -t chrx/pnet3 .
	#docker save chrx/pnet | gzip -> chrx_pnet.tar.gz  # -o chrx_pnet.tar

