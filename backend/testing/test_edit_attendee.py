import pytest
import requests
import random
import string
from testing.test_create_attendees import create_get_id_attendee

# Add mock for testing database error

# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

# Helper function to send PUT requests for editing attendees
def edit_attendees(sent=None):
    if sent is None:
        sent = {}
    response = requests.put(BASE_URL + "/edit", json=sent)
    return response.status_code, response.json()

@pytest.fixture
def random_data_edit():
    random_id = random.randint(1, 1000)
    random_mispar_ishi = str(random.randrange(100000, 9999999))
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

def test_edit_attendees_valid_id_update_name():
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

def test_edit_attendees_invalid_arrived():
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(sent={"id": id_to_edit, "arrived": "yes"})
    assert status == 400
    assert data["error_code"] == 101  # Error por tipo de dato inválido

def test_edit_attendees_valid_arrived_true():
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(sent={"id": id_to_edit, "arrived": True})
    assert status == 200

def test_edit_attendees_valid_arrived_false():
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(sent={"id": id_to_edit, "arrived": False})
    assert status == 200

def test_edit_attendees_invalid_date_format():
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(sent={"id": id_to_edit, "date_arrived": "2023-13-32"})
    assert status == 400
    assert data["error_code"] == 5

def test_edit_attendees_invalid_date_type():
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(sent={"id": id_to_edit, "date_arrived": 123456789})
    assert status == 400
    assert data["error_code"] == 5

def test_edit_attendees_null_date():
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(sent={"id": id_to_edit, "date_arrived": None})
    assert status == 400
    assert data["error_code"] == 5

def test_edit_attendees_valid_date():
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(sent={"id": id_to_edit, "date_arrived": "2023-12-15 10:00:00"})
    assert status == 200

def test_edit_attendees_update_all_fields_double_mispar_ishi(random_data_edit):
    _, random_mispar_ishi, random_tehudat_zehut = random_data_edit
    create_get_id_attendee(mispar_ishi_sent=random_mispar_ishi)
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(
        sent={
            "id": id_to_edit,
            "mispar_ishi": random_mispar_ishi,
            "tehudat_zehut": random_tehudat_zehut,
            "full_name": "Updated Name",
            "arrived": True,
            "date_arrived": "2023-12-15 10:00:00",
        }
    )
    assert status == 400
    assert data["error_code"] == 3

def test_edit_attendees_update_all_fields_double_tehudat_zehut(random_data_edit):
    _, random_mispar_ishi, random_tehudat_zehut = random_data_edit
    create_get_id_attendee(tehudat_zehut=random_tehudat_zehut)
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(
        sent={
            "id": id_to_edit,
            "mispar_ishi": random_mispar_ishi,
            "tehudat_zehut": random_tehudat_zehut,
            "full_name": "Updated Name",
            "arrived": True,
            "date_arrived": "2023-12-15 10:00:00",
        }
    )
    assert status == 400
    assert data["error_code"] == 4

def test_edit_attendees_update_all_fields(random_data_edit):
    _, random_mispar_ishi, random_tehudat_zehut = random_data_edit
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(
        sent={
            "id": id_to_edit,
            "mispar_ishi": random_mispar_ishi,
            "tehudat_zehut": random_tehudat_zehut,
            "full_name": "Updated Name",
            "arrived": True,
            "date_arrived": "2023-12-15 10:00:00",
        }
    )
    assert status == 200

def test_edit_attendees_invalid_combined_fields():
    id_to_edit = create_get_id_attendee()
    status, data = edit_attendees(
        sent={
            "id": id_to_edit,
            "mispar_ishi": "123",
            "tehudat_zehut": "12345678",
            "full_name": "J0hn D0e!",
            "arrived": "yes",
            "date_arrived": "2023-13-32",  
        }
    )
    assert status == 400
    assert data["error_code"] == 3


def test_edit_attendees_database_not_found():
    status, data = edit_attendees(sent={"id": 999999, "full_name": "Name Not Found"})
    assert status == 400
    assert data["error_code"] == 101

