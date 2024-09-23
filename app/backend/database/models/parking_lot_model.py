from datetime import datetime
from typing import Optional
from sqlmodel import Field, Column, Integer, SQLModel, Sequence, func


class ParkingLot(SQLModel, table=True):
    """ Parking Lot model/schema """
    __tablename__ = 'parking_lot'

    id: Optional[int] = Field(sa_column=Column(Integer(), Sequence('parking_lot_id_seq'), primary_key=True))
    name: Optional[str] = Field(max_length=256, nullable=True)
    email: Optional[str] = Field(max_length=256, index=True, nullable=True)
    is_active: bool = Field(default=True)
    spots: Optional[int] = Field(default=0)
    start_priece: Optional[float] = Field(default=0.0)
    extra_priece: Optional[float] = Field(default=0.0)
    allowed_time: Optional[int] = Field(default=0)
    cashier: Optional[float] = Field(default=0.0)
    
    created_date: Optional[datetime] = Field(default=datetime.now(), sa_column_kwargs={"server_default": func.now()}, nullable=True)
    created_by: Optional[str] = Field(max_length=255, nullable=True)
    updated_date: Optional[datetime] = Field(default=datetime.now(), nullable=True)
    updated_by: Optional[str] = Field(max_length=255, nullable=True)


class ParkingLotHistory(SQLModel, table=True):
    """ Parking Lot History model/schema """
    __tablename__ = 'parking_lot_history'

    id: Optional[int] = Field(sa_column=Column(Integer(), Sequence('parking_lot_history_id_seq'), primary_key=True))
    parking_lot_id: Optional[int] = Field(nullable=False, foreign_key="parking_lot.id")
    name: Optional[str] = Field(max_length=256, nullable=True)
    email: Optional[str] = Field(max_length=256, index=True, nullable=True)
    is_active: bool = Field(default=True)
    spots: Optional[int] = Field(default=0)
    start_priece: Optional[float] = Field(default=0.0)
    extra_priece: Optional[float] = Field(default=0.0)
    allowed_time: Optional[int] = Field(default=0)
    cashier: Optional[float] = Field(default=0.0)
    created_date: Optional[datetime] = Field(default=datetime.now(), sa_column_kwargs={"server_default": func.now()}, nullable=True)
    created_by: Optional[str] = Field(max_length=255, nullable=True)