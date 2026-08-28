from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field




class DeviceStatus(str, Enum):
    ONLINE="online"
    OFFLINE ="offline"
    BUSY="busy"

class FHIRDevice(BaseModel)
    resourceType: str = Field(default="Device", const=True)
    id: str = Field(
        ...,
        example="Robot Service Hospital - 01"
    )
    status: DeviceStatus = Field(
        default=DeviceStatus.ONLINE
    )
    battery: int = Field(
        default=100, ge=10, le=100, example=95
    )
    currentLocation: Optional[str] = Field(
        default="Location/pharmacy-center"
    )

