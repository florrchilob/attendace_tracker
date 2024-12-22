import pytest
from fastapi.testclient import TestClient
import app

client = TestClient(app)

@pytest.fixture
def call_create_attendees_endpoint():
    """
    Fixture to call the create attendees endpoint with a payload.
    This avoids repeating the same code to call the endpoint.
    """
    def _call_endpoint(payload):
        response = client.post("/attendees/create", json=payload)
        return response
    return _call_endpoint

def test_create_attendees_missing_attendees_key(call_create_attendees_endpoint):
    # Test case where the 'attendees' key is missing from the payload.
    response = call_create_attendees_endpoint({})
    assert response.status_code == 400
    assert response.json() == {"status": "BAD_REQUEST", "error_code": 101, "message": "No valid"}

def test_create_attendees_attendees_not_a_list(call_create_attendees_endpoint):
    # Test case where 'attendees' value is not a list.
    response = call_create_attendees_endpoint({"attendees": "not a list"})
    assert response.status_code == 400
    assert response.json() == {"status": "BAD_REQUEST", "error_code": 101, "message": "No valid"}

def test_create_attendees_empty_attendees_list(call_create_attendees_endpoint):
    # Test case where 'attendees' list is empty.
    response = call_create_attendees_endpoint({"attendees": []})
    assert response.status_code == 400
    assert response.json() == {"status": "BAD_REQUEST", "error_code": 101, "message": "No valid"}

