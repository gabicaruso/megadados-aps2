from typing import Optional, List, Dict
from fastapi import FastAPI, APIRouter, Path, Body, Query, HTTPException, Depends
import uuid
from ..database import DBSession, get_db
from ..models import (TaskIn, TaskOut, TaskInUpdate, TaskStatusModel)

router = APIRouter()

@router.get("/check",
         summary="Check",
         description="Used to check if the network is running",)

def get_root():
    return {"Check": "Running"}


@router.post("",
          summary="Create Tasks",
          description="Used to create new tasks",
          response_description="New task",
          response_model=TaskOut)

async def create_task(task: TaskIn = Body(...), db: DBSession = Depends(get_db)):
    return db.create_task(task)


@router.get("",
         summary="Read Tasks",
         description="Used to consult the sistem in order to retrieve tasks on the dictionary",
         response_description="Dictionary containing all tasks based on the query parameter or returning all the tasks created if no query is sent",
         response_model=Dict[uuid.UUID, TaskOut])

async def read_task(q: Optional[TaskStatusModel] = Query(
        None,
        alias="status",
        title="Query filter based on status",
        description="Used to return only the tasks with the status in question or all of then if no status is sent",
        example="Example: done, not_done"), db: DBSession = Depends(get_db)):
    return db.read_task(q)


@router.patch("/{task_id}",
           summary="Update Tasks",
           description="Used to update the description and the status of a task on the dictionary",
           response_description="Dictionary containing the altered task",
           response_model=TaskOut)

def update_task(*, task_id: uuid.UUID = Path(
        ...,
        description="The ID of the task to be altered",
        example="Example: 3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        task: TaskInUpdate, db: DBSession = Depends(get_db)):
    return db.update_task(task_id, task)


@router.delete("/{task_id}",
            summary="Delete Tasks",
            description="Used to delete a task on the dictionary",
            response_description="Dictionary containing all the remaining tasks",
            response_model=Dict[uuid.UUID, TaskOut])

def delete_task(*, task_id: uuid.UUID = Path(
        ...,
        description="The ID of the task to be deleted",
        example="Example: 3fa85f64-5717-4562-b3fc-2c963f66afa6"), 
        db: DBSession = Depends(get_db)):
    return db.delete_task(task_id)
