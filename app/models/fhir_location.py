from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class LocationPhysicalType(str, Enum):
    ROOM = "room"
    STATION = "station"
    PHARMACY = "pharmacy"


class FHIRLocation(BaseModel):
    resourceType: Literal["Location"] = "Location"
    id: str = Field(..., example="room-304")
    name: str = Field(..., example="Room 304 - B")
    floor: str = Field(..., example="3rd floor")
    status: str = Field(default="active", example="active")
    physicalType: LocationPhysicalType | None = LocationPhysicalType.ROOM
