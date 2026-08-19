from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app=FastAPI()

class Todo(BaseModel):
    task:str
    completed: bool=False

todos_db={}
next_id=1

@app.get('/')
def read_root():
    return {"message" : "Todo API is running"}

@app.post("/todos", status_code=201)
def create_todo(todo:Todo):
    global next_id

    new_todo={
        "id" : next_id,
        "task" : todo.task,
        "completed" : todo.completed
    }

    todos_db[next_id]=new_todo
    next_id+=1
    return new_todo

@app.get("/todos")
def get_all_todos():
    return list(todos_db.values())

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[todo_id]

@app.put("/todos/{todo_id}")
def update_todo(todo_id:int, todo: Todo):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated_todos={
        "id": todo_id,
        "task": todo.task,
        "completed": todo.completed
    }
    todos_db[todo_id]=updated_todos
    return updated_todos

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id:int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_db[todo_id]
    return {"message": "Todo deleted successfully"}