"""Aircraft schemas"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID


class AircraftBase(BaseModel):
    registration: str
    model: str
    manufacturer: str
    serial_number: str
    year_manufactured: Optional[int] = None
    status: str = "operational"
    owner: Optional[str] = None
    insurance_policy: Optional[str] = None
    insurance_expiry: Optional[date] = None
    coa_number: Optional[str] = None
    coa_issue_date: Optional[date] = None
    coa_expiry_date: Optional[date] = None
    notes: Optional[str] = None


class AircraftCreate(AircraftBase):
    total_hours: Decimal = Decimal("0.0")
    total_cycles: int = 0


class AircraftUpdate(BaseModel):
    registration: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AircraftResponse(AircraftBase):
    id: UUID
    total_hours: Decimal
    total_cycles: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str
    id: Optional[UUID] = None
