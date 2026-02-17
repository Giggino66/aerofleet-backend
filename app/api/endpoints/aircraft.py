"""Aircraft endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.aircraft import Aircraft
from app.schemas.aircraft import AircraftCreate, AircraftUpdate, AircraftResponse, MessageResponse

router = APIRouter(prefix="/aircraft", tags=["Aircraft"])


@router.get("", response_model=List[AircraftResponse])
def list_aircraft(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all aircraft"""
    aircraft = db.query(Aircraft).filter(
        Aircraft.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()
    
    return aircraft


@router.get("/{aircraft_id}", response_model=AircraftResponse)
def get_aircraft(
    aircraft_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get aircraft by ID"""
    aircraft = db.query(Aircraft).filter(
        Aircraft.id == aircraft_id,
        Aircraft.deleted_at.is_(None)
    ).first()
    
    if not aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    
    return aircraft


@router.post("", response_model=MessageResponse, status_code=201)
def create_aircraft(
    aircraft_data: AircraftCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new aircraft"""
    
    # Check role
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Check if exists
    if db.query(Aircraft).filter(Aircraft.registration == aircraft_data.registration).first():
        raise HTTPException(status_code=409, detail="Aircraft already exists")
    
    # Create
    aircraft = Aircraft(**aircraft_data.model_dump())
    db.add(aircraft)
    db.commit()
    db.refresh(aircraft)
    
    return {"message": "Aircraft created", "id": aircraft.id}


@router.put("/{aircraft_id}", response_model=MessageResponse)
def update_aircraft(
    aircraft_id: str,
    aircraft_data: AircraftUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update aircraft"""
    
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    aircraft = db.query(Aircraft).filter(
        Aircraft.id == aircraft_id,
        Aircraft.deleted_at.is_(None)
    ).first()
    
    if not aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    
    # Update
    for field, value in aircraft_data.model_dump(exclude_unset=True).items():
        setattr(aircraft, field, value)
    
    db.commit()
    
    return {"message": "Aircraft updated", "id": aircraft.id}


@router.delete("/{aircraft_id}", status_code=204)
def delete_aircraft(
    aircraft_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete aircraft"""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    
    aircraft = db.query(Aircraft).filter(
        Aircraft.id == aircraft_id,
        Aircraft.deleted_at.is_(None)
    ).first()
    
    if not aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    
    from datetime import datetime
    aircraft.deleted_at = datetime.utcnow()
    db.commit()
