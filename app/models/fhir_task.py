import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal

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
    reference: str = Field(
        ...,
        example="Device/MOCK-ROBOT-01",
        description="Tipo/ID do recurso referenciado",
    )
    display: str | None = Field(
        None, example="Robô Mock 01", description="Nome legível"
    )


class BusinessStatus(BaseModel):
    text: str = Field(..., example="Navigating 3rd floor en route to room 304")


class FHIRTask(BaseModel):
    resourceType: Literal["Task"] = "Task"
    id: str = Field(default_factory=lambda: f"task-{uuid.uuid4().hex[:8]}")
    status: TaskStatus = Field(default=TaskStatus.REQUESTED)
    intent: str = Field(
        default="order", description="Intention: proposal | plan | order"
    )
    priority: TaskPriority = Field(default=TaskPriority.ROUTINE)
    description: str | None = Field(default=None, example="O- blood bag in transit")
    focus: dict[str, Any] | None = Field(
        default=None, description="Item or medication in transit"
    )
    owner: Reference | None = Field(None, description="Robot owner task")
    location: Reference | None = Field(None, description="Drop-off location")
    businessStatus: BusinessStatus | None = None
    authoredOn: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    lastModified: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# class TaskUpdate(BaseModel):
#    status: TaskStatus
#    businessStatus_txt: str | None = Field(None, description="Text Description")


class TaskPatch(BaseModel):
    status: TaskStatus | None = Field(default=None, description="New FHIR task status")
    businessStatus: BusinessStatus | None = Field(
        default=None, description="business status"
    )
    priority: TaskPriority | None = Field(default=None, description="Priority Level")
    description: str | None = Field(default=None, description="Task description")
    owner: Reference | None = Field(default=None, description="Device with the task")
    location: Reference | None = Field(default=None, description="Task Location")
    focus: dict[str, Any] | None = Field(default=None, description="Robot payload")
