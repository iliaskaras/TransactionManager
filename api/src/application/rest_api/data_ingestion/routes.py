from fastapi import APIRouter
from starlette.responses import JSONResponse


from application.rest_api.data_ingestion.models import DataIngestionPostRequestBody
from application.rest_api.data_ingestion.tasks import data_ingestion_spark_job_task

router = APIRouter()


@router.post("/data-ingestion-spark/", response_description="Data ingestion spark endpoint")
async def data_ingestion(data_ingestion_post_request_body: DataIngestionPostRequestBody):
    task = data_ingestion_spark_job_task.delay(
        data_ingestion_post_request_body.filepath,
        data_ingestion_post_request_body.data_address
    )

    return JSONResponse({"task_id": task.id})
