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

def test_get_accounts_authorize_missing_JWT_token():
    response, error = helper_tests.get_accounts_authorize(JWT_token= False)
    assert (response == 400 and error == 16) or response == 422

def test_get_accounts_authorize_JWT_token_empty():
    response, error = helper_tests.get_accounts_authorize(JWT_token= "")
    assert response == 400 and error == 16
    
def test_get_accounts_authorize_wrong_JWT_token():
    random_JWT_token = str(random.randrange(1000000, 99999999999)) + "." + str(random.randrange(1000000, 99999999999))+ "." + str(random.randrange(1000000, 99999999999))
    response, error = helper_tests.get_accounts_authorize(JWT_token= random_JWT_token)
    assert response == 400 and error == 16
    
def test_get_accounts_authorize_missing_token():
    token = helper_tests.encode_JWT_token(account_id= 1)
    response, error = helper_tests.get_accounts_authorize(JWT_token= token, testing= "token")
    assert response == 400 and error == 16

def test_get_accounts_authorize_missing_account_id():
    random_JWT_token = str(random.randrange(1000000, 99999999999)) + "." + str(random.randrange(1000000, 99999999999))+ "." + str(random.randrange(1000000, 99999999999))
    token = helper_tests.encode_JWT_token(token= random_JWT_token)
    response, error = helper_tests.get_accounts_authorize(JWT_token= token)
    assert response == 400 and error == 16

def test_get_accounts_authorize_token_wrong_type():
    token = helper_tests.encode_JWT_token(token= 123)
    response, error = helper_tests.get_accounts_authorize(JWT_token= token)
    assert response == 400 and error == 16

def test_get_accounts_authorize_account_id_wrong_type():
    token = helper_tests.encode_JWT_token(account_id="123456")
    response, error = helper_tests.get_accounts_authorize(JWT_token= token)
    assert response == 400 and error == 16

def test_get_accounts_authorize_wrong_account_id():
    response, token, mail, password = helper_tests.sign_up(testing = True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    token_decoded = jwt.decode(token, secret_key, algorithms='HS256')
    random_id = random.randrange(1000000, 99999999999)
    JWT_token = helper_tests.encode_JWT_token(account_id=random_id, token= token_decoded["token"])
    response, error = helper_tests.get_accounts_authorize(JWT_token= JWT_token, testing= "token")
    assert response == 400 and error == 16

def testget_accounts_authorize_wrong_token():
    response, token, mail, password = helper_tests.sign_up(testing = True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    token_decoded = jwt.decode(token, secret_key, algorithms='HS256')
    random_token = random.randrange(1000000, 99999999999)
    JWT_token = helper_tests.encode_JWT_token(account_id=token_decoded["account_id"], token=random_token)
    response, error = helper_tests.get_accounts_authorize(JWT_token= JWT_token, testing= "token")
    assert response == 400 and error == 16

def test_get_accounts_authorize_wrong_type_account():
    response, token, mail, password = helper_tests.sign_up(testing = True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    token_decoded = jwt.decode(token, secret_key, algorithms='HS256')
    random_token = random.randrange(1000000, 99999999999)
    JWT_token = helper_tests.encode_JWT_token(account_id=token_decoded["account_id"], token=token_decoded["token"])
    response, error = helper_tests.get_accounts_authorize(JWT_token=JWT_token)
    assert response == 400 and error == 17

def test_get_accounts_authorize_ok():
    response, token, mail, password = helper_tests.sign_up(testing = True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    token_decoded = jwt.decode(token, secret_key, algorithms='HS256')
    random_token = random.randrange(1000000, 99999999999)
    JWT_token = helper_tests.encode_JWT_token(account_id=token_decoded["account_id"], token=token_decoded["token"])
    response, data = helper_tests.get_accounts_authorize(JWT_token=JWT_token, testing="type", answer=1)
    assert response == 200 and data != ""