from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import engine, SessionLocal, Base
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/todos", response_model=list[schemas.TodoResponse])
def get_todos(filter: Optional[str] = Query("all", description="all/completed/uncompleted"), db: Session = Depends(get_db)):
    query = db.query(models.Todo)
    if filter == "completed":
        query = query.filter(models.Todo.completed == True)
    elif filter == "uncompleted":
        query = query.filter(models.Todo.completed == False)
    return query.all()

@app.post("/todos", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{id}", response_model=schemas.TodoResponse)
def update_todo(id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not db_todo:
        raise HTTPException(404, "Todo not found")
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not db_todo:
        raise HTTPException(404, "Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"ok": True}

@app.delete("/todos")
def clear_todos(action: str = Query("completed", description="completed/all"), db: Session = Depends(get_db)):
    if action == "completed":
        db.query(models.Todo).filter(models.Todo.completed == True).delete()
    else:
        db.query(models.Todo).delete()
    db.commit()
    return {"ok": True}
