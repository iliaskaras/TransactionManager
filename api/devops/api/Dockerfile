FROM python:3.8.2

ARG transaction_manager_api_user_id=9003
ARG transaction_manager_api_group_id=9003

# Environment variables such as mongodb_connection_uri should not be displayed like that
# and instead be passed with some other mechanism that hides these information. Ansible could be used for example.
ARG transaction_manager_api_environment="local"
ARG transaction_manager_api_directory="/usr/local/transaction-manager-api"
ARG mongodb_connection_uri="mongodb://mongo:27017/test"
ARG celery_broker_url="redis://localhost:6379"
ARG celery_result_backend="redis://localhost:6379"

ENV TRANSACTION_MANAGER_API_ENVIRONMENT ${transaction_manager_api_environment}
ENV MONGODB_CONNECTION_URI ${mongodb_connection_uri}
ENV CELERY_BROKER_URL ${celery_broker_url}
ENV CELERY_RESULT_BACKEND ${celery_result_backend}

# Create Transaction Manager API group and user.
RUN groupadd --system --gid ${transaction_manager_api_group_id} appuser \
  && useradd --system --shell /usr/sbin/nologin \
             --gid appuser --uid ${transaction_manager_api_user_id} appuser

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
WORKDIR ${transaction_manager_api_directory}
ENV PYTHONPATH ${transaction_manager_api_directory}/src
USER appuser

ENTRYPOINT ["uvicorn", "application.main:application", "--host", "0.0.0.0", "--port", "8000"]
