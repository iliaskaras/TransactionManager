from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/tasks/{task_id}")
async def get_status(task_id):
    task_result = AsyncResult(task_id)

    if task_result.state == states.STARTED:
        response = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
    elif task_result.state == states.FAILURE:
        return JSONResponse(task_result.result)
    else:
        response = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }

    return JSONResponse(response)


