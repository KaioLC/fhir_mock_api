from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import device_router, health_router, location_router, task_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API RESTful FHIR",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router.router)
app.include_router(task_router.router)
app.include_router(location_router.router)
app.include_router(device_router.router)
