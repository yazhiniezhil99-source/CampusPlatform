
from datetime import datetime


def validate_booking(start_time, end_time, min_minutes=30, max_minutes=240):
    if end_time <= start_time:
        return False

    duration = (end_time - start_time).total_seconds() / 60

    if duration < min_minutes or duration > max_minutes:
        return False

    return True


def check_booking_overlap(db, facility_id, start_time, end_time):
    from app.models import Booking

    existing = db.query(Booking).filter(
        Booking.facility_id == facility_id,
        Booking.status != "CANCELLED",
        Booking.start_time <  end_time,
        Booking.end_time > start_time
    ).first()

    return existing is not None


def calculate_priority(impact, urgency):
    impact = impact.upper()
    urgency = urgency.upper()

    priority_map = {
        ("HIGH", "HIGH"): "CRITICAL",
        ("HIGH", "MEDIUM"): "HIGH",
        ("HIGH", "LOW"): "MEDIUM",
        ("MEDIUM", "HIGH"): "HIGH",
        ("MEDIUM", "MEDIUM"): "MEDIUM",
        ("MEDIUM", "LOW"): "LOW",
        ("LOW", "HIGH"): "MEDIUM",
        ("LOW", "MEDIUM"): "LOW",
        ("LOW", "LOW"): "LOW"
    }

    if (impact, urgency) not in priority_map:
        raise ValueError("Invalid impact or urgency")

    return priority_map[(impact, urgency)]


def check_sensor_alert(reading, threshold):
    return reading >= threshold


def validate_ticket_transition(current_status, new_status):
    allowed_transitions = {
        "OPEN": ["IN_PROGRESS", "CLOSED"],
        "IN_PROGRESS": ["OPEN", "RESOLVED"],
        "RESOLVED": ["CLOSED", "IN_PROGRESS"],
        "CLOSED": []
    }

    return new_status in allowed_transitions.get(current_status, [])


def authorize_action(role, action):
    permissions = {
        "STUDENT": ["create_booking", "create_ticket"],
        "FACULTY": ["create_booking", "create_ticket", "approve_booking"],
        "ADMIN": [
            "create_booking",
            "create_ticket",
            "approve_booking",
            "manage_facilities",
            "manage_tickets"
        ]
    }

    return action in permissions.get(role.upper(), [])
