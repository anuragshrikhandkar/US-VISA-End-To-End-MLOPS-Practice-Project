# US-VISA-End-To-End-MLOPS-Practice-Project
MLOPS Pratice Project 

## workflows 
 1.constants 
 2.entity
 3.components
 4.pipeline 
 5.main file


 ## Key Technologies

1.Machine Learning Model: (KNeighborsClassifier, RandomForestClassifier) trained to predict visa approvals/rejections.

2.MongoDB: NoSQL database to store and manage database

3.MLOps Pipeline: Data ingestion, Data Validation, Model training, model deployement are various pipeline used for effective project implementation.

3.Docker: Containerization for packaging the application and its dependencies, ensuring consistent execution across environments.

4.AWS EC2: Cloud-based deployment platform for hosting the application in a scalable and cost-effective manner.

5.Amazon S3 Bucket: S3 is Simple Storage Services is a cloud storage service It is used to store retrive any amount of data

6.GitHub Actions: Continuous Integration and Continuous Delivery (CI/CD) tool for automating the build, testing, and deployment of the application on AWS EC2 upon code changes.


## GIT HUB Actions 

git add .

git commit -m "First Commit Created Sucessfully"

git push orign main


## Conda Env

conda create -n visa python=3.8 -y

conda activate visa

python -m venv myenv

pip install -r requirements.txt


## Export the environment veriables 

export MONGODB_URL="mongodb+srv://<username>:<password>...."

export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>


## AWS-CICD-Deployment-with-Github-Actions
1. Logging AWS CONSOLE
2. CREATE A IAM USER FOR DEPLOYMNENT

#with specific access

1. EC2 access : It is virtual machine

2. ECR: Elastic Container registry to save your docker image in aws


#Description: About the deployment

1. Build docker image of the source code

2. Push your docker image to ECR

3. Launch Your EC2 

4. Pull Your image from ECR in EC2

5. Lauch your docker image in EC2

#Policy:

1. AmazonEC2ContainerRegistryFullAccess

2. AmazonEC2FullAccess   

## Create ECR repo to store/save docker image
- Save the URI:

## Create EC2 machine (Ubuntu)

## Open EC2 and Install docker in EC2 Machine:

#optinal

sudo apt-get update -y

sudo apt-get upgrade

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker

## Configure EC2 as self-hosted runner:

setting>actions>runner>new self hosted runner> choose os> then run command one by one

## Setup github secrets:

1.AWS_ACCESS_KEY_ID
2.AWS_SECRET_ACCESS_KEY
3.AWS_DEFAULT_REGION
4.ECR_REPO


<img width="1919" height="1079" alt="Screenshot 2025-08-13 183809" src="https://github.com/user-attachments/assets/2c235908-0849-4758-a4c3-36fc6656e722" />

<img width="1919" height="1079" alt="Screenshot 2025-08-13 183928" src="https://github.com/user-attachments/assets/13f97a1c-1285-48d5-bc15-93d9713c4545" />

<img width="1919" height="1077" alt="Screenshot 2025-08-13 183403" src="https://github.com/user-attachments/assets/9182108a-5e5d-48c7-8dbc-18c272c5732c" />

