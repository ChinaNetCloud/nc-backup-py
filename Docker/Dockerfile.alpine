FROM alpine:3.7
RUN sed "s|dl-cdn.alpinelinux.org|mirrors.aliyun.com|g" /etc/apk/repositories -i && \
    apk update && apk add git python py2-pip && \
    git clone https://github.com/ChinaNetCloud/nc-backup-py.git && \
    cd nc-backup-py && \
    git checkout jenkins-setup && \
    pip install --upgrade .
