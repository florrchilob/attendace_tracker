from testing import helper_tests
from dotenv import find_dotenv, load_dotenv
import string
import random
import jwt
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

secret_key = os.getenv("secret_key")

def test_call_endpoint():
    response = helper_tests.test_call_endpoint()
    assert response == 200

def test_get_my_account_missing_JWT_token():
    response, error = helper_tests.get_my_account(JWT_token= False)
    assert (response == 400 and error == 16) or response == 422

def test_get_my_account_JWT_token_empty():
    response, error = helper_tests.get_my_account(JWT_token= "")
    assert response == 400 and error == 16

    
def test_get_my_account_wrong_JWT_token():
    random_JWT_token = str(random.randrange(1000000, 99999999999)) + "." + str(random.randrange(1000000, 99999999999))+ "." + str(random.randrange(1000000, 99999999999))
    response, error = helper_tests.get_my_account(JWT_token= str(random_JWT_token))
    assert response == 400 and error == 16
    
def test_get_my_account_missing_token():
    token = helper_tests.encode_JWT_token(account_id= 1)
    response, error = helper_tests.get_my_account(JWT_token= token, testing= "token")
    assert response == 400 and error == 16

def test_get_my_account_token_wrong_type():
    token = helper_tests.encode_JWT_token(token= 123)
    response, error = helper_tests.get_my_account(JWT_token= token)
    assert response == 400 and error == 16

def test_get_my_account_account_id_wrong_type():
    token = helper_tests.encode_JWT_token(account_id="123456")
    response, error = helper_tests.get_my_account(JWT_token= token)
    assert response == 400 and error == 16


def test_get_my_account_wrong_token():
    response, token, mail, password = helper_tests.sign_up(testing = True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    token_decoded = jwt.decode(token, secret_key, algorithms='HS256')
    random_token = random.randrange(1000000, 99999999999)
    JWT_token = helper_tests.encode_JWT_token(account_id=token_decoded["account_id"], token=str(random_token))
    response, error = helper_tests.get_my_account(JWT_token= str(JWT_token), testing= "token")
    assert response == 400 and error == 16

def test_get_my_account_ok():
    response, token, mail, password = helper_tests.sign_up(testing = True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    token_decoded = jwt.decode(token, secret_key, algorithms='HS256')
    random_token = random.randrange(1000000, 99999999999)
    JWT_token = helper_tests.encode_JWT_token(account_id=token_decoded["account_id"], token=token_decoded["token"])
    response, data = helper_tests.get_my_account(JWT_token=str(JWT_token), testing="type", answer=1)
    assert response == 200 and data != ""