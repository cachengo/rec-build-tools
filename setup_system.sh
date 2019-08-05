#!/bin/bash

sudo yum update -y
sudo yum install -y git wget
sudo yum -y groupinstall 'Development Tools'
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python ~/get-pip.py
sudo yum -y install python-devel

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