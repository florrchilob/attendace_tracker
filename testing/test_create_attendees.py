import string
import random
from testing import helper_tests

# Tests for the create_attendees function
def test_create_attendees_missing_attendees():
    response, error = helper_tests.create_attendees(sent={})
    assert response == 400 and error == 101

def test_create_attendees_empty_attendees():
    response, error = helper_tests.create_attendees(sent={"attendees": []})
    assert response == 400 and error == 101

def test_create_attendees_invalid_attendee():
    invalid_attendee = [{"mispar_ishi": 12345}]
    response, error = helper_tests.create_attendees(sent={"attendees": invalid_attendee})
    assert response == 400 and error == 4

def test_create_attendees_valid_attendee():
    valid_attendee = [{"mispar_ishi": 1234567, "tehudat_zehut": 123456789, "full_name": "John Doe"}]
    response, error = helper_tests.create_attendees(sent={"attendees": valid_attendee}, answer=1)
    assert response == 201 and error["error"] == 0

def test_create_attendees_duplicate_attendee():
    duplicate_attendee = [{"mispar_ishi": 1234567, "tehudat_zehut": 123456789, "full_name": "John Doe"}]
    helper_tests.create_attendees(sent={"attendees": duplicate_attendee})
    response, error = helper_tests.create_attendees(sent={"attendees": duplicate_attendee})
    assert response == 400 and error == 14

def test_create_attendees_missing_name():
    attendee_no_name = [{"mispar_ishi": 1234567, "tehudat_zehut": 123456789}]
    response, error = helper_tests.create_attendees(sent={"attendees": attendee_no_name})
    assert response == 400 and error == 4

def test_create_attendees_invalid_name():
    invalid_name = [{"mispar_ishi": 1234567, "tehudat_zehut": 123456789, "full_name": "J0hn D0e!"}]
    response, error = helper_tests.create_attendees(sent={"attendees": invalid_name})
    assert response == 400 and error == 1

def test_create_attendees_invalid_mispar_ishi():
    invalid_mispar_ishi = [{"mispar_ishi": 123, "tehudat_zehut": 123456789, "full_name": "John Doe"}]
    response, error = helper_tests.create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert response == 400 and error == 3

def test_create_attendees_invalid_tehudat_zehut():
    invalid_tehudat_zehut = [{"mispar_ishi": 1234567, "tehudat_zehut": 12345678, "full_name": "John Doe"}]
    response, error = helper_tests.create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert response == 400 and error == 4

def test_create_attendees_mixed_valid_and_invalid():
    mixed_attendees = [
        {"mispar_ishi": 1234567, "tehudat_zehut": 123456789, "full_name": "John Doe"},
        {"mispar_ishi": 123, "tehudat_zehut": 123456789, "full_name": "Invalid Mispar"}
    ]
    response, error, data = helper_tests.create_attendees(sent={"attendees": mixed_attendees}, answer=1)
    assert response == 201
    assert len(data["misssing_data"]) == 1
    assert len(data["successfull"]["mispar_ishi"]) == 1

def test_create_attendees_large_input():
    large_input = [{"mispar_ishi": 1234567 + i, "tehudat_zehut": 123456789, "full_name": "John Doe"} for i in range(1000)]
    response, error = helper_tests.create_attendees(sent={"attendees": large_input}, answer=1)
    assert response == 201 and error["error"] == 0
