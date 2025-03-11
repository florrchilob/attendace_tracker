import pytest
import requests
import random
from testing.test_attendee_arrived import test_attendee_arrived_valid_attendee
from testing.test_create_attendees import create_get_id_attendee
import asyncio

# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

@pytest.mark.asyncio
async def test_restart_attendace():
    random_mispar_ishi = str(random.randrange(100000000, 999999999))
    await create_get_id_attendee(random_mispar_ishi)
    await test_attendee_arrived_valid_attendee()
    response = requests.put(BASE_URL + "/restart")
    assert response.status_code == 200
    response = requests.get(BASE_URL + "/getby/mispar_ishi/" + random_mispar_ishi)
    assert response.status_code == 200
    data = response.json()["data"]
    attendees_not_arrived = [item for item in data if item.get("arrived") == False]
    assert len(data) == len(attendees_not_arrived)