from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    task: str
    completed: bool = False


class TodoResponse(BaseModel):
    id: int
    task: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)