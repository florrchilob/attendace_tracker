from testing import helper_tests
import string
import random

def test_call_endpoint():
    response = helper_tests.test_call_endpoint()
    assert response == 200

def test_validate_account_missing_token():
    response = helper_tests.validate_account(answer= 1)
    assert response == 404
    
def test_validate_account_empty_token():
    response = helper_tests.validate_account(token= "", answer= 1 )
    assert response == 404

def test_validate_account_token_wrong_type():
    response, error = helper_tests.validate_account(token= "123", testing= "wrong_type")
    assert response == 400 and error == 16

def test_validate_account_token_incorrect():
    random_token = ""
    for i in range(random.randrange(16)):
        random_token += random.choice(string.ascii_lowercase)
    response, error = helper_tests.validate_account(token= random_token)
    assert response == 400 and error == 16  

def test_validate_account_validated():
    response, token = helper_tests.sign_up(testing= True, answer= 2)
    assert response == 201
    response, error = helper_tests.validate_account(token= token, testing= "validated")
    assert response == 400 and error == 15
    
def test_validate_account_refresh_token_incorrect():
    response, token = helper_tests.sign_up(testing= True, answer= 2)
    assert response == 201
    response, error = helper_tests.validate_account(token= token, testing= "wrong_refresh_token")
    assert response == 400 and error == 15.1

def test_validate_account_token_expiration_incorrect():
    response, token = helper_tests.sign_up(testing= True, answer= 2)
    assert response == 201
    response, error = helper_tests.validate_account(token= token, testing= "wrong_expiration")
    assert response == 400 and error == 15.1

def test_validate_account_token_expirated():
    response, token = helper_tests.sign_up(testing= True, answer= 2)
    assert response == 201
    response, error = helper_tests.validate_account(token= token, testing= "expirated")
    assert response == 400 and error == 15.1

def test_validate_account_ok():
    response, token = helper_tests.sign_up(testing= True, answer= 2)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  