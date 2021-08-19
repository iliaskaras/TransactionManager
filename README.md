# TransactionManager
### A REST API written with the FastAPI Web Framework

A FastAPI Rest API that provides endpoints that query a MongoDB using PySpark.

## Description
A FastAPI Rest API that provides endpoints that query a MongoDB using PySpark. The data are Transactions that are
included in an Excel file and ingested into the MongoDB using Spark. All the endpoints for retrieving information
about transactions are executed using Spark queries. Celery with redis has been used to trigger and execute the
Spark calls, providing also an endpoint for retrieving Task details.

##### Showcasing:
1. PySpark's implementation.
2. Celery for async tasks with Redis as broker.
3. Flower for task monitoring.

### Transaction Manager REST endpoints:
1. ***POST***: Data ingestion from excel file to MongoDB.
2. ***GET***: Retrieve celery task details. For monitoring the running tasks and retrieving their results when finished. 
3. ***GET***: Get group transactions by InvoiceNo.
4. ***GET***: Get the most sold product.
5. ***GET***: Get customer with the most spent money.
6. ***GET***: Get the average unit price.
7. ***GET***: Get the price and quantity ratio for all the invoices.

## Getting Started

### Dependencies

* Have Docker and docker-compose installed in your OS.
* Linux
* Have the ports used in the project's deployment free, or make sure to modify the docker-compose.yml.

### Deploying the REST API

* Download the repository.
* Change directory to TransactionManager where the Makefile is located.
* Run the docker-compose with the Makefile command (warning: you might be required to type your sudo password):
```
make deploy-local
```
* This will deploy the following:
    * ****MongoDB container****
    * The ****Redis****
    * The ****The Celery Worker****
    * The ****REST API****
    * The ****Flower****

### Testing the REST API

* A collection of Postman ****TransactionManager.postman_collection.json**** requests is provided under the TransactionManager directory, import and:
* The Excel file that you will be using to ingest and initialize the MongoDB database 
  ****should locate under the '/mnt/data' directory, because this directory is volumed to the rest api docker container.****

* Run tests with the Makefile command: 
```
make run-tests
```

## Version History

* 0.1
    * Initial Release
