from testing import helper_tests
import string
import random

def test_call_endpoint():
    response = helper_tests.test_call_endpoint()
    assert response == 200

def test_new_password_missing_token():
    response = helper_tests.new_password(answer= 1)
    assert response == 404

def test_new_password_token_wrong_type():
    response, data = helper_tests.new_password(mispar_ishi= 123456, password= "123456", testing= "wrong_type", token = "123")
    assert response == 400 and data == 16

def test_new_password_missing_password():
    response, token, mail, password, mispar_ishi = helper_tests.sign_up(testing = True, answer= 4)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.forgot_password(mail= mail, testing = True, answer= 2)
    assert response == 200
    response, data = helper_tests.new_password(password= False, mispar_ishi= mispar_ishi, token= token)
    assert response == 400 and data == 11
    
def test_new_password_missing_mispar_ishi():
    response, token, mail, password, mispar_ishi = helper_tests.sign_up(testing = True, answer= 4)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.forgot_password(mail= mail, testing = True, answer= 2)
    assert response == 200
    response, data = helper_tests.new_password(password= password, mispar_ishi= False, token= token)
    assert response == 400 and data == 3
    
def test_new_password_password_empty():
    response, token, mail, password, mispar_ishi = helper_tests.sign_up(testing = True, answer= 4)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.forgot_password(mail= mail, testing = True, answer= 2)
    assert response == 200
    response, data = helper_tests.new_password(password= "", mispar_ishi= mispar_ishi, token= token)
    assert response == 400 and data == 11


def test_new_password_password_wrong_type():
    response, token, mail, password, mispar_ishi = helper_tests.sign_up(testing = True, answer= 4)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.forgot_password(mail= mail, testing = True, answer= 2)
    assert response == 200
    response, data = helper_tests.new_password(password= 123, mispar_ishi= mispar_ishi, token= token)
    assert response == 400 and data == 11
    
def test_new_password_mispar_ishi_wrong_type():
    response, token, mail, password, mispar_ishi = helper_tests.sign_up(testing = True, answer= 4)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.forgot_password(mail= mail, testing = True, answer= 2)
    assert response == 200
    response, data = helper_tests.new_password(password= password, mispar_ishi= "abc", token= token)
    assert response == 400 and data == 3

def test_new_password_token_incorrect():
    response, token, mail, password, mispar_ishi = helper_tests.sign_up(testing = True, answer= 4)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response = helper_tests.forgot_password(mail= mail, testing = True, answer= 1)
    assert response == 200
    random_token = ""
    for i in range(random.randrange(16)):
        random_token += random.choice(string.ascii_lowercase)
    response, data = helper_tests.new_password(password= password, mispar_ishi= mispar_ishi, token= random_token)
    assert response == 400 and data == 16

def test_new_password_wrong_mispar_ishi():
    response, token, mail, password, mispar_ishi = helper_tests.sign_up(testing = True, answer= 4)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.forgot_password(mail= mail, testing = True, answer= 2)
    assert response == 200
    random_mispar_ishi = random.randrange(1000000, 99999999999)
    response, data = helper_tests.new_password(password= password, mispar_ishi= random_mispar_ishi, token= token)
    assert response == 400 and data == 3

def test_new_password_token_expirated():
    response, token, mail, password, mispar_ishi = helper_tests.sign_up(testing = True, answer= 4)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.forgot_password(mail= mail, testing = True, answer= 2)
    assert response == 200
    response, data = helper_tests.new_password(password= password, mispar_ishi= mispar_ishi, token= token, testing= "expirated")
    assert response == 400 and data == 15.1

def test_new_password_ok():
    response, token, mail, password, mispar_ishi = helper_tests.sign_up(testing = True, answer= 4)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.forgot_password(mail= mail, testing = True, answer= 2)
    assert response == 200
    response = helper_tests.new_password(password= password, mispar_ishi= mispar_ishi, token= token, answer= 1)
    assert response == 200
    
