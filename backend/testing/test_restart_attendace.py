import pytest
import requests
import random
from testing.test_attendee_arrived import test_attendee_arrived_valid_attendee

# Base URL for testing
BASE_URL = "http://127.0.0.1:8000/attendees"

def test_restart_attendace():
    test_attendee_arrived_valid_attendee()
    response = requests.put(BASE_URL + "/restart")
    assert response.status_code == 200
    response = requests.get(BASE_URL + "/get")
    assert response.status_code == 200
    data = response.json()["data"]
    attendees_not_arrived = [item for item in data if item.get("arrived") == False]
    assert len(data) == len(attendees_not_arrived)