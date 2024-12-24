import pytest
import requests
import random
import string

# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

def create_get_id_attendee():
    # Make random attendee
    random_mispar_ishi = str(random.randrange(10000, 9999999))
    random_tehudat_zehut = str(random.randrange(100000000, 999999999))
    random_name = ""
    for i in range(random.randrange(99)):
        random_name = random_name + random.choice(string.ascii_lowercase)
    random_name = random_name + " "
    for i in range(random.randrange(99)):
        random_name = random_name + random.choice(string.ascii_lowercase)
    valid_attendee = {"attendees":[{"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut, "full_name": random_name}]}
    # Create attendee
    response = requests.post(BASE_URL + "/create", json=valid_attendee)
    status = response.status_code
    data = response.json()
    assert status == 201
    assert len(data["data"]["successfull"]["mispar_ishi"]) == 1
    # Get id attendee
    response = requests.get(BASE_URL + "/getattendees")
    assert response.status_code == 200
    data = response.json()["data"]
    id_to_edit = None
    for attendee in data:
        if attendee["full_name"].lower() == random_name:
            id_to_edit = attendee["id"]
            break
    assert id_to_edit is not None
    return id_to_edit

# Helper function to send PUT requests for editing attendees
def edit_attendees(sent=None):
    if sent is None:
        sent = {}
    response = requests.put(BASE_URL + "/edit", json=sent)
    return response.status_code, response.json()

@pytest.fixture
def random_data_edit():
    random_id = random.randint(1, 1000)
    random_mispar_ishi = str(random.randrange(10000, 9999999))
    random_tehudat_zehut = str(random.randrange(100000000, 999999999))
    return random_id, random_mispar_ishi, random_tehudat_zehut

# Test cases
def test_edit_attendees_missing_id():
    status, data = edit_attendees(sent={"full_name": "Updated Name"})
    assert status == 400
    assert data["error_code"] == 102

def test_edit_attendees_no_fields_to_update():
    status, data = edit_attendees(sent={"id": 1})
    assert status == 400
    assert data["error_code"] == 101

def test_edit_attendees_invalid_id():
    status, data = edit_attendees(sent={"id": "invalid", "full_name": "Updated Name"})
    assert status == 400
    assert data["error_code"] == 102

def test_edit_attendees_valid_id_update_name(random_data_edit):
    id_to_edit = create_get_id_attendee()
    status, _ = edit_attendees(sent={"id": id_to_edit, "full_name": "Updated Name"})
    assert status == 200


def test_edit_attendees_invalid_mispar_ishi(random_data_edit):
    random_id, _, _ = random_data_edit
    status, data = edit_attendees(sent={"id": random_id, "mispar_ishi": "123"})
    assert status == 400
    assert data["error_code"] == 3

def test_edit_attendees_invalid_tehudat_zehut(random_data_edit):
    random_id, _, _ = random_data_edit
    status, data = edit_attendees(sent={"id": random_id, "tehudat_zehut": "12345"})
    assert status == 400
    assert data["error_code"] == 4

def test_edit_attendees_valid_id_update_multiple_fields(random_data_edit):
    id_to_edit = create_get_id_attendee()
    random_id, random_mispar_ishi, random_tehudat_zehut = random_data_edit
    status, data = edit_attendees(
        sent={
            "id": id_to_edit,
            "mispar_ishi": random_mispar_ishi,
            "tehudat_zehut": random_tehudat_zehut,
            "full_name": "Updated Name",
            "arrived": True,
        }
    )
    assert status == 200

def test_edit_attendees_missing_field_validation_error(random_data_edit):
    random_id, _, _ = random_data_edit
    status, data = edit_attendees(
        sent={
            "id": random_id,
            "mispar_ishi": "",
        }
    )
    assert status == 400
    assert data["error_code"] == 3

def test_edit_attendees_database_not_found():
    status, data = edit_attendees(sent={"id": 999999, "full_name": "Name Not Found"})
    assert status == 400
    assert data["error_code"] == 101

