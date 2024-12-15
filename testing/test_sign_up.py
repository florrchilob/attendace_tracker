import string
import random
from testing import helper_tests

def test_call_endpoint():
    response = helper_tests.test_call_endpoint()
    assert response == 200

def test_sign_up_mail_wrong_type():
    response, error = helper_tests.sign_up(mail= 123)
    assert response == 422  or (response == 400 and error == 4)

def test_sign_up_mail_hebrew():
    response, error = helper_tests.sign_up(mail= "juan@פרז.com")
    assert response == 422  or (response == 400 and error == 4) 

def test_sign_up_mail_signs():
    response, error = helper_tests.sign_up(mail= "juan@$%#perez.com")
    assert response == 422  or (response == 400 and error == 4) 

def test_sign_up_mail_space():
    response, error = helper_tests.sign_up(mail= "juan@ perez.com")
    assert response == 422  or (response == 400 and error == 4) 

def test_sign_up_mail_long():
    response, error = helper_tests.sign_up(mail= "abcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxy@example.com")
    assert response == 422  or (response == 400 and error == 4) 

def test_sign_up_mail_wrong_type_at():
    response, error = helper_tests.sign_up(mail= "juanperez.com")
    assert response == 400 and error == 4

def test_sign_up_mail_wrong_type_at_2():
    response, error = helper_tests.sign_up(mail= "juan@@@@perez.com")
    assert response == 400 and error == 4


def test_sign_up_missing_password():
    response, error = helper_tests.sign_up(password= False)
    assert response == 400 and error == 11

def test_sign_up_password_wrong_type():
    response, error = helper_tests.sign_up(password= 123456)
    assert response == 422  or (response== 400 and error == 11)

def test_sign_up_password_missing_upper_case():
    response, error = helper_tests.sign_up(password= "abc123")
    assert response == 422  or (response== 400 and error == 11)

def test_sign_up_password_missing_lower_case():
    response, error = helper_tests.sign_up(password= "ABC123")
    assert response == 422  or (response== 400 and error == 11)

def test_sign_up_password_missing_numbers():
    response, error = helper_tests.sign_up(password= "ABCabc")
    assert response == 422  or (response== 400 and error == 11)

def test_sign_up_password_hebrew():
    response, error = helper_tests.sign_up(password= "abcשדגASD123")
    assert response == 422  or (response== 400 and error == 11)

def test_sign_up_password_space():
    response, error = helper_tests.sign_up(password= "abc ABC 123")
    assert response == 422  or (response== 400 and error == 11)

def test_sign_up_password_long():
    response, error = helper_tests.sign_up(password= "abcdefghijklmnopsfsdfsqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyasdertyuiolkjhg")
    assert response == 422  or (response == 400 and error == 11)

def test_sign_up_missing_name():
    response, error = helper_tests.sign_up(name = False)
    assert response == 400 and error == 1

def test_sign_up_name_wrong_type():
    response, error = helper_tests.sign_up(name= "Juan @ Perez")
    assert response == 422  or (response== 400 and error == 1)

def test_sign_up_name_signs():
    response, error = helper_tests.sign_up(name= 123)
    assert response == 422  or (response== 400 and error == 1)

def test_sign_up_name_long():
    response, error = helper_tests.sign_up(name= "abcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxy asdertyuiolkjhg")
    assert response == 422  or (response == 400 and error == 1) 

def test_sign_up_not_full_name():
    response, error = helper_tests.sign_up(name= "JuanPerez")
    assert response == 400 and error == 2

def test_sign_up_hebrew_english_name():
    response, error = helper_tests.sign_up(name= "Juan פרז")
    assert response == 400 and error == 1

def test_sign_up_missing_mispar_ishi():
    response, error = helper_tests.sign_up(mispar_ishi= False)
    assert response == 400 and error == 3

def test_sign_up_mispar_ishi_wrong_type():
    response, error = helper_tests.sign_up(mispar_ishi= "abc")
    assert response == 422  or (response== 400 and error == 3)

def test_sign_up_missing_telephone():
    response, error = helper_tests.sign_up(telephone= False)
    assert response == 400 and error == 12

def test_sign_up_telephone_wrong_type():
    response, error = helper_tests.sign_up(telephone= "123456789")
    assert response == 422  or (response== 400 and error == 13)

def test_sign_up_repeated_mail():
    random_mail = ""
    for i in range(random.randrange(99)):
        random_mail = random_mail + random.choice(string.ascii_lowercase)
    random_mail = "juanperez" + random_mail + "@gmail.com"
    helper_tests.sign_up(mail= random_mail, answer= 1)
    response, error = helper_tests.sign_up(mail= random_mail)
    assert response == 400 and error == 14

def test_sign_up_repeated_mispar_ishi():
    random_mispar_ishi = random.randrange(1000000, 99999999999)
    helper_tests.sign_up(mispar_ishi= random_mispar_ishi, answer= 1)
    response, error = helper_tests.sign_up(mispar_ishi= random_mispar_ishi)
    assert response == 400 and error == 14
    
def test_sign_up_ok_english():
    response = helper_tests.sign_up(name="Juan Perez", answer=0)
    assert response == 201

def test_sign_up_ok_hebrew():
    response = helper_tests.sign_up(name="חואן פרז", answer=0)
    assert response == 201