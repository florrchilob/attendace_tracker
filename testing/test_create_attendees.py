import pytest
import requests
import random


# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

# Helper function to send POST requests

random_mispar_ishi = random.randrange(10000, 9999999)
random_tehudat_zehut = random.randrange(100000000, 999999999)

def create_attendees(sent=None, testing=None):
    if sent is None:
        sent = {}
    payload = {"attendees": sent.get("attendees", [])}
    if testing:
        payload["testing"] = testing
    response = requests.post(BASE_URL + "/create", json=payload)
    return response.status_code, response.json()

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
    invalid_attendee = [{"mispar_ishi": 12345}]
    status, data = create_attendees(sent={"attendees": invalid_attendee})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_valid_attendee():
    global random_mispar_ishi, random_tehudat_zehut
    valid_attendee = [{"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut, "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": valid_attendee})
    assert status == 201
    assert len(data["data"]["successfull"]["mispar_ishi"]) == 1

def test_create_attendees_duplicate_attendee():
    duplicate_attendee = [{"mispar_ishi": 1234567, "tehudat_zehut": 123456789, "full_name": "John Doe"}]
    create_attendees(sent={"attendees": duplicate_attendee})
    status, data = create_attendees(sent={"attendees": duplicate_attendee})
    assert status == 400
    assert len(data["data"]["already_database"]["mispar_ishi"]) == 1

def test_create_attendees_missing_name():
    attendee_no_name = [{"mispar_ishi": 1234567, "tehudat_zehut": 123456789}]
    status, data = create_attendees(sent={"attendees": attendee_no_name})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_invalid_name():
    invalid_name = [{"mispar_ishi": 1234567, "tehudat_zehut": 123456789, "full_name": "J0hn D0e!"}]
    status, data = create_attendees(sent={"attendees": invalid_name})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 1

def test_create_attendees_invalid_mispar_ishi():
    invalid_mispar_ishi = [{"mispar_ishi": 123, "tehudat_zehut": 123456789, "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 3

def test_create_attendees_invalid_tehudat_zehut():
    invalid_tehudat_zehut = [{"mispar_ishi": 1234567, "tehudat_zehut": 12345678, "full_name": "John Doe"}]
    status, data = create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert status == 400
    assert data["data"]["misssing_data"][0]["error"]["error_code"] == 4

def test_create_attendees_mixed_valid_and_invalid():
    global random_mispar_ishi, random_tehudat_zehut
    mixed_attendees = [
        {"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut, "full_name": "John Doe"},
        {"mispar_ishi": 123, "tehudat_zehut": 123456789, "full_name": "Invalid Mispar"}
    ]
    status, data = create_attendees(sent={"attendees": mixed_attendees})
    assert status == 201
    assert len(data["data"]["misssing_data"]) == 1
    assert len(data["data"]["successfull"]["mispar_ishi"]) == 1

def test_create_attendees_large_input():
    global random_mispar_ishi, random_tehudat_zehut
    large_input = [{"mispar_ishi": random_mispar_ishi + i, "tehudat_zehut": random_tehudat_zehut, "full_name": "John Doe"} for i in range(100)]
    status, data = create_attendees(sent={"attendees": large_input}, testing="Ok")
    assert status == 201
    assert len(data["data"]["successfull"]["mispar_ishi"]) == 100
