from fastapi import APIRouter, HTTPException, status

from app.models.fhir_location import FHIRLocation
from app.services.state_store import state_store

router = APIRouter(prefix="/fhir/Location", tags=["FHIR Location"])


@router.get("", response_model=list[FHIRLocation])
async def list_locations():
    """List all locations"""
    return list(state_store.locations.values())


@router.get("/{location_id}", response_model=FHIRLocation)
async def get_location(location_id: str):
    """Check Location details"""
    if location_id not in state_store.locations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location '{location_id}' not found.",
        )

    return state_store.locations[location_id]
