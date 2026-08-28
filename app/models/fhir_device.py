from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"


class FHIRDevice(BaseModel):
    resourceType: Literal["Device"] = "Device"
    id: str = Field(..., example="Robot Service Hospital - 01")
    displayName: str | None = Field(None, example="Robot Service Simulated 01")
    status: DeviceStatus = Field(default=DeviceStatus.ONLINE)
    battery: int = Field(default=100, ge=0, le=100, example=95)
    currentLocation: str | None = Field(default="Location/pharmacy-center")
