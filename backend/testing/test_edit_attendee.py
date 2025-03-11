import pytest
import requests
import random
import string
from testing.test_create_attendees import create_get_id_attendee
import asyncio
import httpx

# Add mock for testing database error

# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

# Helper function to send PUT requests for editing attendees
async def edit_attendees(sent=None):
    if sent is None:
        sent = {}
    async with httpx.AsyncClient() as client:
        response = await client.put(BASE_URL + "/edit", json=sent)
    return {"status": response.status_code, "data": response.json()}

@pytest.fixture
def random_data_edit():
    random_id = random.randint(1, 1000)
    random_mispar_ishi = str(random.randrange(100000, 9999999))
    random_tehudat_zehut = str(random.randrange(100000000, 999999999))
    return {
        "random_id": random_id, 
        "random_mispar_ishi": random_mispar_ishi, 
        "random_tehudat_zehut":random_tehudat_zehut
    }

# Test cases
@pytest.mark.asyncio
async def test_edit_attendees_missing_id():
    response = await edit_attendees(sent={"full_name": "Updated Name"})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 102

@pytest.mark.asyncio
async def test_edit_attendees_no_fields_to_update():
    response = await edit_attendees(sent={"id": 1})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 101

@pytest.mark.asyncio
async def test_edit_attendees_invalid_id():
    response = await edit_attendees(sent={"id": "invalid", "full_name": "Updated Name"})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 102

@pytest.mark.asyncio
async def test_edit_attendees_valid_id_update_name():
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(sent={"id": id_to_edit, "full_name": "Updated Name"})
    assert response["status"] == 200

@pytest.mark.asyncio
async def test_edit_attendees_invalid_mispar_ishi(random_data_edit):
    random_data = random_data_edit
    response = await edit_attendees(sent={"id": random_data["random_id"], "mispar_ishi": "123"})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 3

@pytest.mark.asyncio
async def test_edit_attendees_invalid_tehudat_zehut(random_data_edit):
    random_data = random_data_edit
    response = await edit_attendees(sent={"id": random_data["random_id"], "tehudat_zehut": "12345"})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 4

@pytest.mark.asyncio
async def test_edit_attendees_valid_id_update_multiple_fields(random_data_edit):
    id_to_edit = await create_get_id_attendee()
    random_data = random_data_edit
    response = await edit_attendees(
        sent={
            "id": id_to_edit,
            "mispar_ishi": random_data["random_mispar_ishi"],
            "tehudat_zehut": random_data["random_tehudat_zehut"],
            "full_name": "Updated Name",
            "arrived": True,
        }
    )
    assert response["status"] == 200

@pytest.mark.asyncio
async def test_edit_attendees_missing_field_validation_error(random_data_edit):
    random_data= random_data_edit
    response = await edit_attendees(
        sent={
            "id": random_data["random_id"],
            "mispar_ishi": "",
        }
    )
    assert response["status"] == 400
    assert response["data"]["error_code"] == 3

@pytest.mark.asyncio
async def test_edit_attendees_invalid_arrived():
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(sent={"id": id_to_edit, "arrived": "yes"})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 101  # Error por tipo de dato inválido

@pytest.mark.asyncio
async def test_edit_attendees_valid_arrived_true():
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(sent={"id": id_to_edit, "arrived": True})
    assert response["status"] == 200

@pytest.mark.asyncio
async def test_edit_attendees_valid_arrived_false():
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(sent={"id": id_to_edit, "arrived": False})
    assert response["status"] == 200

    response = requests.get(f"{BASE_URL}/getby/id/{id_to_edit}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data[0]["arrived"] == False


@pytest.mark.asyncio
async def test_edit_attendees_invalid_date_format():
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(sent={"id": id_to_edit, "date_arrived": "2023-13-32"})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 5

@pytest.mark.asyncio
async def test_edit_attendees_invalid_date_type():
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(sent={"id": id_to_edit, "date_arrived": 123456789})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 5

@pytest.mark.asyncio
async def test_edit_attendees_null_date():
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(sent={"id": id_to_edit, "date_arrived": None})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 5

@pytest.mark.asyncio
async def test_edit_attendees_valid_date():
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(sent={"id": id_to_edit, "date_arrived": "2023-12-15 10:00:00"})
    assert response["status"] == 200
    response = requests.get(f"{BASE_URL}/getby/id/{id_to_edit}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data[0]["arrived"] == True and data[0]["date_arrived"] == "2023-12-15T10:00:00"

@pytest.mark.asyncio
async def test_edit_attendees_update_all_fields_double_mispar_ishi(random_data_edit):
    random_data = random_data_edit
    await create_get_id_attendee(mispar_ishi_sent=random_data["random_mispar_ishi"])
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(
        sent={
            "id": id_to_edit,
            "mispar_ishi": random_data["random_mispar_ishi"],
            "tehudat_zehut": random_data["random_tehudat_zehut"],
            "full_name": "Updated Name",
            "arrived": True,
            "date_arrived": "2023-12-15 10:00:00",
        }
    )
    assert response["status"] == 400
    assert response["data"]["error_code"] == 3

@pytest.mark.asyncio
async def test_edit_attendees_update_all_fields_double_tehudat_zehut(random_data_edit):
    random_data = random_data_edit
    await create_get_id_attendee(tehudat_zehut=random_data["random_tehudat_zehut"])
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(
        sent={
            "id": id_to_edit,
            "mispar_ishi": random_data["random_mispar_ishi"],
            "tehudat_zehut": random_data["random_tehudat_zehut"],
            "full_name": "Updated Name",
            "arrived": True,
            "date_arrived": "2023-12-15 10:00:00",
        }
    )
    assert response["status"] == 400
    assert response["data"]["error_code"] == 4

@pytest.mark.asyncio
async def test_edit_attendees_update_all_fields(random_data_edit):
    random_data = random_data_edit
    id_to_edit = await create_get_id_attendee()
    response= await edit_attendees(
        sent={
            "id": id_to_edit,
            "mispar_ishi": random_data["random_mispar_ishi"],
            "tehudat_zehut": random_data["random_tehudat_zehut"],
            "full_name": "Updated Name",
            "arrived": True,
            "date_arrived": "2023-12-15 10:00:00",
        }
    )
    assert response["status"] == 200

    
    response = requests.get(f"{BASE_URL}/getby/id/{id_to_edit}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data[0]["arrived"] == True and data[0]["date_arrived"] == "2023-12-15T10:00:00"

@pytest.mark.asyncio
async def test_edit_attendees_invalid_combined_fields():
    id_to_edit = await create_get_id_attendee()
    response = await edit_attendees(
        sent={
            "id": id_to_edit,
            "mispar_ishi": "123",
            "tehudat_zehut": "12345678",
            "full_name": "J0hn D0e!",
            "arrived": "yes",
            "date_arrived": "2023-13-32",  
        }
    )
    assert response["status"] == 400
    assert response["data"]["error_code"] == 3

@pytest.mark.asyncio
async def test_edit_attendees_database_not_found():
    response = await edit_attendees(sent={"id": 999999, "full_name": "Name Not Found"})
    assert response["status"] == 400
    assert response["data"]["error_code"] == 101

