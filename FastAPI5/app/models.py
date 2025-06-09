from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    employees = relationship("Employee", back_populates="position")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False)
    position = relationship("Position", back_populates="employees")