from .models import (TaskIn, TaskOut, TaskInUpdate, TaskStatusModel)
from fastapi import HTTPException
import uuid

class DBSession:
    fake_db = {}

    def __init__(self):
        self.fake_db = DBSession.fake_db

    def create_task(self, task):

        id = uuid.uuid4()

        task_out_db = TaskOut(**task.dict(), status=False, task_id=id)
        self.fake_db.update({id: task_out_db})

        return task_out_db

    def read_task(self, q = None):

        q_dict = {}

        if q != None:
            for task in self.fake_db.values():

                if task.status and q == TaskStatusModel.done:
                    q_dict.update({task.task_id: task})

                elif not task.status and q == TaskStatusModel.not_done:
                    q_dict.update({task.task_id: task})

            return q_dict
        else:
            return self.fake_db

    def update_task(self, task_id, task):

        if task_id not in self.fake_db:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            )

        task_db = self.fake_db.get(task_id)
        update_data = task_db.dict(exclude_unset=True)
        update_data.update(**task.dict())
        task_out = TaskOut(**update_data)
        self.fake_db.update({task_id: task_out})

        return task_out

    def delete_task(self, task_id):
        try:
            task_db = self.fake_db.get(task_id)
            del self.fake_db[task_id]

        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception

        return self.fake_db

def get_db():
    return DBSession()
