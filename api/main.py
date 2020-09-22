from fastapi import FastAPI
from .routers import task

app = FastAPI(
    title="APS2",
    description="Megadados APS2 - Creating a REST interface",
)
app.include_router(
    task.router,
    prefix='/task',
    tags=['task']
)