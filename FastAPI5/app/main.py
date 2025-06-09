from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Важно использовать абсолютные импорты от корня `app`
from . import models, schemas
from .database import engine, get_db

# Эта команда создает таблицы в базе данных при первом запуске
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Registry API")


@app.get("/")
def read_root():
    return {"message": "API is running"}


# --- API для должностей ---
@app.post("/positions/", response_model=schemas.Position, tags=["Positions"])
def create_position(position: schemas.PositionCreate, db: Session = Depends(get_db)):
    db_position = models.Position(title=position.title)
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position


@app.get("/positions/", response_model=List[schemas.Position], tags=["Positions"])
def read_positions(db: Session = Depends(get_db)):
    return db.query(models.Position).all()


# --- API для сотрудников ---
@app.post("/employees/", response_model=schemas.Employee, tags=["Employees"])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли должность
    db_position = db.query(models.Position).filter(models.Position.id == employee.position_id).first()
    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")

    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.get("/employees/", response_model=List[schemas.Employee], tags=["Employees"])
def read_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()