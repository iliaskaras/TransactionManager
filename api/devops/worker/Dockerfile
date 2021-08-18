FROM python:3.7

ARG transaction_manager_worker_user_id=9004
ARG transaction_manager_worker_group_id=9004

# Environment variables such as mongodb_connection_uri should not be displayed like that
# and instead be passed with some other mechanism that hides these information. Ansible could be used for example.
ARG transaction_manager_api_environment="local"
ARG transaction_manager_api_directory="/usr/local/transaction-manager-api"
ARG mongodb_connection_uri="mongodb://mongo:27017/test"
ARG celery_broker_url="redis://localhost:6379"
ARG celery_result_backend="redis://localhost:6379"
ARG java_home="/usr/lib/jvm/java-1.11.0-openjdk-amd64"
ARG spark_input_uri="mongodb://localhost:27017/transaction_manager.transactions"
ARG spark_output_uri="mongodb://localhost:27017/transaction_manager.transactions"
ARG spark_driver_memory="10g"
ARG spark_app_name="Transaction Manager Spark"

ENV TRANSACTION_MANAGER_API_ENVIRONMENT ${transaction_manager_api_environment}
ENV MONGODB_CONNECTION_URI ${mongodb_connection_uri}
ENV CELERY_BROKER_URL ${celery_broker_url}
ENV CELERY_RESULT_BACKEND ${celery_result_backend}
ENV JAVA_HOME ${java_home}
ENV SPARK_INPUT_URI ${spark_input_uri}
ENV SPARK_OUTPUT_URI ${spark_output_uri}
ENV SPARK_DRIVER_MEMORY ${spark_driver_memory}
ENV SPARK_APP_NAME ${spark_app_name}

# Create Transaction Manager API group and user.
RUN groupadd --system --gid ${transaction_manager_worker_group_id} appuser \
  && useradd --system --shell /usr/sbin/nologin \
             --gid appuser --uid ${transaction_manager_worker_user_id} appuser

# Install and configure Java, Scala and Spark for local spark deployment.
RUN apt-get update -y \
  && apt-get install default-jdk -y \
  && java --version \
  && wget www.scala-lang.org/files/archive/scala-2.12.14.deb \
  && dpkg -i scala-2.12.14.deb \
  && apt-get update \
  && apt-get install scala \
  && wget https://archive.apache.org/dist/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz \
  && tar -xvzf spark-2.4.6-bin-hadoop2.7.tgz \
  && mv spark-2.4.6-bin-hadoop2.7/ /opt/spark \
  && echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc \
  && echo 'export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH' >> ~/.bashrc \
  && echo 'export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> ~/.bashrc \
  && echo 'export JAVA_PATH=/usr/lib/jvm/java-11-openjdk-amd64/' >> ~/.bashrc \
  && rm scala-2.12.14.deb \
  && rm spark-2.4.6-bin-hadoop2.7.tgz

# Create Transaction Manager API directory.
RUN mkdir -p ${transaction_manager_api_directory}/src \
  && chown -R appuser:appuser ${transaction_manager_api_directory} \
  && chmod -R 770 ${transaction_manager_api_directory}

# Copy and install Transaction Manager API requirements.txt.
COPY --chown=appuser:appuser "api/requirements.txt" ${transaction_manager_api_directory}/
RUN pip3 install -r ${transaction_manager_api_directory}/requirements.txt

# Copy Transaction Manager API source code.
COPY --chown=appuser:appuser "api/src" ${transaction_manager_api_directory}/src/

# Run Transaction Manager API.
ENV PYTHONPATH ${transaction_manager_api_directory}/src
WORKDIR ${transaction_manager_api_directory}/src

