import pytest
import random
import string
from testing.test_create_attendees import create_get_id_attendee
import asyncio
import httpx


# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

async def get_by_endpoint(endpoint: str, value):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/getby/{endpoint}/{value}")
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
def test_attendee_data():
    random_mispar_ishi = str(random.randrange(100000, 9999999))
    random_tehudat_zehut = str(random.randrange(100000000, 999999999))
    random_name = ''.join(random.choices(string.ascii_lowercase, k=10))
    return {
        "mispar_ishi": random_mispar_ishi,
        "tehudat_zehut": random_tehudat_zehut,
        "full_name": random_name
    }

@pytest.mark.asyncio
async def test_get_by_id_valid():
    id = await create_get_id_attendee()
    response = await get_by_endpoint("id", id)
    assert response["status"] == 200
    assert len(response["data"]) == 1
    assert response["data"][0]["id"] == id

@pytest.mark.asyncio
async def test_get_by_id_invalid():
    response = await get_by_endpoint("id", "invalid")
    assert response["status"] == 400
    assert response["data"]["error_code"] == 102

@pytest.mark.asyncio
async def test_get_by_id_nonexistent():
    response = await get_by_endpoint("id", 99999999)
    assert response["status"] == 400
    assert response["data"]["error_code"] == 104

@pytest.mark.asyncio
async def test_get_by_id_negative():
    response = await get_by_endpoint("id", "-1111")
    assert response["status"] == 400
    assert response["data"]["error_code"] == 102

@pytest.mark.asyncio
async def test_get_by_mispar_ishi_valid(test_attendee_data):
    attendee = test_attendee_data
    await create_get_id_attendee(mispar_ishi_sent=attendee["mispar_ishi"])
    response = await get_by_endpoint("mispar_ishi", attendee["mispar_ishi"])
    assert response["status"] == 200
    assert len(response["data"]) == 1
    assert response["data"][0]["mispar_ishi"] == attendee["mispar_ishi"]

@pytest.mark.asyncio
async def test_get_by_mispar_ishi_invalid():
    response = await get_by_endpoint("mispar_ishi", "123")
    assert response["status"] == 400
    assert response["data"]["error_code"] == 6

@pytest.mark.asyncio
async def test_get_by_mispar_ishi_nonexistent():
    response = await get_by_endpoint("mispar_ishi", "9999999")
    assert response["status"] == 400
    assert response["data"]["error_code"] == 104

@pytest.mark.asyncio
async def test_get_by_mispar_ishi_leading_zeros():
    response = await get_by_endpoint("mispar_ishi", "0123456")
    assert response["status"] == 400
    assert response["data"]["error_code"] == 3

@pytest.mark.asyncio
async def test_get_by_tehudat_zehut_valid(test_attendee_data):
    attendee = test_attendee_data
    await create_get_id_attendee(tehudat_zehut=attendee["tehudat_zehut"])
    response = await get_by_endpoint("tehudat_zehut", attendee["tehudat_zehut"])
    assert response["status"] == 200
    assert len(response["data"]) == 1
    assert response["data"][0]["tehudat_zehut"] == attendee["tehudat_zehut"]

@pytest.mark.asyncio
async def test_get_by_tehudat_zehut_invalid():
    response = await get_by_endpoint("tehudat_zehut", "999999999999999") 
    assert response["status"] == 400
    assert response["data"]["error_code"] == 4

@pytest.mark.asyncio
async def test_get_by_tehudat_zehut_nonexistent():
    response = await get_by_endpoint("tehudat_zehut", "1256")
    assert response["status"] == 400
    assert response["data"]["error_code"] == 104


@pytest.mark.asyncio
async def test_get_by_name_valid(test_attendee_data):
    attendee = test_attendee_data
    await create_get_id_attendee(full_name_sent=attendee["full_name"])
    response = await get_by_endpoint("name", attendee["full_name"])
    assert response["status"] == 200
    assert len(response["data"]) > 0
    assert any(attendee["full_name"].lower() == attendee["full_name"].lower() 
              for attendee in response["data"])

@pytest.mark.asyncio
async def test_get_by_name_partial_match(test_attendee_data):
    attendee = test_attendee_data
    id = await create_get_id_attendee(full_name_sent=attendee["full_name"])
    partial_name = attendee["full_name"][:5]
    response = await get_by_endpoint("name", partial_name)
    assert response["status"] == 200
    assert len(response["data"]) > 0

@pytest.mark.asyncio
async def test_get_by_name_case_insensitive(test_attendee_data):
    attendee = test_attendee_data
    id = await create_get_id_attendee(full_name_sent=attendee["full_name"])
    upper_name = attendee["full_name"].upper()
    response = await get_by_endpoint("name", upper_name)
    assert response["status"] == 200
    assert len(response["data"]) > 0

@pytest.mark.asyncio
async def test_get_by_name_nonexistent():
    response = await get_by_endpoint("name", "ThisNameDefinitelyDoesNotExist12345")
    assert response["status"] == 400
    assert response["data"]["error_code"] == 104

@pytest.mark.asyncio
async def test_get_by_name_empty():
    response = await get_by_endpoint("name", "")
    assert response["status"] == 400 and response["data"]["error_code"] == 1 or response["status"] == 404

@pytest.mark.asyncio
async def test_get_by_invalid_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/getby/invalid_endpoint/123")
    assert response.status_code == 400 and response.json()["error_code"] == 6

@pytest.mark.asyncio
async def test_get_by_name_multiple_matches():
    common_name = "John Doe"
    id1 = await create_get_id_attendee()
    id2 = await create_get_id_attendee()
    
    async with httpx.AsyncClient() as client:
        await client.put(f"{BASE_URL}/edit", json={"id": id1, "full_name": common_name})
        await client.put(f"{BASE_URL}/edit", json={"id": id2, "full_name": common_name})
    
    response = await get_by_endpoint("name", common_name)
    assert response["status"] == 200
    assert len(response["data"]) >= 2
    matching_names = [attendee["full_name"] for attendee in response["data"] if attendee["full_name"] == common_name]
    assert len(matching_names) >= 2

@pytest.mark.asyncio
async def test_get_by_name_special_characters():
    special_name = "O'Connor-Smith"
    id = await create_get_id_attendee()
    
    async with httpx.AsyncClient() as client:
        await client.put(f"{BASE_URL}/edit", json={"id": id, "full_name": special_name})
    
    response = await get_by_endpoint("name", special_name)
    assert response["status"] == 200
    assert len(response["data"]) > 0
    assert any(attendee["full_name"] == special_name for attendee in response["data"])

@pytest.mark.asyncio
async def test_get_by_name_unicode_characters():
    unicode_name = "José María"
    id = await create_get_id_attendee()
    
    async with httpx.AsyncClient() as client:
        await client.put(f"{BASE_URL}/edit", json={"id": id, "full_name": unicode_name})
    
    response = await get_by_endpoint("name", unicode_name)
    assert response["status"] == 200
    assert len(response["data"]) > 0
    assert any(attendee["full_name"] == unicode_name for attendee in response["data"]) 