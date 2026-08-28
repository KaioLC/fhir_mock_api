"""
ARQUIVO MOCK: SIMULAR ARMAZENAMENTO LOCAL
"""

from typing import Dict
from app.models.fhir_task import FHIRTask
from app.models.fhir_location import FHIRLocation, LocationPhysicalType
from app.models.fhir_device import FHIRDevice, DeviceStatus

class StateStore:
    def __init__(self) -> None:
        self.tasks: Dict[str, FHIRTask] = {}

        self.devices: Dict[str, FHIRDevice] = {
            "MOCK-ROBOT-01": FHIRDevice(
                id="MOCK-ROBOT-01"
                displayName="Robot Service Simulated 01",
                status=DeviceStatus.ONLINE,
                battery=95,
                currentLocation="Location/pharmacy-center"
            ),

            "MOCK-ROBOT-02": FHIRDevice(
                id="MOCK-ROBOT-02",
                displayName="Robot Service Simulated 02"
                status=DeviceStatus.OFFLINE,
                battery=100,
                currentLocation="Location/charge-base"
            )
        }

        self.locations: Dict[str, FHIRLocation] = {
            "pharmacy-center": FHIRLocation(
                id="pharmacy-center",
                name="Pharmacy Center",
                floor="1nd floor",
                status="active",
                physicalType=LocationPhysicalType.PHARMACY
            ),
            "room-304": FHIRLocation(
                id="room-304",
                name="Room 304 - B"
                floor="3rd floor",
                status="active",
                physicalType=LocationPhysicalType.ROOM
            ),
            "room-201": FHIRLocation(
                id="room-201",
                name="Room 201 - A",
                floor="2nd floor"
                status="active",
                physicalType=LocationPhysicalType.ROOM
            ),
            "nurse-station-01": FHIRLocation(
                id="nurse-station-01",
                name="Nurse Station - 1",
                floor="2nd floor",
                status="active",
                physicalType=LocationPhysicalType.STATION
            )
        }

state_store = StateStore()
