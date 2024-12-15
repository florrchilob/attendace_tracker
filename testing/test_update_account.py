from testing import helper_tests
import string
import random
import jwt
import os


def test_call_endpoint():
    response = helper_tests.test_call_endpoint()
    assert response == 200

def test_update_account_missing_JWT_token():
    response, error = helper_tests.update_account(payload= {})
    assert (response == 400 and error == 16) or response == 422

def test_update_account_JWT_token_empty():
    response, error = helper_tests.update_account(JWT_token= "")
    assert response == 400 and error == 16

def test_update_account_wrong_JWT_token():
    random_JWT_token = str(random.randrange(1000000, 99999999999)) + "." + str(random.randrange(1000000, 99999999999))+ "." + str(random.randrange(1000000, 99999999999))
    response, error = helper_tests.update_account(JWT_token= random_JWT_token)
    assert response == 400 and error == 16 

def test_update_account_missing_token():
    token = helper_tests.encode_JWT_token(account_id= 1)
    response, error = helper_tests.update_account(JWT_token= token)
    assert response == 400 and error == 16

def test_update_account_missing_account_id():
    random_token = ""
    for i in range(random.randrange(16)):
        random_token = random_token + random.choice(string.ascii_lowercase)
    token = helper_tests.encode_JWT_token(token= random_token)   
    response, error = helper_tests.update_account(JWT_token= token)
    assert response == 400 and error == 16

def test_update_account_token_wrong_type():
    token = helper_tests.encode_JWT_token(token= 123, account_id= 1)   
    response, error = helper_tests.update_account(JWT_token= token)
    assert response == 400 and error == 16

def test_update_account_id_wrong_type():
    random_token = ""
    for i in range(random.randrange(16)):
        random_token = random_token + random.choice(string.ascii_lowercase)
    token = helper_tests.encode_JWT_token(token= str(random_token), account_id= "123456")   
    response, error = helper_tests.update_account(JWT_token= token)
    assert response == 400 and error == 16
    
def test_update_account_wrong_old_password():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_password = ""
    for i in range(random.randrange(99)):
        random_password = random_password + random.choice(string.ascii_letters)
    random_number = random.randint(1, 100)
    random_password = random_password + str(random_number)
    response, error = helper_tests.update_account(JWT_token= JWT_token, testing= "old_password", to_update= {"old_password": random_password, "password": "ABCabc123"})
    assert response == 400 and error == 4.2

def test_update_account_id():
    random_token = random.randrange(1000000, 99999999999)
    random_id = random.randrange(1000000, 99999999999)
    response, error = helper_tests.update_account(JWT_token= str(random_token), to_update= {"account_id": random_id})
    assert response == 400 and error == 101

def test_update_account_repeated_mail():
    response, token, mail2, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    response, error = helper_tests.update_account(JWT_token= JWT_token, testing= "repeated_mail", to_update= {"mail": mail2})
    assert response == 400 and error == 4

def test_update_account_mail():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_new_mail = ""
    for i in range(random.randrange(99)):
        random_new_mail = random_new_mail + random.choice(string.ascii_lowercase)
    random_new_mail = "perezjuan" + random_new_mail + "@gmail.com"
    response, error = helper_tests.update_account(JWT_token= JWT_token, testing= "mail", to_update= {"mail": random_new_mail})
    assert response == 400 and error == 15.1

def test_update_account_not_validated():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1, testing = "update_account")
    assert response == 200 and token != ""
    random_new_mail = ""
    for i in range(random.randrange(99)):
        random_new_mail = random_new_mail + random.choice(string.ascii_lowercase)
    random_new_mail = "perezjuan" + random_new_mail + "@gmail.com"
    response, error = helper_tests.update_account(JWT_token= JWT_token, to_update= {"mail": random_new_mail})
    assert response == 400 and error == 15.1

def test_update_account_not_authorized():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_new_mail = ""
    for i in range(random.randrange(99)):
        random_new_mail = random_new_mail + random.choice(string.ascii_lowercase)
    random_new_mail = "perezjuan" + random_new_mail + "@gmail.com"
    response, error = helper_tests.update_account(JWT_token= JWT_token, to_update= {"mail": random_new_mail})    
    assert response == 400 and error == 17

def test_update_account_email_wrong_type():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_wrong_mail = random.randrange(1000000, 99999999999)
    response, error = helper_tests.update_account(JWT_token= JWT_token, testing= "type", to_update= {"mail": random_wrong_mail})    
    assert response == 400 and error == 4

def test_update_account_name_wrong_type():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_wrong_name = random.randrange(1000000, 99999999999)
    response, error = helper_tests.update_account(JWT_token= JWT_token, testing= "type", to_update= {"name": random_wrong_name})  
    assert response == 400 and error == 1

def test_update_account_mispar_ishi():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_mispar_ishi = random.randrange(1000000, 99999999999)
    response, error = helper_tests.update_account(JWT_token= JWT_token, to_update= {"mispar_ishi": random_mispar_ishi})  
    assert response == 400 and error == 101

def test_update_account_telephone_wrong_type():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_telephone = random.randrange(1000000, 99999999999)
    response, error = helper_tests.update_account(JWT_token= JWT_token, testing= "type", to_update= {"telephone": str(random_telephone)})  
    assert response == 400 and error == 13
    
def test_update_account_account_type():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    response, error = helper_tests.update_account(JWT_token= JWT_token, to_update= {"account_type": 2})  
    assert response == 400 and error == 101

def test_update_account_validated():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    response, error = helper_tests.update_account(JWT_token= JWT_token, testing= True, to_update= {"validated": True})  
    assert response == 400 and error == 101
    
def test_update_account_authorized():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    response, error = helper_tests.update_account(JWT_token= JWT_token, to_update= {"authorized": True})  
    assert response == 400 and error == 101

def test_update_account_token():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_token = random.randrange(1000000, 99999999999)
    response, error = helper_tests.update_account(JWT_token= JWT_token, to_update= {"token": random_token})  
    assert response == 400 and error == 101

def test_update_account_refresh_token():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_token = random.randrange(1000000, 99999999999)
    response, error = helper_tests.update_account(JWT_token= JWT_token, to_update= {"refresh_token": random_token})
    assert response == 400 and error == 101

def test_update_account_token_expiration():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_token = random.randrange(1000000, 99999999999)
    response, error = helper_tests.update_account(JWT_token= JWT_token, to_update= {"token_expiration": random_token})
    assert response == 400 and error == 101

def test_update_account_ok():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200   
    response, JWT_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
    random_telephone = random.randrange(100000000, 999999999)
    random_password = ""
    for i in range(random.randrange(99)):
        random_password = random_password + random.choice(string.ascii_letters)
    random_number = random.randint(1, 100)
    random_password = random_password + str(random_number)
    random_name = ""
    for i in range(random.randrange(99)):
        random_name = random_name + random.choice(string.ascii_lowercase)
    random_surname = ""
    for i in range(random.randrange(99)):
        random_surname = random_surname + random.choice(string.ascii_lowercase)
    random_name = random_name + " " + random_surname
    response = helper_tests.update_account(JWT_token= JWT_token, testing= "ok", to_update= {"telephone": random_telephone, "password": random_password, "name": random_name}, answer= 1)
    assert response == 200