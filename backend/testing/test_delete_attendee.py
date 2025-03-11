import pytest
import requests
import random
from testing.test_create_attendees import create_get_id_attendee
import asyncio
import httpx

# Add mock for testing database error

# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

# Helper function to send DELETE requests
async def delete_attendee(id, testing=None):
    headers = {}
    if testing:
        headers["testing"] = testing
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/delete/{id}", headers=headers)
    return response.status_code, response.json()

@pytest.fixture
def random_id():
    return random.randint(1000, 9999)

# Test cases

@pytest.mark.asyncio
async def test_delete_attendee_valid_id():
    attendee_id = await create_get_id_attendee()
    status, data = await delete_attendee(attendee_id)
    assert status == 200
    assert data["status"] == "OK"

@pytest.mark.asyncio
async def test_delete_attendee_missing_id():
    status, data = await delete_attendee(id="")
    assert status == 400 and data["error_code"] == 102 or status == 404

@pytest.mark.asyncio
async def test_delete_attendee_nonexistent_id():
    status, data = await delete_attendee(id=99999999)
    assert status == 400
    assert data["error_code"] == 102

@pytest.mark.asyncio
async def test_delete_attendee_invalid_id():
    status, data = await delete_attendee(id="invalid")
    assert status == 400 and data["error_code"] == 102 or status == 422

@pytest.mark.asyncio
async def test_delete_attendee_negative_id():
    status, data = await delete_attendee(id=-1)
    assert status == 400
    assert data["error_code"] == 102

