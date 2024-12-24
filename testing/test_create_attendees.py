import pytest
import requests
import random

# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

# Helper function to send POST requests
def create_attendees(sent=None, testing=None):
    if sent is None:
        sent = {}
    payload = {"attendees": sent.get("attendees", [])}
    if testing:
        payload["testing"] = testing
    response = requests.post(BASE_URL + "/create", json=payload)
    return response.status_code, response.json()

@pytest.fixture
def random_data_create():
    random_mispar_ishi = str(random.randrange(10000, 9999999))
    random_tehudat_zehut = str(random.randrange(100000000, 999999999))
    return random_mispar_ishi, random_tehudat_zehut

# Test cases

def test_create_attendees_missing_attendees():
    status, data = create_attendees(sent={})
    assert status == 400
    assert data["error_code"] == 101

def test_create_attendees_empty_attendees():
    status, data = create_attendees(sent={"attendees": []})
    assert status == 400
    assert data["error_code"] == 101

def test_create_attendees_invalid_attendee():
    invalid_attendee = [{"mispar_ishi": "12345"}]
    status, data = create_attendees(sent={"attendees": invalid_attendee})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4


def test_create_attendees_duplicate_attendee():
    duplicate_attendee = [{"mispar_ishi": "1234567", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    create_attendees(sent={"attendees": duplicate_attendee})
    status, data = create_attendees(sent={"attendees": duplicate_attendee})
    assert status == 400
    assert len(data["data"]["already_database"]["mispar_ishi"]) == 1

def test_create_attendees_missing_name():
    attendee_no_name = [{"mispar_ishi": "1234567", "tehudat_zehut": "123456789"}]
    status, data = create_attendees(sent={"attendees": attendee_no_name})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_invalid_name():
    invalid_name = [{"mispar_ishi": "1234567", "tehudat_zehut": "123456789", "full_name": "J0hn D0e!"}]
    status, data = create_attendees(sent={"attendees": invalid_name})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 1

def test_create_attendees_invalid_mispar_ishi():
    invalid_mispar_ishi = [{"mispar_ishi": "123", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 3

def test_create_attendees_invalid_tehudat_zehut():
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "12345678", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_mixed_valid_and_invalid(random_data_create):
    random_mispar_ishi, random_tehudat_zehut = random_data_create
    mixed_attendees = [
        {"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut, "full_name": "John Doe"},
        {"mispar_ishi": "123", "tehudat_zehut": "123456789", "full_name": "Invalid Mispar"}
    ]
    status, data = create_attendees(sent={"attendees": mixed_attendees})
    assert status == 201
    assert len(data["data"]["misssing_data"]) == 1
    assert len(data["data"]["successfull"]["mispar_ishi"]) == 1

def test_create_attendees_large_input(random_data_create):
    random_mispar_ishi, random_tehudat_zehut = random_data_create
    large_input = [{"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut, "full_name": "John Doe"} for i in range(100)]
    status, data = create_attendees(sent={"attendees": large_input}, testing="Ok")
    assert status == 201
    assert len(data["data"]["successfull"]["mispar_ishi"]) == 100

def test_create_attendees_invalid_mispar_ishi_leading_zeros(random_data_create):
    random_mispar_ishi, random_tehudat_zehut = random_data_create
    invalid_mispar_ishi = [{"mispar_ishi": "00123", "tehudat_zehut": random_tehudat_zehut, "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 3

def test_create_attendees_invalid_tehudat_zehut_leading_zeros():
    # tehudat_zehut is passed as a string to preserve the leading zeros
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "001234567", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_tehudat_zehut, "testing":"zeros"})
    assert status == 201
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_invalid_mispar_ishi_too_few_digits():
    invalid_mispar_ishi = [{"mispar_ishi": "123", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 3

def test_create_attendees_invalid_tehudat_zehut_too_few_digits():
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "12345678", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_invalid_tehudat_zehut_too_many_digits():
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "123456789012", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_invalid_mispar_ishi_leading_zeros():
    # mispar_ishi is passed as a string to preserve the leading zeros
    invalid_mispar_ishi = [{"mispar_ishi": "00123", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 3

def test_create_attendees_invalid_tehudat_zehut_leading_zeros():
    # tehudat_zehut is passed as a string to preserve the leading zeros
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "00123456789", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_invalid_mispar_ishi_too_few_digits():
    # mispar_ishi has too few digits (3 digits)
    invalid_mispar_ishi = [{"mispar_ishi": "123", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 3

def test_create_attendees_invalid_tehudat_zehut_too_few_digits():
    # tehudat_zehut has too few digits (8 digits)
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "12345678", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_invalid_tehudat_zehut_too_many_digits():
    # tehudat_zehut has too many digits (12 digits)
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "123456789012", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_invalid_mispar_ishi_invalid_characters():
    # mispar_ishi has invalid characters (alphabetical)
    invalid_mispar_ishi = [{"mispar_ishi": "ABC123456", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 3

def test_create_attendees_valid_attendee(random_data_create):
    random_mispar_ishi, random_tehudat_zehut = random_data_create   
    valid_attendee = [{"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut, "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": valid_attendee})
    assert status == 201
    assert len(data["data"]["successfull"]["mispar_ishi"]) == 1