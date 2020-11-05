from pydantic import BaseModel, Field
from enum import Enum
import uuid

class TaskIn(BaseModel):
    name: str = Field(
        description="Name of the task (user imput)",
    )
    description: str = Field(
        description="Description of the task (user imput)",
    )


class TaskOut(BaseModel):
    task_id: uuid.UUID = Field(
        description="Id of the task (UUID)",
    )
    name: str = Field(
        description="Name of the task",
    )
    description: str = Field(
        description="Description of the task",
    )
    status: bool = Field(
        description="Status of the task (done or not done yet)",
        example="True, False"
    )


class TaskInUpdate(BaseModel):
    description: str = Field(
        description="Description of the task",
    )
    status: bool = Field(
        description="Status of the task (done or not done yet)",
        example="True, False"
    )


class TaskStatusModel(str, Enum):
    done = "done"
    not_done = "not_done"