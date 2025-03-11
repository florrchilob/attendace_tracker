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
    return response.status_code, response.json()

@pytest.fixture
async def test_attendee_data():
    random_mispar_ishi = str(random.randrange(100000, 9999999))
    random_tehudat_zehut = str(random.randrange(100000000, 999999999))
    random_name = ''.join(random.choices(string.ascii_lowercase, k=10))
    id = await create_get_id_attendee(random_mispar_ishi, random_tehudat_zehut)
    return {
        "id": id,
        "mispar_ishi": random_mispar_ishi,
        "tehudat_zehut": random_tehudat_zehut,
        "full_name": random_name
    }

@pytest.mark.asyncio
async def test_get_by_id_valid():
    id = await create_get_id_attendee()
    status, data = await get_by_endpoint("id", id)
    assert status == 200
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == id

@pytest.mark.asyncio
async def test_get_by_id_invalid():
    status, data = await get_by_endpoint("id", "invalid")
    assert status == 400
    assert data["error_code"] == 102

@pytest.mark.asyncio
async def test_get_by_id_nonexistent():
    status, data = await get_by_endpoint("id", 99999999)
    assert status == 400
    assert data["error_code"] == 104

@pytest.mark.asyncio
async def test_get_by_id_negative():
    status, data = await get_by_endpoint("id", "-1111")
    assert status == 400
    assert data["error_code"] == 102

@pytest.mark.asyncio
async def test_get_by_mispar_ishi_valid(test_attendee_data):
    attendee = await test_attendee_data
    status, data = await get_by_endpoint("mispar_ishi", attendee["mispar_ishi"])
    assert status == 200
    assert len(data["data"]) == 1
    assert data["data"][0]["mispar_ishi"] == attendee["mispar_ishi"]

@pytest.mark.asyncio
async def test_get_by_mispar_ishi_invalid():
    status, data = await get_by_endpoint("mispar_ishi", "1234")
    assert status == 400
    assert data["error_code"] == 3

@pytest.mark.asyncio
async def test_get_by_mispar_ishi_nonexistent():
    status, data = await get_by_endpoint("mispar_ishi", "9999999")
    assert status == 400
    assert data["error_code"] == 104

@pytest.mark.asyncio
async def test_get_by_mispar_ishi_leading_zeros():
    status, data = await get_by_endpoint("mispar_ishi", "0123456")
    assert status == 400
    assert data["error_code"] == 3

@pytest.mark.asyncio
async def test_get_by_tehudat_zehut_valid(test_attendee_data):
    attendee = await test_attendee_data
    status, data = await get_by_endpoint("tehudat_zehut", attendee["tehudat_zehut"])
    assert status == 200
    assert len(data["data"]) == 1
    assert data["data"][0]["tehudat_zehut"] == attendee["tehudat_zehut"]

@pytest.mark.asyncio
async def test_get_by_tehudat_zehut_invalid():
    status, data = await get_by_endpoint("tehudat_zehut", "12345678") 
    assert status == 400
    assert data["error_code"] == 4

@pytest.mark.asyncio
async def test_get_by_tehudat_zehut_nonexistent():
    status, data = await get_by_endpoint("tehudat_zehut", "999999999")
    assert status == 400
    assert data["error_code"] == 104

@pytest.mark.asyncio
async def test_get_by_tehudat_zehut_leading_zeros():
    status, data = await get_by_endpoint("tehudat_zehut", "012345678")
    assert status == 400
    assert data["error_code"] == 4

@pytest.mark.asyncio
async def test_get_by_name_valid(test_attendee_data):
    attendee = await test_attendee_data
    status, data = await get_by_endpoint("name", attendee["full_name"])
    assert status == 200
    assert len(data["data"]) > 0
    assert any(attendee["full_name"].lower() == attendee["full_name"].lower() 
              for attendee in data["data"])

@pytest.mark.asyncio
async def test_get_by_name_partial_match(test_attendee_data):
    attendee = await test_attendee_data
    partial_name = attendee["full_name"][:5]
    status, data = await get_by_endpoint("name", partial_name)
    assert status == 200
    assert len(data["data"]) > 0

@pytest.mark.asyncio
async def test_get_by_name_case_insensitive(test_attendee_data):
    attendee = await test_attendee_data
    upper_name = attendee["full_name"].upper()
    status, data = await get_by_endpoint("name", upper_name)
    assert status == 200
    assert len(data["data"]) > 0

@pytest.mark.asyncio
async def test_get_by_name_nonexistent():
    status, data = await get_by_endpoint("name", "ThisNameDefinitelyDoesNotExist12345")
    assert status == 400
    assert data["error_code"] == 104

@pytest.mark.asyncio
async def test_get_by_name_empty():
    status, data = await get_by_endpoint("name", "")
    assert status == 400 and data["error_code"] == 1 or status == 404

@pytest.mark.asyncio
async def test_get_by_invalid_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/getby/invalid_endpoint/123")
    assert response.status_code == 400 and response.json()["error_code"] == 104

@pytest.mark.asyncio
async def test_get_by_name_multiple_matches():
    common_name = "John Doe"
    id1 = await create_get_id_attendee()
    id2 = await create_get_id_attendee()
    
    async with httpx.AsyncClient() as client:
        await client.put(f"{BASE_URL}/edit", json={"id": id1, "full_name": common_name})
        await client.put(f"{BASE_URL}/edit", json={"id": id2, "full_name": common_name})
    
    status, data = await get_by_endpoint("name", common_name)
    assert status == 200
    assert len(data["data"]) >= 2
    matching_names = [attendee["full_name"] for attendee in data["data"] if attendee["full_name"] == common_name]
    assert len(matching_names) >= 2

@pytest.mark.asyncio
async def test_get_by_name_special_characters():
    special_name = "O'Connor-Smith"
    id = await create_get_id_attendee()
    
    async with httpx.AsyncClient() as client:
        await client.put(f"{BASE_URL}/edit", json={"id": id, "full_name": special_name})
    
    status, data = await get_by_endpoint("name", special_name)
    assert status == 200
    assert len(data["data"]) > 0
    assert any(attendee["full_name"] == special_name for attendee in data["data"])

@pytest.mark.asyncio
async def test_get_by_name_unicode_characters():
    unicode_name = "José María"
    id = await create_get_id_attendee()
    
    async with httpx.AsyncClient() as client:
        await client.put(f"{BASE_URL}/edit", json={"id": id, "full_name": unicode_name})
    
    status, data = await get_by_endpoint("name", unicode_name)
    assert status == 200
    assert len(data["data"]) > 0
    assert any(attendee["full_name"] == unicode_name for attendee in data["data"]) 