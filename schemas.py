from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class TodoCreate(BaseModel):
    task: str
    completed: bool = False


class TodoResponse(BaseModel):
    id: int
    task: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)