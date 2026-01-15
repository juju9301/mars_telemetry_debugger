from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title='Mars Telemetry Debugger API')

app.include_router(router)