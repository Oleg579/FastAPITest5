from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинты для должностей остаются без изменений
@app.post("/positions/", response_model=schemas.Position)
def create_position(position: schemas.PositionCreate, db: Session = Depends(get_db)):
    db_position = models.Position(title=position.title)
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

@app.get("/positions/", response_model=list[schemas.Position])
def read_positions(db: Session = Depends(get_db)):
    return db.query(models.Position).all()

# Обновленные эндпоинты для сотрудников
@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = models.Employee(
        full_name=employee.full_name,
        position_id=employee.position_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/", response_model=list[schemas.Employee])
def read_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()