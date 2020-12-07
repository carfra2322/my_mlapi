#!/bin/bash

# UPDATE
sudo yum update -y

# INSTALL DOCKER-COMPOSE
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# PROVIDE PRIVILIGES TO DOCKER COMPOSE
sudo chmod +x /usr/local/bin/docker-compose

# ADD TO PATH
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# INSTALL DOCKER
sudo yum install docker -y

# START DOCKER
sudo service docker start

# GIVE PERMISSIONS TO DOCKER ON EC2
sudo usermod -a -G docker ec2-user

# INSTALL GIT
sudo yum install git -y

# CLONE REPO
git clone https://github.com/carfra2322/my_mlapi.git

# CHANGE DIRECTORY
cd my_mlapi

# DOWNLOAD PICKLE FILES
aws s3 cp s3://mycapstonebucket/num_topics.pkl my_api/num_topics.pkl
aws s3 cp s3://mycapstonebucket/lda.pkl my_api/lda.pkl
aws s3 cp s3://mycapstonebucket/covid.pkl my_api/covid.pkl
aws s3 cp s3://mycapstonebucket/num_topics.pkl my_api/num_topics.pkl

# BUILD AND DEPLOY DOCKERS
sudo docker-compose build
sudo docker-compose up