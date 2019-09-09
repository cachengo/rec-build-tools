#!/bin/bash

sudo yum update -y
sudo yum install -y git wget
sudo yum -y groupinstall 'Development Tools'
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python ~/get-pip.py
sudo yum -y install python-devel

sudo yum remove docker docker-client docker-client-latest \
    docker-common docker-latest docker-latest-logrotate \
    docker-logrotate docker-engine
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum -y install docker-ce docker-ce-cli containerd.io
sudo mkdir -p /etc/docker/
echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
sudo systemctl start docker
# Ugly hack to make docker usable for non-root
# (adding to the group would require re-login)
sudo chmod 777 /var/run/docker.sock
sudo yum -y install createrepo libguestfs-tools-c jq
sudo systemctl start libvirtd
systemctl status libvirtd

yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install mock createrepo rpmdevtools
getent group mock || groupadd mock
usermod -a -G mock $USER
