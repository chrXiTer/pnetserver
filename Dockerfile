FROM python:3.7.1-alpine3.8
LABEL maintainer cx<cx@663.cn>001

WORKDIR /app
ADD ./dfiles/go1.11.2.src.tar.gz /app/go.tgz

# 添加 golang
# 根据 python:3.7-alpine3.8 的 Dockerfile 内容 
# 移除 golang:1.11.2-alpine3.8 Dockerfile 中不不要的内容添加到下面
# vim 一行是后面自己需要的软件，放这里统一安装
RUN [ ! -e /etc/nsswitch.conf ] && echo 'hosts: files dns' > /etc/nsswitch.conf
ENV GOLANG_VERSION 1.11.2
RUN set -eux; \
	apk add --no-cache --virtual .build-deps \
	    dropbear-ssh dropbear-scp vim \
		bash musl-dev openssl go; 
RUN export \
		GOROOT_BOOTSTRAP="$(go env GOROOT)" \
		GOOS="$(go env GOOS)" \
		GOARCH="$(go env GOARCH)" \
		GOHOSTOS="$(go env GOHOSTOS)" \
		GOHOSTARCH="$(go env GOHOSTARCH)"; \
    echo '042fba357210816160341f1002440550e952eb12678f7c9e7e9d389437942550 *go.tgz' | sha256sum -c -; \
	tar -C /usr/local -xzf go.tgz; 	rm go.tgz; \
	cd /usr/local/go/src; \
	./make.bash; \
	rm -rf /usr/local/go/pkg/bootstrap /usr/local/go/pkg/obj; \
	apk del .build-deps; \
	export PATH="/usr/local/go/bin:$PATH"; \
	go version
ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH
RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"
#WORKDIR $GOPATH

#
# 添加自己的代码
#
ADD ./requirements.txt /app
#RUN apk --update add gcc linux-headers
RUN pip3 install -r /app/requirements.txt 
#RUN pip3 install --no-cache-dir --no-index --find-links=/dfiles/packages -r requirements.txt \
    #&& rm -r /dfiles
ADD ./appdc /app/appdc
ADD ./manage.py /app
ADD ./crun.py /app

EXPOSE 80

CMD python3 manage.py runserver -h 0.0.0.0 -p 80
