from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import jobs
from app.core.custom_exception import CustomException

app = FastAPI()

app.include_router(jobs.router)

@app.get("/health")
async def read_root():
    return {
        'Message': 'Wel-Come to jobs API'
    }

@app.exception_handler(CustomException)
async def global_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': exc.message
        }
    )