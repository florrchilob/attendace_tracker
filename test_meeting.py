# import requests
# import json

# endpoint = "http://127.0.0.1:8000/meetings"

# def test_can_call_endpoint():
#     response  = requests.get(endpoint)
#     assert response.status_code == 200
     
# def test_insert_correct_user():
#     payload = {
#         "name":"Flori",
#         "mispar_ishi":123456789,
#         "mail":"michvee.alon@gmail.com",
#         "day":"2023-06-27",
#         "since":"22:00:00",
#         "until":"23:30:00",
#         "people_amount":100
#     }
#     response = requests.post(endpoint + "/save", json = payload)  
#     data = response.json()
#     assert data["status_code"] == 201

# def test_insert_wrong_mail():
#     payload = {
#         "name":"Flori",
#         "mispar_ishi":123456789,
#         "mail":"michvee.alon@gmail",
#         "day":"2023-06-27",
#         "since":"15:00:00",
#         "until":"15:30:00",
#         "people_amount":100
#     }
#     response = requests.post(endpoint + "/save", json = payload)
#     data = response.json()
#     assert data["status_code"] == 400 and data["error"] == 4

# def test_insert_wrong_credentials():
#     payload = {
#         "name":"Flori",
#         "mispar_ishi":123456789,
#         "mail":"michvee.alon@gmail.com",
#         "day":"2023-06-27",
#         "since":"05:00:00",
#         "until":"06:30:00",
#         "people_amount":100
#     }
#     response = requests.post(endpoint + "/save", json = payload)
#     data = response.json()
#     assert data["status_code"] == 400 and data["error"] == 3

# def test_insert_no_avaliable_licenses():
#     payload = {
#         "name":"Flori",
#         "mispar_ishi":123456789,
#         "mail":"mekahar2@gmail.com",
#         "day":"2023-06-25",
#         "since":"10:05:00",
#         "until":"17:50:00",
#         "people_amount":100
#     }
#     response = requests.post(endpoint + "/save", json = payload)
#     data = response.json()
#     assert data["status_code"] == 400 and data["error"] == 2

