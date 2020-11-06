# pylint: disable=missing-module-docstring,missing-class-docstring
from typing import Optional

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


# pylint: disable=too-few-public-methods
class Task(BaseModel):
    description: Optional[str] = Field(
        'no description',
        title='Task description',
        max_length=1024,
    )
    completed: Optional[bool] = Field(
        False,
        title='Shows whether the task was completed',
    )
    user_id : Optional[str] = Field(
        False,
        title='User ID',
    )

    class Config:
        schema_extra = {
            'example': {
                'description': 'Buy baby diapers',
                'completed': False,
                'user_id': "06abfdbe-5a1d-488b-b13a-accb3e7f3c23",
            }
        }


#Create User Model
class User(BaseModel):
    username: Optional[str] = Field(
        'no description',
        title='User description',
        max_length=1024,
    )

    class Config:
        schema_extra = {
            'example': {
                'username': 'gabilu123'
            }
        }
