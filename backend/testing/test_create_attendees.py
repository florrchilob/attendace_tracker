import pytest
import requests
import random
import string
import httpx
import asyncio

# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

# Add mock for testing database error
@pytest.mark.asyncio
async def create_get_id_attendee(mispar_ishi_sent = None, tehudat_zehut = None, full_name_sent = None):
    # Make random attendee
    if mispar_ishi_sent == None:
        random_mispar_ishi = str(random.randrange(100000, 9999999))
    else:
        random_mispar_ishi = mispar_ishi_sent
    if tehudat_zehut == None:
        random_tehudat_zehut = str(random.randrange(100000000, 999999999))
    else:
        random_tehudat_zehut = tehudat_zehut
    if full_name_sent == None:
        random_name = ""
        for i in range(random.randrange(99)):
            random_name = random_name + random.choice(string.ascii_lowercase)
        random_name = random_name + " "
        for i in range(random.randrange(99)):
            random_name = random_name + random.choice(string.ascii_lowercase)
    else:
        random_name = full_name_sent
    valid_attendee = {"attendees":[{"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut, "full_name": random_name, "arrived": False}]}
    # Create attendee
    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL + "/create", json=valid_attendee)
    status = response.status_code
    data = response.json()
    assert status == 201
    assert len(data["data"]["successfull"]["mispar_ishi"]) == 1
    # Get id attendee
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL + "/getby/mispar_ishi/" + random_mispar_ishi)    
    assert response.status_code == 200
    data = response.json()["data"]
    id_to_edit = None
    for attendee in data:
        if attendee["full_name"].lower() == random_name:
            id_to_edit = attendee["id"]
            break
    assert id_to_edit is not None
    return id_to_edit

# Helper function to send POST requests
@pytest.mark.asyncio
async def create_attendees(sent=None, testing=None):
    if sent is None:
        sent = {}
    payload = {"attendees": sent.get("attendees", [])}
    if testing:
        payload["testing"] = testing
    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL + "/create", json=payload)
    data = response.json()
    if "data" in data:
        return {
            "status": response.status_code, 
            "data": data["data"]
        }
    else:
        return {
            "status": response.status_code, 
            "data": data
        }

@pytest.fixture
def random_data_create():
    random_mispar_ishi = str(random.randrange(100000, 9999999))
    random_tehudat_zehut = str(random.randrange(100000000, 999999999))
    return random_mispar_ishi, random_tehudat_zehut

# Test cases
@pytest.mark.asyncio
async def test_create_attendees_missing_attendees():
    response = await create_attendees(sent={})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 101

@pytest.mark.asyncio
async def test_create_attendees_empty_attendees():
    response = await create_attendees(sent={"attendees": []})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 101

@pytest.mark.asyncio
async def test_create_attendees_invalid_attendee():
    invalid_attendee = [{"mispar_ishi": "12345", "full_name": "AAA"}]
    response = await create_attendees(sent={"attendees": invalid_attendee})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 3


