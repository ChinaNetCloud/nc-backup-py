#!/bin/bash

sudo ed 's|^mirrorlist|#mirrorlist|g' /etc/yum.repos.d/CentOS-* -i
sudo ed 's|^#baseurl|baseurl|g' /etc/yum.repos.d/CentOS-* -i
sudo ed 's|mirror.centos.org|mirrors.aliyun.com|g' /etc/yum.repos.d/CentOS-* -i
sudo ed 's|enabled=1|enabled=0|g' /etc/yum/pluginconf.d/fastestmirror.conf -i
sudo um install https://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm -y
sudo um updateinfo && yum install git python python-pip python-wheel python-crypto sudo -y
sudo um groupinstall 'Development Tools' -y
# git clone https://github.com/ChinaNetCloud/nc-backup-py.git
# cd nc-backup-py
sudo it checkout jenkins-setup
sudo ip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade .
