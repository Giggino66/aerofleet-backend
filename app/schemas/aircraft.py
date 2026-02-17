from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID


class AircraftCreate(BaseModel):
    registration: str
    model: str
    manufacturer: str
    serial_number: str
    year_manufactured: Optional[int] = None
    total_hours: Decimal = Decimal("0.0")
    total_cycles: int = 0
    status: str = "operational"
    owner: Optional[str] = None
    insurance_policy: Optional[str] = None
    insurance_expiry: Optional[date] = None
    coa_number: Optional[str] = None
    coa_issue_date: Optional[date] = None
    coa_expiry_date: Optional[date] = None
    notes: Optional[str] = None


class AircraftUpdate(BaseModel):
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    status: Optional[str] = None
    owner: Optional[str] = None
    insurance_policy: Optional[str] = None
    insurance_expiry: Optional[date] = None
    coa_number: Optional[str] = None
    coa_expiry_date: Optional[date] = None
    notes: Optional[str] = None


class AircraftResponse(BaseModel):
    id: UUID
    registration: str
    model: str
    manufacturer: str
    serial_number: str
    year_manufactured: Optional[int] = None
    total_hours: Decimal
    total_cycles: int
    status: str
    owner: Optional[str] = None
    insurance_expiry: Optional[date] = None
    coa_expiry_date: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    # from_attributes enables ORM mode in Pydantic v2
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str
    id: Optional[UUID] = None
