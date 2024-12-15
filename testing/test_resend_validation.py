from testing import helper_tests
import string
import random

def test_call_endpoint():
    response = helper_tests.test_call_endpoint()
    assert response == 200

def test_resend_validation_missing_mail():
    response, error = helper_tests.resend_validation()
    assert response == 400 and error == 4

def test_resend_validation_mail_wrong_type():
    response, error = helper_tests.resend_validation(mail= 123)
    assert response == 422 or error == 4

def test_resend_validation_mail_wrong_type_at():
    response, error = helper_tests.resend_validation(mail= "juanperez.com")
    assert response == 400 and error == 4

def test_resend_validation_mail_wrong_type_at_2():
    response, error = helper_tests.resend_validation(mail= "juan@@@perez.com")
    assert response == 400 and error == 4

def test_resend_validation_mail_inexistent():
    random_mail = ""
    random_domain = ""
    for i in range(random.randrange(99)):
        random_mail = random_mail + random.choice(string.ascii_lowercase)
        random_domain = random_domain + random.choice(string.ascii_lowercase)
    random_mail = "juanperez" + random_mail + random_domain
    response, error = helper_tests.resend_validation(mail= random_mail)
    assert response == 400 and error == 4

def test_resend_validation_account_validated():
    response, mail = helper_tests.sign_up(answer= 1)
    assert response == 201
    response, error = helper_tests.resend_validation(mail= mail, testing= "validated")
    assert response == 400 and error == 15

def test_resend_validation_ok():
    response, mail = helper_tests.sign_up(answer= 1)
    assert response == 201
    response= helper_tests.resend_validation(mail= mail, answer=1)
    assert response == 200