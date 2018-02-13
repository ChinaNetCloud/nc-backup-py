#!/bin/bash

sudo sed 's|^mirrorlist|#mirrorlist|g' /etc/yum.repos.d/CentOS-* -i
sudo sed 's|^#baseurl|baseurl|g' /etc/yum.repos.d/CentOS-* -i
sudo sed 's|mirror.centos.org|mirrors.aliyun.com|g' /etc/yum.repos.d/CentOS-* -i
sudo sed 's|enabled=1|enabled=0|g' /etc/yum/pluginconf.d/fastestmirror.conf -i
sudo yum install https://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm -y
sudo yum update --assumeno
echo "sudo yum install git python python-pip python-wheel python-crypto sudo -y"
sudo yum install git python python-pip python-wheel python-crypto sudo -y
sudo yum groupinstall 'Development Tools' -y
# git clone https://github.com/ChinaNetCloud/nc-backup-py.git
# cd nc-backup-py
sudo git checkout jenkins-setup
sudo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade .
