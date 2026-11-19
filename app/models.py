
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    facility_type = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id"), nullable=False)
    booked_by = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="PENDING")


class MaintenanceTicket(Base):
    __tablename__ = "maintenance_tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    impact = Column(String, nullable=False)
    urgency = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class SensorEvent(Base):
    __tablename__ = "sensor_events"

    id = Column(Integer, primary_key=True, index=True)
    sensor_name = Column(String, nullable=False)
    reading = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    alert_triggered = Column(Boolean, default=False)
    received_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
