import os
import requests
import random
import string
from dotenv import find_dotenv, load_dotenv

# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# API endpoints
base_url = "http://127.0.0.1:8000/attendees"
create_attendees_endpoint = base_url + "/create"

def create_attendees(sent=None, testing=None, answer=None):
    # Default payload
    if sent is None:
        sent = {}

    payload = {"attendees": sent.get("attendees", [])}

    # Add testing flag if provided
    if testing:
        payload["testing"] = True

    # Send POST request
    response = requests.post(create_attendees_endpoint, json=payload)
    status_code = response.status_code

    # Parse response
    data = response.json() if response.status_code != 422 else {}
    error = data.get("error", 0)

    # Handle different answer types
    if answer == 0:
        return status_code
    if answer == 1:
        return status_code, data
    if answer == 2:
        return status_code, data.get("data", {})
    if answer == 3:
        return status_code, data.get("data", {}), payload

    return status_code, error
