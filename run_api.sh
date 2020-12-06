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
git clone https://github.com/carfra2322/sfml2

# CHANGE DIRECTORY
cd sfml2

# DOWNLOAD TEST AND TRAIN DATA
wget -O api/exercise_26_test.csv https://sf-ml-role.s3.amazonaws.com/exercise_26_test.csv
wget -O api/exercise_26_train.csv https://sf-ml-role.s3.amazonaws.com/exercise_26_train.csv

# BUILD AND DEPLOY DOCKERS
sudo docker-compose build
sudo docker-compose up