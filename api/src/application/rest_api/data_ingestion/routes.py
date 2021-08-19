from fastapi import APIRouter


from application.rest_api.data_ingestion.models import DataIngestionPostRequestBody
from application.data_ingestion.tasks import excel_to_mongodb_data_ingestion_task
from application.tasks.models import TaskResponseBody

router = APIRouter()


@router.post(
    "/data-ingestion/",
    response_description="Data ingestion endpoint.",
    response_model=TaskResponseBody,
)
async def excel_to_mongodb_data_ingestion(data_ingestion_post_request_body: DataIngestionPostRequestBody) \
        -> TaskResponseBody:
    """
    Entrypoint for ingesting excel data into the MongoDB database.

    :param data_ingestion_post_request_body: The data ingestion post request body.
    :return TaskResponseBody.
    """
    task = excel_to_mongodb_data_ingestion_task.delay(
        data_ingestion_post_request_body.filepath,
        data_ingestion_post_request_body.excel_sheet_name
    )

    return TaskResponseBody(task_id=task.id)
