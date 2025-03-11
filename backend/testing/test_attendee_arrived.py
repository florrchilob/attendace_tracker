import pytest
import requests
from testing.test_create_attendees import create_get_id_attendee
import random
import asyncio
import httpx

# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

# Add mock for testing database error

# Helper function to send PUT requests
async def attendee_arrived(sent=None, testing=None):
    if sent is None:
        sent = {}
    payload = sent
    if testing:
        payload["testing"] = testing
    async with httpx.AsyncClient() as client:
        response = await client.put(BASE_URL + "/arrived", json=payload)
    return response.status_code, response.json()

@pytest.fixture
def random_data_attendee():
    random_mispar_ishi = str(random.randrange(100000, 9999999))
    random_tehudat_zehut = str(random.randrange(100000000, 999999999))
    return random_mispar_ishi, random_tehudat_zehut

# Test cases
@pytest.mark.asyncio
async def test_attendee_arrived_missing_identifiers():
    status, data = await attendee_arrived(sent={})
    assert status == 400
    assert data["error_code"] == 101

@pytest.mark.asyncio
async def test_attendee_arrived_invalid_mispar_ishi():
    status, data = await attendee_arrived(sent={"mispar_ishi": "123", "tehudat_zehut": "123456789"})
    assert status == 400
    assert data["error_code"] == 3


@pytest.mark.asyncio
async def test_attendee_arrived_invalid_tehudat_zehut():
    status, data = await attendee_arrived(sent={"mispar_ishi": "1234567", "tehudat_zehut": "12345678"})
    assert status == 400
    assert data["error_code"] == 4


@pytest.mark.asyncio
async def test_attendee_arrived_nonexistent_attendee(random_data_attendee):
    random_mispar_ishi, random_tehudat_zehut = random_data_attendee
    status, data = await attendee_arrived(sent={"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut})
    assert status == 400
    assert data["error_code"] == 104


@pytest.mark.asyncio
async def test_attendee_arrived_valid_attendee():
    random_mispar_ishi = str(random.randrange(100000, 9999999))
    random_tehudat_zehut = str(random.randrange(100000000, 999999999))
    id = await create_get_id_attendee(random_mispar_ishi, random_tehudat_zehut)
    status, data = await attendee_arrived(sent={"mispar_ishi": random_mispar_ishi, "tehudat_zehut": random_tehudat_zehut})
    assert status == 200
    assert data["status"] == "OK"
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL + "/getby/tehudat_zehut/" + random_tehudat_zehut)
    assert response.status_code == 200
    data = response.json()["data"]
    attendee = [item for item in data if item.get("tehudat_zehut") == random_tehudat_zehut][0]
    assert attendee.get("arrived") == True

