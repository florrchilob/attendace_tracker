from dotenv import find_dotenv, load_dotenv
import requests
import random
import string
import os
import jwt

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

secret_key = os.getenv("secret_key")

endpoint = "http://127.0.0.1:8000/accounts"
sign_up_endpoint = endpoint + "/signup"
resend_validation_endpoint = endpoint + "/resendvalidation"
validate_account_endpoint = endpoint + "/validate"
log_in_endpoint = endpoint + "/login"
log_out_endpoint = endpoint + "/logout"
forgot_password_endpoint = endpoint + "/forgotpassword"
new_password_endpoint = endpoint + "/newpassword"
update_account_endpoint = endpoint + "/updateaccount"
get_accounts_authorize_endpoint = endpoint + "/getaccountsauthorize"
authorize_account_endpoint = endpoint + "/authorizeaccount"
get_accounts_endpoint = endpoint + "/getaccounts"
create_admin_endpoint = endpoint + "/createadmin"
get_my_account_endpoint = endpoint + "/getmyaccount"

def test_call_endpoint():
    return (requests.get(endpoint)).status_code

def sign_up(mail = None, password = None, name = None, mispar_ishi = None, telephone = None, payload = None, testing = None, answer = None):
    random_mail = ""
    for i in range(random.randrange(99)):
        random_mail = random_mail + random.choice(string.ascii_lowercase)
    random_mail = str("juanperez" + random_mail + "@gmail.com")
    random_mispar_ishi = random.randrange(1000000, 99999999999)
    random_password = ""
    for i in range(random.randrange(5, 99)):
        random_password = str(random_password + random.choice(string.ascii_letters))
    random_number = random.randint(1, 100)
    random_password = random_password + str(random_number)
    payload = {
        "mail": random_mail,
        "password": random_password ,
        "name":  "Juan Perez",
        "mispar_ishi": random_mispar_ishi,
        "telephone": 123654789
    }
    variables = {"mail": mail, "password": password, "name": name, "mispar_ishi": mispar_ishi, "telephone": telephone, "testing": testing}
    for key, value in variables.items():
        if value is not None:
            if value == False: 
                del payload[key]
            else:
                payload[key] = value
    response = requests.post(sign_up_endpoint, json = payload)
    status_code = response.status_code
    if status_code == 400:
        data = response.json()
        error = data["error"]
        if mail == None and mispar_ishi == None:
            while error == 14:
                random_mail = ""
                for i in range(random.randrange(99)):
                    random_mail = random_mail + random.choice(string.ascii_lowercase)
                random_domain = ""
                for i in range(random.randrange(99)):
                    random_domain = random_domain + random.choice(string.ascii_lowercase)
                random_mail = random_mail + "@" + random_domain + ".com"
                payload[mail] = random_mail
                random_mispar_ishi = random.randrange(1000000, 99999999999)
                payload[mispar_ishi] = random_mispar_ishi
                response = requests.post(sign_up_endpoint, json = payload)
                error = (response.json())["error"]
    if answer == 0:
        return response.status_code
    if answer == 1:
        return response.status_code, random_mail
    data = response.json()
    if answer == 2:
        return response.status_code, data["data"]
    if answer == 3: 
        return response.status_code, data["data"], random_mail, random_password
    if answer == 4: 
        return response.status_code, data["data"], random_mail, random_password, random_mispar_ishi
    if answer == 5: 
        content = data["data"]
        return response.status_code, content["id"], content["token"]
    return response.status_code, data["error"]


def resend_validation(mail = None, testing = None, answer = None):
    payload = {
        "mail": mail
    }
    if testing != None:
        payload["testing"] = testing
    response = requests.post(resend_validation_endpoint, json = payload)
    data = response.json()
    if answer == 1:
        return response.status_code
    return response.status_code, data["error"]

def validate_account(token = "", testing = None, answer = None):
    if testing != None:
        payload = {
            "testing": testing
        }
        response = requests.put(validate_account_endpoint + "/" + token, json = payload)
    else:
        response = requests.put(validate_account_endpoint + "/" + token)
    data = response.json()
    if answer == 1:
        return response.status_code
    return response.status_code, data["error"]

def log_in(mail = None, password = None, answer = None, testing = None):
    payload = {
        "mail" : mail,
        "password": password
    }
    if testing != None:
        payload["testing"] = testing
    response = requests.post(log_in_endpoint, json = payload)
    data = response.json()
    if answer == 1:
        content = data["data"]
        token = content["token"]
        return response.status_code, token
    error = data["error"]
    return response.status_code, error

def log_out(token = None, headers = None, answer = None):
    if headers == None:
        headers = {
            "JWToken" : token
        }
    response = requests.post(log_out_endpoint, headers = headers)
    if answer == 1:
        return response.status_code
    data = response.json()
    if response.status_code == 422:
        error = 0
    else:    
        error = data["error"]
    return response.status_code, error

