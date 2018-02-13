#!/bin/bash

sudo -s
sed 's|^mirrorlist|#mirrorlist|g' /etc/yum.repos.d/CentOS-* -i
sed 's|^#baseurl|baseurl|g' /etc/yum.repos.d/CentOS-* -i
sed 's|mirror.centos.org|mirrors.aliyun.com|g' /etc/yum.repos.d/CentOS-* -i
sed 's|enabled=1|enabled=0|g' /etc/yum/pluginconf.d/fastestmirror.conf -i
yum install https://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm -y
yum updateinfo && yum install git python python-pip python-wheel python-crypto sudo -y
yum groupinstall 'Development Tools' -y
# git clone https://github.com/ChinaNetCloud/nc-backup-py.git
# cd nc-backup-py
git checkout jenkins-setup
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade .
