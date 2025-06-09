from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Схемы Pydantic
class PositionCreate(BaseModel):
    title: str

class EmployeeCreate(BaseModel):
    full_name: str
    position_id: int

@app.post("/positions/")
def create_position(position: PositionCreate, db: Session = Depends(database.get_db)):
    db_position = models.Position(title=position.title)
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

@app.get("/positions/")
def read_positions(db: Session = Depends(database.get_db)):
    return db.query(models.Position).all()

@app.post("/employees/")
def create_employee(employee: EmployeeCreate, db: Session = Depends(database.get_db)):
    db_employee = models.Employee(
        full_name=employee.full_name,
        position_id=employee.position_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/")
def read_employees(db: Session = Depends(database.get_db)):
    return db.query(models.Employee).all()