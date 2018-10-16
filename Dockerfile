FROM python:3.7-alpine3.8
LABEL maintainer cx<cx@663.cn>001

WORKDIR /app


ADD ./requirements.txt /app
#RUN apk --update add gcc linux-headers
#RUN pip3 install -r /app/requirements.txt
ADD ./packages /app/packages
RUN apk --update add dropbear-ssh dropbear-scp vim\
    && pip3 install --no-cache-dir --no-index --find-links=/app/packages -r requirements.txt \
    && rm -r /app/packages

LABEL vv1="001"
ADD ./appdc /app/appdc
ADD ./manage.py /app
ADD ./crun.py /app

EXPOSE 80

CMD python3 manage.py runserver -h 0.0.0.0 -p 80
