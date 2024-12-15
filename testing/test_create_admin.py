from testing import helper_tests
from dotenv import find_dotenv, load_dotenv
import string
import random
import jwt 
import os


endpoint = "http://127.0.0.1:8000/accounts"
create_admin_endpoint = endpoint + "/createadmin"

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

secret_key = os.getenv("secret_key")

def test_call_endpoint():
    response = helper_tests.test_call_endpoint()
    assert response == 200

def test_create_admin_missing_JWT_token():
    response, error = helper_tests.create_admin()
    assert (response == 400 and error == 16) or response == 422

def test_create_admin_JWT_token_empty():
    response, error = helper_tests.create_admin(JWT_token="", account_id=1, account_type=3)
    assert response == 400 and error == 16

    
def test_create_admin_wrong_JWT_token():
    random_JWT_token = str(random.randrange(1000000, 99999999999)) + "." + str(random.randrange(1000000, 99999999999))+ "." + str(random.randrange(1000000, 99999999999))
    response, error = helper_tests.create_admin(JWT_token=random_JWT_token, account_id=1, account_type=3)
    assert response == 400 and error == 16
    
def test_create_admin_missing_id_to_authorize():
    response, admin_token, admin_mail, admin_password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= admin_token, answer= 1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail= admin_mail, password= admin_password, answer= 1)
    assert response == 200 and admin_token != ""
    response, error = helper_tests.create_admin(JWT_token=admin_token, testing="type", account_type=3)
    assert response == 400 and error == 18

def test_create_admin_type_wrong():
    response, admin_token, admin_mail, admin_password = helper_tests.sign_up(testing=True, answer=3)
    assert response == 201
    response = helper_tests.validate_account(token=admin_token, answer=1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail=admin_mail, password=admin_password, answer=1)
    assert response == 200 and admin_token != ""
    response, error = helper_tests.create_admin(JWT_token=admin_token, testing="type", account_type=-99, account_id=1)
    assert response == 400 and error == 19

def test_create_admin_type_wrong_type():
    response, admin_token, admin_mail, admin_password = helper_tests.sign_up(testing=True, answer=3)
    assert response == 201
    response = helper_tests.validate_account(token=admin_token, answer=1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail=admin_mail, password=admin_password, answer=1)
    assert response == 200 and admin_token != ""
    response, error = helper_tests.create_admin(JWT_token=admin_token, testing="type", account_type="1", account_id=1)
    assert response == 400 and error == 19

def test_create_admin_type_missing():
    response, admin_token, admin_mail, admin_password = helper_tests.sign_up(testing=True, answer=3)
    assert response == 201
    response = helper_tests.validate_account(token=admin_token, answer=1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail=admin_mail, password=admin_password, answer=1)
    assert response == 200 and admin_token != ""
    response, error = helper_tests.create_admin(JWT_token=admin_token, testing="type", account_id=1)
    assert response == 400 and error == 19

def test_create_admin_id_to_auth_wrong_type():
    response, admin_token, admin_mail, admin_password = helper_tests.sign_up(testing=True, answer=3)
    assert response == 201
    response = helper_tests.validate_account(token=admin_token, answer=1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail=admin_mail, password=admin_password, answer=1)
    assert response == 200 and admin_token != ""
    response, error = helper_tests.create_admin(JWT_token=admin_token, testing="type", account_type=3, account_id="123456")
    assert response == 400 and error == 18

def test_create_admin_missing_token():
    token = helper_tests.encode_JWT_token(account_id=1)
    response, error = helper_tests.create_admin(JWT_token=token, account_id=1, account_type=3)
    assert response == 400 and error == 16

def test_create_admin_missing_account_id():
    random_token = ""
    for i in range(random.randrange(16)):
        random_token = random_token + random.choice(string.ascii_lowercase)
    token = helper_tests.encode_JWT_token(token=random_token)
    response, error = helper_tests.create_admin(JWT_token=token, account_id=1, account_type=3)
    assert response == 400 and error == 16

def test_create_admin_token_wrong_type():
    token = helper_tests.encode_JWT_token(token=123, account_id=1)
    response, error = helper_tests.create_admin(JWT_token=token, account_id=1, account_type=3)
    assert response == 400 and error == 16

