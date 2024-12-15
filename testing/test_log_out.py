from testing import helper_tests
from dotenv import find_dotenv, load_dotenv
import string
import random
import jwt
import os

secret_key = os.getenv("secret_key")

def test_call_endpoint():
    response = helper_tests.test_call_endpoint()
    assert response == 200

def test_log_out_missing_JWT_token():
    response, error = helper_tests.log_out(headers= {})
    assert (response == 400 and error == 16) or response == 422
    
def test_log_out_JWT_token_empty():
    response, error = helper_tests.log_out(token= "")
    assert response == 400 and error == 16

def test_log_out_wrong_JWT_token():
    random_JWT_token = str(random.randrange(1000000, 99999999999)) + "." + str(random.randrange(1000000, 99999999999))+ "." + str(random.randrange(1000000, 99999999999))
    response, error = helper_tests.log_out(token= random_JWT_token)
    assert response == 400 and error == 16
    
def test_log_out_missing_token():
    token = helper_tests.encode_JWT_token(account_id= 1)
    response, error = helper_tests.log_out(token= token)
    assert response == 400 and error == 16

def test_log_out_missing_account_id():
    random_token = ""
    for i in range(random.randrange(16)):
        random_token = random_token + random.choice(string.ascii_lowercase)
    token = helper_tests.encode_JWT_token(token= random_token)
    response, error = helper_tests.log_out(token= token)
    assert response == 400 and error == 16

def test_log_out_token_wrong_type():
    token = helper_tests.encode_JWT_token(account_id= 1, token= 123)
    response, error = helper_tests.log_out(token= token)
    assert response == 400 and error == 16

def test_log_out_account_id_wrong_type():
    random_token = ""
    for i in range(random.randrange(16)):
        random_token = random_token + random.choice(string.ascii_lowercase)
    token = helper_tests.encode_JWT_token(account_id= "123456", token= str(random_token))
    response, error = helper_tests.log_out(token= token)
    assert response == 400 and error == 16

def test_log_out_wrong_account_id():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    token_decoded = jwt.decode(token, secret_key, algorithms='HS256')
    random_id = random.randrange(1000000, 99999999999)
    token = helper_tests.encode_JWT_token(account_id= random_id, token= token_decoded["token"])
    response, error = helper_tests.log_out(token= token)
    assert response == 400 and error == 16

def test_log_out_wrong_token():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    token_decoded = jwt.decode(token, secret_key, algorithms='HS256')
    random_token = random.randrange(1000000, 99999999999)
    token = helper_tests.encode_JWT_token(account_id= token_decoded["account_id"], token= random_token )
    response, error = helper_tests.log_out(token= token)
    assert response == 400 and error == 16

def test_log_out_no_needed():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    helper_tests.log_out(token= token, answer= 1)
    response, error = helper_tests.log_out(token= token)
    assert response == 400 and error == 15

def test_log_out_ok():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    response = helper_tests.log_out(token= token, answer= 1)
    assert response == 200