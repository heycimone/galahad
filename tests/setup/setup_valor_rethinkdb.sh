#!/bin/bash

EFS_ID="${1}"

sudo apt --assume-yes install nfs-common
sudo mkdir /mnt/nfs
sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport $EFS_ID:/ /mnt/nfs/
sudo cp -R /mnt/nfs/deploy/rethink/config /home/ubuntu
cd /home/ubuntu/config
sudo /bin/bash setup.sh
