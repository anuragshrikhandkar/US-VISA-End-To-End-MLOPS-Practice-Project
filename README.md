# US-VISA-End-To-End-MLOPS-Practice-Project
MLOPS Pratice Project 

## workflows 
 constants 
 entity
 components
 pipeline 
 main file


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
