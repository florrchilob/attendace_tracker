from testing import helper_tests
import string
import random

def test_call_endpoint():
    response = helper_tests.test_call_endpoint()
    assert response == 200

def test_forgot_password_missing_mail():
    response, data = helper_tests.forgot_password(payload= {})
    assert response == 400 and data == 4

def test_forgot_password_mail_wrong_type():
    response, data = helper_tests.forgot_password(mail= 123)
    assert response == 422 or data == 4

def test_forgot_password_mail_wrong_type_at():
    response, data = helper_tests.forgot_password(mail= "juanperez.com")
    assert response == 400 and data == 4

def test_forgot_password_mail_wrong_type_at_2():
    response, data = helper_tests.forgot_password(mail= "juan@@@@perez.com")
    assert response == 400 and data == 4

def test_forgot_password_mail_inexistent():
    random_mail = ""
    random_domain = ""
    for i in range(random.randrange(99)):
        random_mail = random_mail + random.choice(string.ascii_lowercase)
        random_domain = random_domain + random.choice(string.ascii_lowercase)
    random_mail = random_mail +  "@" + random_domain
    response, data = helper_tests.forgot_password(mail= random_mail)
    assert response == 400 and data == 4

def test_forgot_password_account_not_validated():
    response, mail = helper_tests.sign_up(answer= 1)
    assert response == 201
    response, data = helper_tests.forgot_password(mail= mail)
    assert response == 400 and data == 15.1

def test_forgot_password_ok():
    response, token, mail, password = helper_tests.sign_up(testing = True, answer= 3)
    assert response == 201
    response = helper_tests.validate_account(token= token, answer= 1)
    assert response == 200 
    response = helper_tests.forgot_password(mail= mail, answer= 1)
    assert response == 200