def forgot_password(mail = None, payload = None, answer = None, testing = None):
    if payload == None:
        payload = {
            "mail" : mail
        }
        if testing != None:
            payload["testing"] = testing
    response = requests.post(forgot_password_endpoint, json = payload)
    if answer == 1:
        return response.status_code
    if answer == 2: 
        data = response.json()
        token = data["data"]
        return response.status_code, token
    data = response.json()
    error = data["error"]
    return response.status_code, error

def new_password(mispar_ishi= None, password= None, token= "", testing = None, answer = None):
    payload={
        "mispar_ishi": mispar_ishi,
        "password": password
    }
    if mispar_ishi == False:
        payload = {
            "password": password
        }
    if password == False:
        payload = {
            "mispar_ishi": mispar_ishi
        }
    if testing != None:
        payload["testing"] = testing
    response = requests.put(new_password_endpoint + "/" + token, json = payload)
    if answer == 1:
        return response.status_code
    data = response.json()  
    return response.status_code, data["error"]

def update_account(JWT_token = None, to_update = {}, testing = None, answer = None, payload = None):
    payload = {}
    headers = {}
    if JWT_token != None:
        headers = {
                "JWToken" : JWT_token
            }
    for key, value in to_update.items():
        payload[key] = value
    if testing != None:
        payload["testing"] = testing
    response = requests.put(update_account_endpoint, json = payload, headers = headers)
    if answer == 1:
        return response.status_code
    data = response.json()
    if response.status_code == 422:
        error = 0
    else:    
        error = data["error"]
    return response.status_code, error

def encode_JWT_token(token = None, account_id = None):
    payload = {}
    variables = {"token": token, "account_id": account_id}
    for key, value in variables.items(): 
        if value != None:
            payload[key] = value
    JWT_token = jwt.encode(payload, secret_key, algorithm='HS256')
    return JWT_token

def get_accounts_authorize(JWT_token = None, answer = None, testing = None):
    payload = {}
    headers = {}
    if JWT_token != False:
        headers = {
            "JWToken": JWT_token
        }
    if testing != None:
        payload["testing"] = testing
    response = requests.get(get_accounts_authorize_endpoint, json = payload, headers = headers)
    data = response.json()
    if answer == 1:
        list = data["data"]
        return response.status_code, list
    if response.status_code == 422:
        error = 0
    else:    
        error = data["error"]
    return response.status_code, error

def get_my_account(JWT_token = None, answer = None, testing = None):
    headers = {}
    if JWT_token != False:
        headers = {
            "JWToken": JWT_token
        }
    if testing != None:
        headers["testing"] = testing
    response = requests.get(get_my_account_endpoint, headers= headers)
    data = response.json()
    if answer == 1:
        list = data["data"]
        return response.status_code, list
    if response.status_code == 422:
        error = 0 
    else:
        error = data["error"]
    return response.status_code, error

def authorize_account(JWT_token = None, account_id = None, testing = None, answer = None, payload = None):
    payload = {}
    headers = {}
    if JWT_token != False:
        headers = {
            "JWToken": JWT_token
        }
    if account_id != None:
        payload["account_id"] = account_id
    if testing != None:
        payload["testing"] = testing
    response = requests.put(authorize_account_endpoint, json = payload, headers = headers)
    data = response.json()
    if answer == 1:
        return response.status_code
    if response.status_code == 422:
        error = 0
    else:    
        error = data["error"]
    return response.status_code, error
    
def get_accounts(JWT_token = None, testing = None, answer = None):
    payload = {}
    headers = {}
    if JWT_token != False:
        headers = {
            "JWToken": JWT_token
        }
    if testing != None:
        payload["testing"] = testing
    response = requests.get(get_accounts_endpoint, json = payload, headers = headers)
    data = response.json()
    if answer == 1:
        list = data["data"]
        return response.status_code, list
    if response.status_code == 422:
        error = 0
    else:    
        error = data["error"]
    return response.status_code, error
def create_admin(JWT_token = None, testing = None, account_id = None, account_type = None, answer = None):
    payload = {}
    headers = {}
    variables = {"JWT_token": JWT_token, "testing": testing, "account_id": account_id, "account_type": account_type}
    if JWT_token != False:
        headers = {
            "JWToken": JWT_token
        }
    if testing != None:
        payload["testing"] = testing
    for key, value in variables.items():
        if value != None:
            payload[key] = value
    response = requests.post(create_admin_endpoint, json = payload, headers = headers)
    if answer == 1:
        return response.status_code
    data = response.json()
    if response.status_code == 422:
        error = 0
    else:    
        error = data["error"]
    return response.status_code, error