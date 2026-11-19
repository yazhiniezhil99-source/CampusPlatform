
# REGRESSION TESTS

# TEST 1: Booking shorter than 30 minutes must remain rejected
def test_short_booking_rejected(client):
    facility = client.post(
        "/facilities",
        headers={"X-Role": "ADMIN"},
        json={
            "name": "Regression Room",
            "facility_type": "ROOM"
        }
    )

    facility_id = facility.json()["facility_id"]

    response = client.post(
        "/bookings",
        headers={"X-Role": "STUDENT"},
        json={
            "facility_id": facility_id,
            "start_time": "2026-11-20T10:00:00",
            "end_time": "2026-11-20T10:29:00"
        }
    )

    assert response.status_code == 400


# TEST 2: Invalid impact must not create a ticket
def test_invalid_ticket_impact_rejected(client):
    response = client.post(
        "/tickets",
        headers={"X-Role": "STUDENT"},
        json={
            "title": "Invalid test ticket",
            "description": "Testing invalid impact",
            "impact": "EXTREME",
            "urgency": "HIGH"
        }
    )

    assert response.status_code == 400


# TEST 3: Invalid ticket transition must remain rejected
def test_invalid_ticket_transition_rejected(client):
    ticket = client.post(
        "/tickets",
        headers={"X-Role": "STUDENT"},
        json={
            "title": "Regression ticket",
            "description": "Testing status transition",
            "impact": "MEDIUM",
            "urgency": "MEDIUM"
        }
    )

    ticket_id = ticket.json()["ticket_id"]

    response = client.patch(
        f"/tickets/{ticket_id}/status",
        headers={"X-Role": "ADMIN"},
        json={"status": "RESOLVED"}
    )

    assert response.status_code == 400


# TEST 4: Student must not update ticket status
def test_student_ticket_update_remains_blocked(client):
    ticket = client.post(
        "/tickets",
        headers={"X-Role": "STUDENT"},
        json={
            "title": "Access control test",
            "description": "Student must not update status",
            "impact": "LOW",
            "urgency": "LOW"
        }
    )

    ticket_id = ticket.json()["ticket_id"]

    response = client.patch(
        f"/tickets/{ticket_id}/status",
        headers={"X-Role": "STUDENT"},
        json={"status": "IN_PROGRESS"}
    )

    assert response.status_code == 403
