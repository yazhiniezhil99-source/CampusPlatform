
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Facility, Booking, MaintenanceTicket, SensorEvent
from app.services import (
    validate_booking,
    check_booking_overlap,
    calculate_priority,
    check_sensor_alert,
    validate_ticket_transition,
    authorize_action
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Campus Facility and Maintenance Platform",
    version="1.0.0"
)


class FacilityInput(BaseModel):
    name: str
    facility_type: str


class BookingInput(BaseModel):
    facility_id: int
    start_time: datetime
    end_time: datetime


class TicketInput(BaseModel):
    title: str
    description: str
    impact: str
    urgency: str


class SensorInput(BaseModel):
    sensor_name: str
    reading: float
    threshold: float


class StatusInput(BaseModel):
    status: str


@app.get("/")
def home():
    return {
        "message": "Smart Campus Platform API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/facilities")
def create_facility(
    data: FacilityInput,
    db: Session = Depends(get_db),
    role: str = Header(default="ADMIN", alias="X-Role")
):
    if not authorize_action(role, "manage_facilities"):
        raise HTTPException(status_code=403, detail="Access denied")

    facility = Facility(
        name=data.name,
        facility_type=data.facility_type
    )
    db.add(facility)
    db.commit()
    db.refresh(facility)

    return {"message": "Facility created", "facility_id": facility.id}


@app.get("/facilities")
def get_facilities(db: Session = Depends(get_db)):
    return db.query(Facility).all()


@app.post("/bookings")
def create_booking(
    data: BookingInput,
    db: Session = Depends(get_db),
    role: str = Header(default="STUDENT", alias="X-Role"),
    user: str = Header(default="student1", alias="X-User")
):
    if not authorize_action(role, "create_booking"):
        raise HTTPException(status_code=403, detail="Access denied")

    facility = db.query(Facility).filter(
        Facility.id == data.facility_id
    ).first()

    if not facility or not facility.is_available:
        raise HTTPException(status_code=404, detail="Facility unavailable")

    if not validate_booking(data.start_time, data.end_time):
        raise HTTPException(status_code=400, detail="Invalid booking duration")

    if check_booking_overlap(
        db, data.facility_id, data.start_time, data.end_time
    ):
        raise HTTPException(status_code=409, detail="Booking time overlaps")

    booking = Booking(
        facility_id=data.facility_id,
        booked_by=user,
        start_time=data.start_time,
        end_time=data.end_time
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {"message": "Booking created", "booking_id": booking.id}


@app.get("/bookings")
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()


@app.post("/tickets")
def create_ticket(
    data: TicketInput,
    db: Session = Depends(get_db),
    role: str = Header(default="STUDENT", alias="X-Role")
):
    if not authorize_action(role, "create_ticket"):
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        priority = calculate_priority(data.impact, data.urgency)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    ticket = MaintenanceTicket(
        title=data.title,
        description=data.description,
        impact=data.impact.upper(),
        urgency=data.urgency.upper(),
        priority=priority
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {
        "message": "Maintenance ticket created",
        "ticket_id": ticket.id,
        "priority": ticket.priority
    }


@app.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    return db.query(MaintenanceTicket).all()


@app.patch("/tickets/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    data: StatusInput,
    db: Session = Depends(get_db),
    role: str = Header(default="STUDENT", alias="X-Role")
):
    if not authorize_action(role, "manage_tickets"):
        raise HTTPException(status_code=403, detail="Access denied")

    ticket = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    new_status = data.status.upper()

    if not validate_ticket_transition(ticket.status, new_status):
        raise HTTPException(status_code=400, detail="Invalid status transition")

    ticket.status = new_status
    db.commit()

    return {"message": "Ticket status updated", "status": ticket.status}


@app.post("/sensors")
def record_sensor_event(
    data: SensorInput,
    db: Session = Depends(get_db),
    role: str = Header(default="ADMIN", alias="X-Role")
):
    if not authorize_action(role, "manage_facilities"):
        raise HTTPException(status_code=403, detail="Access denied")

    alert = check_sensor_alert(data.reading, data.threshold)

    event = SensorEvent(
        sensor_name=data.sensor_name,
        reading=data.reading,
        threshold=data.threshold,
        alert_triggered=alert
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return {
        "message": "Sensor reading recorded",
        "alert_triggered": alert,
        "event_id": event.id
    }


@app.get("/sensors")
def get_sensor_events(db: Session = Depends(get_db)):
    return db.query(SensorEvent).all()