@pytest.mark.asyncio
async def test_create_attendees_duplicate_attendee():
    duplicate_attendee = [{"mispar_ishi": "1234567", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    await create_attendees(sent={"attendees": duplicate_attendee})
    response = await create_attendees(sent={"attendees": duplicate_attendee})
    assert response["status"] == 400
    assert len(response["data"]["already_database"]["mispar_ishi"]) == 1

@pytest.mark.asyncio
async def test_create_attendees_missing_name():
    attendee_no_name = [{"mispar_ishi": "1234567", "tehudat_zehut": "123456789"}]
    response = await create_attendees(sent={"attendees": attendee_no_name})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 1


@pytest.mark.asyncio
async def test_create_attendees_invalid_mispar_ishi():
    invalid_mispar_ishi = [{"mispar_ishi": "123", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 3

@pytest.mark.asyncio
async def test_create_attendees_invalid_tehudat_zehut():
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "12345678", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 4

@pytest.mark.asyncio
async def test_create_attendees_mixed_valid_and_invalid(random_data_create):
    random_mispar_ishi, random_tehudat_zehut = random_data_create
    mixed_attendees = [
        {"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut, "full_name": "John Doe"},
        {"mispar_ishi": "123", "tehudat_zehut": "123456789", "full_name": "Invalid Mispar"}
    ]
    response = await create_attendees(sent={"attendees": mixed_attendees})
    assert response["status"] == 201
    assert len(response["data"]["missing_data"]) == 1
    assert len(response["data"]["successfull"]["mispar_ishi"]) == 1

@pytest.mark.asyncio
async def test_create_attendees_invalid_mispar_ishi_leading_zeros(random_data_create):
    random_mispar_ishi, random_tehudat_zehut = random_data_create
    invalid_mispar_ishi = [{"mispar_ishi": "00123", "tehudat_zehut": random_tehudat_zehut, "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 3

@pytest.mark.asyncio
async def test_create_attendees_invalid_tehudat_zehut_leading_zeros():
    # tehudat_zehut is passed as a string to preserve the leading zeros
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "001234567", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_tehudat_zehut, "testing":"zeros"})
    assert response["status"] == 201
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 4

@pytest.mark.asyncio
async def test_create_attendees_invalid_mispar_ishi_too_few_digits():
    invalid_mispar_ishi = [{"mispar_ishi": "123", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 3

@pytest.mark.asyncio
async def test_create_attendees_invalid_tehudat_zehut_too_few_digits():
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "12345678", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 4

@pytest.mark.asyncio
async def test_create_attendees_invalid_tehudat_zehut_too_many_digits():
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "123456789012", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 4

@pytest.mark.asyncio
async def test_create_attendees_invalid_mispar_ishi_leading_zeros():
    # mispar_ishi is passed as a string to preserve the leading zeros
    invalid_mispar_ishi = [{"mispar_ishi": "00123", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 3

@pytest.mark.asyncio
async def test_create_attendees_invalid_tehudat_zehut_leading_zeros():
    # tehudat_zehut is passed as a string to preserve the leading zeros
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "00123456789", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 4

@pytest.mark.asyncio
async def test_create_attendees_invalid_mispar_ishi_too_few_digits():
    # mispar_ishi has too few digits (3 digits)
    invalid_mispar_ishi = [{"mispar_ishi": "123", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 3

@pytest.mark.asyncio
async def test_create_attendees_invalid_tehudat_zehut_too_few_digits():
    # tehudat_zehut has too few digits (8 digits)
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "12345678", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 4

@pytest.mark.asyncio
async def test_create_attendees_invalid_tehudat_zehut_too_many_digits():
    # tehudat_zehut has too many digits (12 digits)
    invalid_tehudat_zehut = [{"mispar_ishi": "1234567", "tehudat_zehut": "123456789012", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_tehudat_zehut})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 4

@pytest.mark.asyncio
async def test_create_attendees_invalid_mispar_ishi_invalid_characters():
    # mispar_ishi has invalid characters (alphabetical)
    invalid_mispar_ishi = [{"mispar_ishi": "ABC123456", "tehudat_zehut": "123456789", "full_name": "John Doe"}]
    response = await create_attendees(sent={"attendees": invalid_mispar_ishi})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 3

@pytest.mark.asyncio
async def test_create_attendees_invalid_date_format(random_data_create):
    mispar_ishi, tehudat_zehut = random_data_create
    invalid_date_attendee = [{"mispar_ishi": mispar_ishi, "tehudat_zehut": tehudat_zehut, "full_name": "John Doe", "date_arrived": "2023-13-32"}]
    response = await create_attendees(sent={"attendees": invalid_date_attendee})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 5

@pytest.mark.asyncio
async def test_create_attendees_invalid_date_type(random_data_create):
    mispar_ishi, tehudat_zehut = random_data_create
    invalid_date_type = [{"mispar_ishi": mispar_ishi, "tehudat_zehut": tehudat_zehut, "full_name": "John Doe", "date_arrived": 123456789}]
    response = await create_attendees(sent={"attendees": invalid_date_type})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 5

@pytest.mark.asyncio
async def test_create_attendees_null_date(random_data_create):
    mispar_ishi, tehudat_zehut = random_data_create
    null_date = [{"mispar_ishi": mispar_ishi, "tehudat_zehut": tehudat_zehut, "full_name": "John Doe", "date_arrived": None}]
    response = await create_attendees(sent={"attendees": null_date})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 5

@pytest.mark.asyncio
async def test_create_attendees_valid_date(random_data_create):
    mispar_ishi, tehudat_zehut = random_data_create
    valid_date = [{"mispar_ishi": mispar_ishi, "tehudat_zehut": tehudat_zehut, "full_name": "John Doe", "date_arrived": "2023-12-15 10:00:00"}]
    response = await create_attendees(sent={"attendees": valid_date})
    assert response["status"] == 201
    assert len(response["data"]["successfull"]["mispar_ishi"]) == 1

@pytest.mark.asyncio
async def test_create_attendees_arrived_as_true(random_data_create):
    mispar_ishi, tehudat_zehut = random_data_create
    arrived_true = [{"mispar_ishi": mispar_ishi, "tehudat_zehut": tehudat_zehut, "full_name": "John Doe", "arrived": True}]
    response = await create_attendees(sent={"attendees": arrived_true})
    assert response["status"] == 201
    assert len(response["data"]["successfull"]["mispar_ishi"]) == 1

@pytest.mark.asyncio
async def test_create_attendees_arrived_as_false(random_data_create):
    mispar_ishi, tehudat_zehut = random_data_create
    arrived_false = [{"mispar_ishi": mispar_ishi, "tehudat_zehut": tehudat_zehut, "full_name": "John Doe", "arrived": False}]
    response = await create_attendees(sent={"attendees": arrived_false})
    assert response["status"] == 201
    assert len(response["data"]["successfull"]["mispar_ishi"]) == 1

@pytest.mark.asyncio
async def test_create_attendees_invalid_arrived(random_data_create):
    mispar_ishi, tehudat_zehut = random_data_create
    invalid_arrived = [{"mispar_ishi": mispar_ishi, "tehudat_zehut": tehudat_zehut, "full_name": "John Doe", "arrived": "yes"}]
    response = await create_attendees(sent={"attendees": invalid_arrived})
    assert response["status"] == 400
    assert response["data"]["missing_data"][0]["error"]["error_code"] == 101  # Valor inválido

@pytest.mark.asyncio
async def test_create_attendees_valid_attendee(random_data_create):
    random_mispar_ishi, random_tehudat_zehut = random_data_create
    valid_attendee = [{"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut, "full_name": "John Doe", "arrived": True, "date_arrived": "2023-12-15 10:00:00"}]
    response = await create_attendees(sent={"attendees": valid_attendee})
    assert response["status"] == 201
    assert len(response["data"]["successfull"]["mispar_ishi"]) == 1

@pytest.mark.asyncio
async def test_create_attendees_invalid_combined_fields():
    invalid_combined = [{
        "mispar_ishi": "123",  
        "tehudat_zehut": "123456789",  
        "full_name": "J0hn D0e!",  
        "arrived": "yes",  
        "date_arrived": "2023-13-32" 
    }]
    response = await create_attendees(sent={"attendees": invalid_combined})
    assert response["status"] == 400
    assert len(response["data"]["missing_data"]) == 1
    errors = response["data"]["missing_data"][0]["error"]
    assert errors["error_code"] == 3
