
# INTEGRATION TESTS

# TEST 1: Health endpoint
def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# TEST 2: Admin can create a facility
def test_admin_creates_facility(client):
    response = client.post(
        "/facilities",
        headers={"X-Role": "ADMIN"},
        json={
            "name": "Computer Laboratory",
            "facility_type": "LAB"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Facility created"


# TEST 3: Student cannot create a facility
def test_student_cannot_create_facility(client):
    response = client.post(
        "/facilities",
        headers={"X-Role": "STUDENT"},
        json={
            "name": "Seminar Hall",
            "facility_type": "HALL"
        }
    )

    assert response.status_code == 403


# TEST 4: Student can create a valid booking
def test_student_creates_booking(client):
    facility_response = client.post(
        "/facilities",
        headers={"X-Role": "ADMIN"},
        json={
            "name": "Smart Classroom",
            "facility_type": "CLASSROOM"
        }
    )

    facility_id = facility_response.json()["facility_id"]

    response = client.post(
        "/bookings",
        headers={
            "X-Role": "STUDENT",
            "X-User": "student_test"
        },
        json={
            "facility_id": facility_id,
            "start_time": "2026-11-20T10:00:00",
            "end_time": "2026-11-20T11:00:00"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Booking created"


# TEST 5: Overlapping booking is rejected
def test_overlapping_booking_rejected(client):
    facility_response = client.post(
        "/facilities",
        headers={"X-Role": "ADMIN"},
        json={
            "name": "Meeting Room",
            "facility_type": "ROOM"
        }
    )

    facility_id = facility_response.json()["facility_id"]

    booking_data = {
        "facility_id": facility_id,
        "start_time": "2026-11-20T10:00:00",
        "end_time": "2026-11-20T11:00:00"
    }

    first = client.post(
        "/bookings",
        headers={"X-Role": "STUDENT"},
        json=booking_data
    )

    second = client.post(
        "/bookings",
        headers={"X-Role": "STUDENT"},
        json=booking_data
    )

    assert first.status_code == 200
    assert second.status_code == 409


# TEST 6: Maintenance ticket creation
def test_create_maintenance_ticket(client):
    response = client.post(
        "/tickets",
        headers={"X-Role": "STUDENT"},
        json={
            "title": "Projector not working",
            "description": "Projector in Room 101 is not turning on",
            "impact": "HIGH",
            "urgency": "HIGH"
        }
    )

    assert response.status_code == 200
    assert response.json()["priority"] == "CRITICAL"


# TEST 7: Sensor alert creation
def test_sensor_alert_creation(client):
    response = client.post(
        "/sensors",
        headers={"X-Role": "ADMIN"},
        json={
            "sensor_name": "Temperature Sensor",
            "reading": 85,
            "threshold": 80
        }
    )

    assert response.status_code == 200
    assert response.json()["alert_triggered"] is True


# TEST 8: Student cannot submit sensor readings
def test_student_cannot_submit_sensor_reading(client):
    response = client.post(
        "/sensors",
        headers={"X-Role": "STUDENT"},
        json={
            "sensor_name": "Temperature Sensor",
            "reading": 85,
            "threshold": 80
        }
    )

    assert response.status_code == 403