def test_create_admin_account_id_wrong_type():
    random_token = ""
    for i in range(random.randrange(16)):
        random_token = random_token + random.choice(string.ascii_lowercase)
    token = helper_tests.encode_JWT_token(token=random_token, account_id="123456")
    response, error = helper_tests.create_admin(JWT_token=token, account_id=1, account_type=3)
    assert response == 400 and error == 16

def test_create_admin_wrong_account_id():
    response, admin_token, admin_mail, admin_password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= admin_token, answer= 1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail= admin_mail, password= admin_password, answer= 1)
    assert response == 200 and admin_token != ""
    token_decoded = jwt.decode(admin_token, secret_key, algorithms='HS256')
    random_id = random.randrange(1000000, 99999999999)
    token = helper_tests.encode_JWT_token(token=token_decoded["token"], account_id=random_id)
    response, error = helper_tests.create_admin(JWT_token=token, account_id=1, account_type=3, testing="token")
    assert response == 400 and error == 16

def test_create_admin_wrong_token():
    response, admin_token, admin_mail, admin_password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= admin_token, answer= 1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail= admin_mail, password= admin_password, answer= 1)
    assert response == 200 and admin_token != ""
    token_decoded = jwt.decode(admin_token, secret_key, algorithms='HS256')
    random_token = random.randrange(1000000, 99999999999)
    token = helper_tests.encode_JWT_token(token=random_token, account_id=token_decoded["account_id"])
    response, error = helper_tests.create_admin(JWT_token=token, account_id=1, account_type=3, testing="token")
    assert response == 400 and error == 16

def test_create_admin_wrong_type_account():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and admin_token != ""
    response, error = helper_tests.create_admin(JWT_token=admin_token, account_id=1, account_type=3)
    assert response == 400 and error == 17

def test_authorize_admin_not_validated():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response, admin_token = helper_tests.log_in(mail= mail, password= password, answer= 1, testing="update_account")
    assert response == 200 and admin_token != ""
    response, error = helper_tests.create_admin(JWT_token=admin_token, account_id=1, account_type=3, testing="type_2")
    assert response == 400 and error == 17

def test_authorize_admin_not_authorized():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and admin_token != ""
    response, error = helper_tests.create_admin(JWT_token=admin_token, account_id=1, account_type=3, testing="type_2")
    assert response == 400 and error == 17

def test_create_admin_already_admin():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and admin_token != ""
    response = helper_tests.create_admin(JWT_token=admin_token, account_id=1, account_type=3, testing="type", answer=1)
    response, error = helper_tests.create_admin(JWT_token=admin_token, account_id=1, account_type=3, testing="type")
    assert response == 400, error == 15

def test_create_admin_account_not_validated():
    response, admin_token, admin_mail, admin_password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= admin_token, answer= 1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail= admin_mail, password= admin_password, answer= 1)
    assert response == 200 and admin_token != ""
    response, id, token = helper_tests.sign_up(testing="id", answer=5)
    assert response == 201 and id != None
    response, error = helper_tests.create_admin(JWT_token=admin_token, account_id=id, account_type=3)
    assert response == 400, error == 15

def test_create_admin_account_not_authorized():
    response, admin_token, admin_mail, admin_password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= admin_token, answer= 1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail= admin_mail, password= admin_password, answer= 1)
    assert response == 200 and admin_token != ""
    response, id, token = helper_tests.sign_up(testing="id", answer=5)
    assert response == 201 and id != None and token != None
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, error = helper_tests.create_admin(JWT_token=admin_token, account_id=id, account_type=3)
    assert response == 400, error == 15

def test_create_admin_ok():
    response, admin_token, admin_mail, admin_password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= admin_token, answer= 1)
    assert response == 200 
    response, admin_token = helper_tests.log_in(mail= admin_mail, password= admin_password, answer= 1)
    assert response == 200 and admin_token != ""
    response, id, token = helper_tests.sign_up(testing="id", answer=5)
    assert response == 201 and id != None
    response = helper_tests.create_admin(JWT_token=admin_token, testing="ok", account_id=id, account_type=3, answer=1)
    assert response == 200