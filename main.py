from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import engine, get_db, Base
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def read_root():
    return {"message": "Todo API is running"}


@app.post("/todos", status_code=201, response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    new_todo = models.Todo(task=todo.task, completed=todo.completed)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.get("/todos", response_model=list[schemas.TodoResponse])
def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return todos


@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    existing_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    existing_todo.task = todo.task
    existing_todo.completed = todo.completed

    db.commit()
    db.refresh(existing_todo)
    return existing_todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return None