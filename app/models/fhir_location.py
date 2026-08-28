from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class LocationPhysicalType(str, Enum):
    ROOM = "room"
    STATION = "station"
    PHARMACY = "pharmacy"


class FHIRLocation(BaseModel):
    resourceType: str = Field(
        default="Location",
        const=True
    )
    id: str = Field(
        ..., 
        example="room-304"
    )
    name: str = Field(
        ...,
        example="Room 304 - B"
    )
    floor: str = Field(
        ...,
        example="3rd floor"
    )
    status: str = Field(
        default="active",
        example="active"
    )
    physicalType: Optional[LocationPhysicalType] = LocationPhysicalType.ROOM
