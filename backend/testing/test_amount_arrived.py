import pytest
import httpx
from datetime import datetime
import random
from testing.test_create_attendees import create_get_id_attendee
import asyncio

BASE_URL = "http://127.0.0.1:8000/attendees"

@pytest.mark.asyncio
async def test_amount_arrived_flow():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/get/amountarrived")
        assert response.status_code == 200
        initial_data = response.json()["data"]
        initial_total = initial_data["total_amount"]
        initial_not_arrived = initial_data["not_arrived"]

    random_mispar_ishi = str(random.randrange(100000, 9999999))
    id = await create_get_id_attendee(random_mispar_ishi)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/get/amountarrived")
        assert response.status_code == 200
        after_add_data = response.json()["data"]
        new_total = after_add_data["total_amount"]
        new_not_arrived = after_add_data["not_arrived"]
        
        assert new_total == initial_total + 1
        assert new_not_arrived == initial_not_arrived + 1

    arrive_data = {
        "mispar_ishi": random_mispar_ishi
    }
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/arrived", json=arrive_data)
        assert response.status_code == 200

        response = await client.get(f"{BASE_URL}/get/amountarrived")
        assert response.status_code == 200
        after_arrive_data = response.json()["data"]
        arrived_total = after_arrive_data["total_amount"]
        arrived_not_arrived = after_arrive_data["not_arrived"]
        assert arrived_total == initial_total + 1
        assert arrived_not_arrived == initial_not_arrived

    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/delete/{id}")
        assert response.status_code == 200

        response = await client.get(f"{BASE_URL}/get/amountarrived")
        assert response.status_code == 200
        final_data = response.json()["data"]
        final_total = final_data["total_amount"]
        final_not_arrived = final_data["not_arrived"]
        
        assert final_total == initial_total
        assert final_not_arrived == initial_not_arrived

