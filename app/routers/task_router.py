from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.models.fhir_task import BusinessStatus, FHIRTask, TaskStatus, TaskPatch
from app.services.state_store import state_store

router = APIRouter(prefix="/fhir/Task", tags=["FHIR Task"])


@router.post("", response_model=FHIRTask, status_code=status.HTTP_201_CREATED)
async def create_task(task_input: FHIRTask):
    """
    Create a new task
    """
    state_store.tasks[task_input.id] = task_input

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=task_input.model_dump(mode="json"),
        headers={"Location": f"/fhir/Task/{task_input.id}"},
    )


@router.get("/{task_id}", response_model=FHIRTask)
async def get_task(task_id: str):
    """Check a task stats"""
    if task_id not in state_store.tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_id}' não encontrada.",
        )
    return state_store.tasks[task_id]


@router.get("", response_model=list[FHIRTask])
async def list_tasks(
    status_filter: TaskStatus | None = Query(None, alias="status"),
    owner: str | None = Query(None, description="Ex: Device/MOCK-ROBOT-01"),
):
    """List tasks wiht filter"""
    results = list(state_store.tasks.values())
    if status_filter:
        results = [t for t in results if t.status == status_filter]
    if owner:
        results = [
            t for t in results if t.owner and t.owner.reference.lower() == owner.lower()
        ]
    return results


@router.patch("/{task_id}", response_model=FHIRTask)
async def patch_task(task_id: str, patch_data: TaskPatch):
    """
    patch a specified field in a task
    """
    if task_id not in state_store.tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_id}' não encontrada.",
        )

    task = state_store.tasks[task_id]

    update_dict = patch_data.model_dump(exclude_unset=True)

    for field_name in update_dict:
        new_val = getattr(patch_data, field_name)
        setattr(task, field_name, new_val)

    task.lastModified = datetime.now(timezone.utc)

    return task