def test_create_attendees_missing_mispar_ishi_and_tehudat_zehut(call_create_attendees_endpoint):
    # Test case where 'mispar_ishi' and 'tehudat_zehut' are missing in an attendee.
    payload = {"attendees": [{"full_name": "Test Attendee"}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
        "status": "BAD_REQUEST",
        "error_code": 101,
        "message": "No valid",
        "data": {
            "misssing_data": [{"attendee": {"full_name": "Test Attendee"}, "error": {"status_code": 400}}],
            "already_database": {"mispar_ishi": [], "tehudat_zehut": []},
            "successfull": {"mispar_ishi": [], "tehudat_zehut": []},
        },
    }


def test_create_attendees_missing_full_name(call_create_attendees_endpoint):
    # Test case where 'full_name' is missing in an attendee.
    payload = {"attendees": [{"mispar_ishi": 1234567}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
        "status": "BAD_REQUEST",
        "error_code": 101,
        "message": "No valid",
        "data": {
            "misssing_data": [{"attendee": {"mispar_ishi": 1234567}, "error": {"status_code": 400}}],
            "already_database": {"mispar_ishi": [], "tehudat_zehut": []},
            "successfull": {"mispar_ishi": [], "tehudat_zehut": []},
        },
    }

def test_create_attendees_invalid_name(call_create_attendees_endpoint):
    # Test case with an invalid 'name' format.
    payload = {"attendees": [{"mispar_ishi": 1234567, "name": 1234, "tehudat_zehut": 123456789}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
        "status": "BAD_REQUEST",
        "error_code": 101,
        "message": "No valid",
        "data": {
             "misssing_data": [{"mispar_ishi": 1234567, "name": 1234, "tehudat_zehut": 123456789}],
             "already_database": {"mispar_ishi": [], "tehudat_zehut": []},
             "successfull": {"mispar_ishi": [], "tehudat_zehut": []}
        }
    }

def test_create_attendees_invalid_mispar_ishi_wrong_type(call_create_attendees_endpoint):
    # Test case with an invalid 'mispar_ishi' format (wrong type).
    payload = {"attendees": [{"mispar_ishi": "abc", "name": "John Doe", "tehudat_zehut": 123456789}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
        "status": "BAD_REQUEST",
        "error_code": 101,
        "message": "No valid",
        "data": {
            "misssing_data": [{"mispar_ishi": "abc", "name": "John Doe", "tehudat_zehut": 123456789}],
            "already_database": {"mispar_ishi": [], "tehudat_zehut": []},
            "successfull": {"mispar_ishi": [], "tehudat_zehut": []},
        }
    }
def test_create_attendees_invalid_mispar_ishi_short(call_create_attendees_endpoint):
    # Test case with an invalid 'mispar_ishi' (short).
    payload = {"attendees": [{"mispar_ishi": 1234, "name": "John Doe", "tehudat_zehut": 123456789}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
        "status": "BAD_REQUEST",
        "error_code": 101,
        "message": "No valid",
        "data": {
            "misssing_data": [{"mispar_ishi": 1234, "name": "John Doe", "tehudat_zehut": 123456789}],
            "already_database": {"mispar_ishi": [], "tehudat_zehut": []},
            "successfull": {"mispar_ishi": [], "tehudat_zehut": []}
        }
    }

def test_create_attendees_invalid_mispar_ishi_long(call_create_attendees_endpoint):
    # Test case with an invalid 'mispar_ishi' (long).
    payload = {"attendees": [{"mispar_ishi": 12345678, "name": "John Doe", "tehudat_zehut": 123456789}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
        "status": "BAD_REQUEST",
        "error_code": 101,
        "message": "No valid",
        "data": {
            "misssing_data": [{"mispar_ishi": 12345678, "name": "John Doe", "tehudat_zehut": 123456789}],
            "already_database": {"mispar_ishi": [], "tehudat_zehut": []},
            "successfull": {"mispar_ishi": [], "tehudat_zehut": []}
        }
    }

def test_create_attendees_invalid_tehudat_zehut_wrong_type(call_create_attendees_endpoint):
    # Test case with an invalid 'tehudat_zehut' format (wrong type).
    payload = {"attendees": [{"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": "abc"}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
        "status": "BAD_REQUEST",
        "error_code": 101,
        "message": "No valid",
         "data": {
            "misssing_data": [{"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": "abc"}],
            "already_database": {"mispar_ishi": [], "tehudat_zehut": []},
            "successfull": {"mispar_ishi": [], "tehudat_zehut": []}
        }
    }

def test_create_attendees_invalid_tehudat_zehut_short(call_create_attendees_endpoint):
    # Test case with an invalid 'tehudat_zehut' (short).
    payload = {"attendees": [{"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": 12345678}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
            "status": "BAD_REQUEST",
            "error_code": 101,
            "message": "No valid",
             "data": {
                 "misssing_data": [{"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": 12345678}],
                 "already_database": {"mispar_ishi": [], "tehudat_zehut": []},
                "successfull": {"mispar_ishi": [], "tehudat_zehut": []},
            },
        }

def test_create_attendees_invalid_tehudat_zehut_long(call_create_attendees_endpoint):
    # Test case with an invalid 'tehudat_zehut' (long).
    payload = {"attendees": [{"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": 1234567890}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
            "status": "BAD_REQUEST",
            "error_code": 101,
            "message": "No valid",
             "data": {
                "misssing_data": [{"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": 1234567890}],
                 "already_database": {"mispar_ishi": [], "tehudat_zehut": []},
                "successfull": {"mispar_ishi": [], "tehudat_zehut": []}
            },
        }

def test_create_attendees_already_in_database_mispar_ishi(call_create_attendees_endpoint,):
    # Test case where an attendee with the same 'mispar_ishi' already exists in the database.
    # Assuming you have a way to add an attendee directly to the DB to cause this conflict
    payload = {"attendees": [{"mispar_ishi": 1111111, "name": "John Doe", "tehudat_zehut": 987654321}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
            "status": "BAD_REQUEST",
            "error_code": 101,
            "message": "No valid",
            "data": {
            "misssing_data": [],
            "already_database": {
                "mispar_ishi": [1111111],
                "tehudat_zehut": [],
            },
            "successfull": {
                "mispar_ishi": [],
                "tehudat_zehut": [],
            },
        }
    }


def test_create_attendees_already_in_database_tehudat_zehut(call_create_attendees_endpoint):
    # Test case where an attendee with the same 'tehudat_zehut' already exists in the database.
    # Assuming you have a way to add an attendee directly to the DB to cause this conflict
    payload = {"attendees": [{"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": 111111111}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
            "status": "BAD_REQUEST",
            "error_code": 101,
            "message": "No valid",
            "data": {
            "misssing_data": [],
            "already_database": {
                "mispar_ishi": [],
                "tehudat_zehut": [111111111],
            },
            "successfull": {
                "mispar_ishi": [],
                "tehudat_zehut": [],
            },
        },
    }


def test_create_attendees_ok_with_mispar_ishi(call_create_attendees_endpoint):
    # Test case for creating a valid attendee with 'mispar_ishi'.
    payload = {"attendees": [{"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": 123456789}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 201
    assert response.json() == {
        "status": "CREATED",
        "data": {
            "misssing_data": [],
            "already_database": {
                "mispar_ishi": [],
                "tehudat_zehut": [],
            },
            "successfull": {
                "mispar_ishi": [1234567],
                "tehudat_zehut": [],
            },
        },
    }

def test_create_attendees_ok_with_tehudat_zehut(call_create_attendees_endpoint):
    # Test case for creating a valid attendee with 'tehudat_zehut'.
    payload = {"attendees": [{"name": "Jane Doe", "tehudat_zehut": 987654321}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 201
    assert response.json() == {
        "status": "CREATED",
        "data": {
            "misssing_data": [],
            "already_database": {
                "mispar_ishi": [],
                "tehudat_zehut": [],
            },
            "successfull": {
                "mispar_ishi": [],
                "tehudat_zehut": [987654321],
            },
        },
    }

def test_create_attendees_ok_multiple_attendees(call_create_attendees_endpoint):
    # Test case for creating multiple valid attendees.
    payload = {
        "attendees": [
            {"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": 123456789},
            {"name": "Jane Smith", "tehudat_zehut": 987654321},
        ]
    }
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 201
    assert response.json() == {
        "status": "CREATED",
        "data": {
            "misssing_data": [],
            "already_database": {
                "mispar_ishi": [],
                "tehudat_zehut": [],
            },
             "successfull": {
                "mispar_ishi": [1234567],
                "tehudat_zehut": [987654321],
            },
        },
    }

def test_create_attendees_mix_valid_and_invalid(call_create_attendees_endpoint):
    # Test case for a mix of valid and invalid attendees.
    payload = {
        "attendees": [
            {"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": 123456789},  # Valid
            {"name": "Jane Smith"},                                           # Missing 'mispar_ishi' and 'tehudat_zehut'
            {"mispar_ishi": "abc", "name": "Invalid Name"},                             # Invalid 'mispar_ishi'
        ]
    }
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 400
    assert response.json() == {
            "status": "BAD_REQUEST",
            "error_code": 101,
            "message": "No valid",
            "data": {
            "misssing_data": [
                {
                    "attendee": {"name": "Jane Smith"},
                     "error": {"status_code": 400}
                },
                {"mispar_ishi": "abc", "name": "Invalid Name"}],
            "already_database": {
                "mispar_ishi": [],
                "tehudat_zehut": []
            },
            "successfull": {
                "mispar_ishi": [1234567],
                "tehudat_zehut": []
            },
        },
    }

def test_create_attendees_with_testing_true(call_create_attendees_endpoint):
    # Test case where 'testing' is True.
    payload = {"attendees": [{"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": 123456789}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 201
    assert response.json() == {
        "status": "CREATED",
        "data": {
            "misssing_data": [],
            "already_database": {
                "mispar_ishi": [],
                "tehudat_zehut": [],
            },
            "successfull": {
                "mispar_ishi": [1234567],
                "tehudat_zehut": [],
            },
        },
    }


def test_create_attendees_with_testing_false(call_create_attendees_endpoint):
    # Test case where 'testing' is False.
    payload = {"attendees": [{"mispar_ishi": 1234567, "name": "John Doe", "tehudat_zehut": 123456789}]}
    response = call_create_attendees_endpoint(payload)
    assert response.status_code == 201
    assert response.json() == {
        "status": "CREATED",
        "data": {
            "misssing_data": [],
            "already_database": {
                "mispar_ishi": [],
                "tehudat_zehut": [],
            },
            "successfull": {
                "mispar_ishi": [1234567],
                "tehudat_zehut": [],
            },
        },
    }