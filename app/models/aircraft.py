from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base


class Aircraft(Base):
    __tablename__ = "aircraft"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration = Column(String(10), unique=True, nullable=False, index=True)
    model = Column(String(100), nullable=False)
    manufacturer = Column(String(100), nullable=False)
    serial_number = Column(String(50), unique=True, nullable=False)
    year_manufactured = Column(Integer)
    total_hours = Column(Numeric(10, 2), default=0, nullable=False)
    total_cycles = Column(Integer, default=0, nullable=False)
    status = Column(String(20), default="operational", nullable=False)
    owner = Column(String(200))
    insurance_policy = Column(String(100))
    insurance_expiry = Column(Date)
    coa_number = Column(String(50))
    coa_issue_date = Column(Date)
    coa_expiry_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
