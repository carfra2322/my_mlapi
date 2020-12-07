# CAPSTONE ML API

API That will return Top 5 recommended medical documents from the covid database, based on your input text

## Installation

> ON AWS EC2
>
> Recommended specs:
> * 50 GB EBS Volume
> * T2.XLARGE

**Note:** This is running in http port 8080, make sure the security groups have that enabled for inbound traffic

Run the run_api.sh script on an [AWS EC2](https://console.aws.amazon.com/ec2)

```
$ bash run_api.sh
```

> Docker only

Make sure you have docker and docker-compose installed.
Clone the Repo and run docker-compose build and then docker-compose up


```
$ docker-compose build
$ docker-compose up
```


Folder Structure 
============================


    my_mlapi
    ├── my_api                 # Flask api for ML endpoint       
    ├── nginx                    # Holds Nginx Dockerfile
    ├── docker-compose.yml       # Orchestrates the 3 docker files (api, locust, nginx)
    ├── run_api.sh               # One touch shell script for spinning up the full application
    └── readme.md                # Readme documentation