help:
	@echo " "
	@echo "Targets:"
	@echo " "
	@echo "- make deploy-local"
	@echo "- make down-services"
	@echo " "

deploy-local:
		@echo "=============================== Start Local Deployment ==============================="
		@echo "=================================== Requirements ====================================="
		@echo "1. Ensure you have Docker installed and service up and running in your system."
		@echo "2. Ensure you have Docker Compose installed and with permissions to execute it."
		sudo docker build -f api/devops/api/Dockerfile -t transaction-manager-api .
		sudo docker tag transaction-manager-api transaction-manager-api:0.1
		sudo docker-compose -f api/devops/docker-compose.yml up -d

down-services:
		@echo "======================= Stopping Local Deployment Running Services==============================="
		sudo docker-compose -f api/devops/docker-compose.yml down