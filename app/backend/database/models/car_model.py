from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, Column, Integer, SQLModel, Sequence, func
from app.backend.database.models.parking_lot_model import ParkingLot

class PlanTypeEnum(str, Enum):
    MONTHLY = "monthly"
    LOOSE = "loose"

class Car(SQLModel, table=True):
    """ Car model/schema """
    __tablename__ = 'car'

    id: Optional[int] = Field(sa_column=Column(Integer(), Sequence('car_id_seq'), primary_key=True))
    parking_lot_id: Optional[int] = Field(nullable=False, foreign_key="parking_lot.id")
    license_plate: Optional[str] = Field(max_length=7, nullable=False)
    plan_type: Optional[PlanTypeEnum] = Field(default=PlanTypeEnum.LOOSE) 
    entry_time: Optional[datetime] = Field(default=datetime.now(), sa_column_kwargs={"server_default": func.now()}, nullable=True)
    exit_time: Optional[datetime] = Field(nullable=True)
    total_priece: Optional[float] = Field(default=0.0)
    created_by: Optional[str] = Field(max_length=255, nullable=True)
    exit_by: Optional[str] = Field(max_length=255, nullable=True)

