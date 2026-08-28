import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field



class TaskStatus(str, Enum):
    DRAFT = "draft"
    REQUESTED = "requested"
    RECEIVED = "received"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in-progress"
    ON_HOLD = "on-hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class TaskPriority(str, Enum):
    ROUTINE = "routine"
    URGENT = "urgent"
    ASAP = "asap"
    STAT = "stat"

class Reference(BaseModel):
    reference: str = Field(...,example="Device/MOCK-ROBOT-01",description="Tipo/ID do recursso referenciado",display: Optional[str] = Field(None,example="Robô Mock 01",description="Name"))

class BusinessStatus(BaseModel):
    text: str = Field(...,example="Navigating 3rd floor en route to room 304")

class FHIRTask(BaseModel):
    resourceType: str = Field(
        default="Task",
        const=True,
    )
    id: str = Field(
        default_factory=lambda: f"task-{uuid.uuid4().hex[:8]}"
    )
    status: TaskStatus = Field(
        default=TaskStatus.REQUESTED
    )
    intent: str = Field(
        default="order",
        description="Intention: proposal | plan | order"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.ROUTINE
    )
    description: Optional[str] = Field(
        default=None,
        example="O- blood bag in transit"
    )
    focus: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Item or medication in transit"
    )
    owner: Optional[Reference] = Field(
        None,
        description="Robot owner task"
    )
    location: Optional[Reference] = Field(
        None,
        description="Drop-off location"
    )
    businessStatus: Optional[BusinessStatus] = None
    authoredOn: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    lastModified: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class TaskUpdate(BaseModel):
    status:TaskStatus
    businessStatus_txt: Optional[str] = Field(
        None,
        description="Text Description"
    )

    
