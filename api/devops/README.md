# Transaction Manager Application DevOps
##DevOps related files for the Transaction Manager REST API

###Prerequisites:
- You must have installed Docker and Docker-compose in your OS.

###Steps to manually run the Dockerfiles:

1. cd to the TransactionManager directory.
2. sudo docker build -f api/devops/api/Dockerfile -t transaction-manager-api .
3. sudo docker tag transaction-manager-api transaction-manager-api:0.1
4. sudo docker-compose -f api/devops/docker-compose.yml up -d