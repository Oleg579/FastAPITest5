from pydantic import BaseModel, Field
from typing import Optional

# Базовые схемы для создания (без id)
class PositionCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)

class EmployeeCreate(BaseModel):
    full_name: str = Field(..., min_length=5, max_length=150)
    position_id: int = Field(..., gt=0)

# Схемы для ответа (с id)
class Position(PositionCreate):
    id: int
    class Config:
        orm_mode = True

class Employee(EmployeeCreate):
    id: int
    class Config:
        orm_mode = True