from fastapi import APIRouter, HTTPException, status

from app.models.fhir_device import FHIRDevice
from app.services.state_store import state_store

router = APIRouter(prefix="/fhir/Device", tags=["FHIR Device"])


@router.get("", response_model=list[FHIRDevice])
async def list_devices():
    """List all Robots"""
    return list(state_store.devices.values())


@router.get("/{device_id}", response_model=FHIRDevice)
async def get_device(device_id: str):
    """Check robot stats"""
    if device_id not in state_store.devices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Robot '{device_id}' not found.",
        )

    return state_store.devices[device_id]
