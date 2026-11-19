
import pytest

from app.services import (
    validate_booking,
    calculate_priority,
    check_sensor_alert,
    validate_ticket_transition,
    authorize_action
)


# UNIT TEST 1: Minimum valid booking duration
def test_booking_minimum_duration():
    from datetime import datetime, timedelta

    start = datetime(2026, 11, 20, 10, 0)
    end = start + timedelta(minutes=30)

    assert validate_booking(start, end) is True


# UNIT TEST 2: Maximum valid booking duration
def test_booking_maximum_duration():
    from datetime import datetime, timedelta

    start = datetime(2026, 11, 20, 10, 0)
    end = start + timedelta(minutes=240)

    assert validate_booking(start, end) is True


# UNIT TEST 3: Booking shorter than minimum
def test_booking_below_minimum_duration():
    from datetime import datetime, timedelta

    start = datetime(2026, 11, 20, 10, 0)
    end = start + timedelta(minutes=29)

    assert validate_booking(start, end) is False


# UNIT TEST 4: Booking longer than maximum
def test_booking_above_maximum_duration():
    from datetime import datetime, timedelta

    start = datetime(2026, 11, 20, 10, 0)
    end = start + timedelta(minutes=241)

    assert validate_booking(start, end) is False


# UNIT TEST 5: Invalid booking time
def test_booking_end_before_start():
    from datetime import datetime, timedelta

    start = datetime(2026, 11, 20, 11, 0)
    end = start - timedelta(minutes=30)

    assert validate_booking(start, end) is False


# UNIT TEST 6: Critical maintenance priority
def test_critical_priority():
    assert calculate_priority("HIGH", "HIGH") == "CRITICAL"


# UNIT TEST 7: Invalid impact and urgency
def test_invalid_priority_input():
    with pytest.raises(ValueError):
        calculate_priority("URGENT", "HIGH")


# UNIT TEST 8: Sensor threshold boundary
def test_sensor_at_threshold():
    assert check_sensor_alert(80, 80) is True


# UNIT TEST 9: Sensor below threshold
def test_sensor_below_threshold():
    assert check_sensor_alert(79, 80) is False


# UNIT TEST 10: Valid ticket status transition
def test_valid_ticket_transition():
    assert validate_ticket_transition("OPEN", "IN_PROGRESS") is True


# UNIT TEST 11: Invalid ticket status transition
def test_invalid_ticket_transition():
    assert validate_ticket_transition("OPEN", "RESOLVED") is False


# UNIT TEST 12: Student permission
def test_student_cannot_approve_booking():
    assert authorize_action("STUDENT", "approve_booking") is False
