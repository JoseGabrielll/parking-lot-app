from datetime import date, datetime
from typing import Optional
from sqlmodel import Field, Column, Integer, SQLModel, Sequence, func


class MonthlyCar(SQLModel, table=True):
    """ MonthlyCar model/schema """
    __tablename__ = 'monthly_car'

    id: Optional[int] = Field(sa_column=Column(Integer(), Sequence('monthly_car_id_seq'), primary_key=True))
    license_plate: Optional[str] = Field(max_length=7, nullable=False)
    priece: Optional[float] = Field(default=0.0)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    created_date: Optional[datetime] = Field(default=datetime.now(), sa_column_kwargs={"server_default": func.now()}, nullable=True)
    created_by: Optional[str] = Field(max_length=255, nullable=True)
    updated_date: Optional[datetime] = Field(default=datetime.now(), nullable=True)
    updated_by: Optional[str] = Field(max_length=255, nullable=True)


