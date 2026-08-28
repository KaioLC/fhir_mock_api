from fastapi import APIRouter

router = APIRouter(tags=["Infra"])

@router.get("/health")
async def health_check():
    """Check health service."""
    return {"status": "ok", "service": "fhir-robotics-mock-api"}


