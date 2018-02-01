FROM alpine:3.7
RUN sed "s|dl-cdn.alpinelinux.org|mirrors.aliyun.com|g" /etc/apk/repositories -i && \
    apk update && apk add git python && \
    git clone https://github.com/ChinaNetCloud/nc-backup-py.git && \
    git checkout jenkins-setup && \
    cd nc-backup-py && \
    pip install --upgrade .
