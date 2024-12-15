from testing import helper_tests
import string 
import random

def test_call_endpoint():
    response = helper_tests.test_call_endpoint()
    assert response == 200

def test_log_in_missing_mail():
    response, error = helper_tests.log_in(password= "123456789")
    assert response == 400 and error == 4
    
def test_log_in_missing_password():
    response, error = helper_tests.log_in(mail= "juan@perez.com.ar")
    assert response == 400 and error == 11
    
def test_log_in_mail_wrong_type():
    response, error = helper_tests.log_in(mail= 123, password= "123456789")
    assert response == 422 or (response == 400 and error == 4)
    
def test_log_in_password_wrong_type():
    response, error = helper_tests.log_in(mail= "juan@perez.com", password= 123456)
    assert response == 422 or (response == 400 and error == 11)
    
def test_log_in_wrong_mail():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  
    random_mail = ""
    for i in range(random.randrange(99)):
        random_mail = random_mail + random.choice(string.ascii_lowercase)
    random_mail = str("juanperez" + random_mail + "@gmail.com")
    response, error = helper_tests.log_in(mail= random_mail, password= password)
    assert response == 400 and error == 4

def test_log_in_wrong_password():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200  
    random_password = ""
    for i in range(random.randrange(99)):
        random_password = random_password + random.choice(string.ascii_letters)
    random_number = random.randint(1, 100)
    random_password = random_password + str(random_number)
    response, error = helper_tests.log_in(mail= mail, password= random_password)
    assert response == 400 and error == 4.2 
    
def test_log_in_non_validated_account():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response, error = helper_tests.log_in(mail= mail, password= password)
    assert response == 400 and error == 15.1

def test_log_in_ok():
    response, token, mail, password = helper_tests.sign_up(testing= True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response, token = helper_tests.log_in(mail= mail, password= password, answer= 1)
    assert response == 200 and token != ""
