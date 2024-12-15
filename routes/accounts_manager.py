#Imports
from fastapi import APIRouter, status, Request, Header
from datetime import datetime
from fastapi.responses import JSONResponse
import logging
from typing import List
from schemas.sub_account import SubAccount
from schemas.token import Token
from routes.helpers import to_return, sends_validate, send_mail, token_validating
from routes.db_helpers import db_validating, db_saving, db_getting, db_updating, db_close_session, db_open_session
from routes.accounts_manage_functions import token_generate, complete_account
from models.tables import sub_accounts
from dotenv import find_dotenv, load_dotenv
import pandas
import json
import jwt
import os


#Log manage
logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
loggerRouter = logging.getLogger(__name__)
loggerRouter.addHandler(file_handler)
loggerRouter.propagate = False

#Router
accounts_route = APIRouter(prefix = "/accounts", tags = ["account"], responses={status.HTTP_404_NOT_FOUND: {"Message" : "Not Found"}})
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

secret_key=os.getenv("secret_key")

@accounts_route.get("/")
def home():
    return to_return(200)

#borrar esta ruta
@accounts_route.get("/getall")
def get_all_probando():
    send = {"type": 1,
            "table": sub_accounts}
    response = db_getting(send)
    if response == "error":
        return to_return(400, 99)
    accounts_df = pandas.DataFrame(response, columns=["id", "mail", "password", "name", "mispar_ishi", "telephone", "account_type", "validated", "authorized", "token", "refresh_token", "token_expiration"])
    accounts_json = accounts_df.to_json(orient="records")
    return accounts_json

#Borrar esta ruta
@accounts_route.post("/probando")
def trying():
    payload = {
        "id": 123
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    token_decoded = jwt.decode(token, secret_key, algorithms='HS256')
    return "ok"

@accounts_route.get("/getprobando")
def get_all_probando():
    send = {"type": 2,
            "table": sub_accounts,
            "conditionals": {'mail' : 'florchilob0703@gmail.com'}, "values":["mail", "id", "account_type", "validated", "authorized"]}
    response = db_getting(send)
    return ""

#Route called to sign up a new account to the system
@accounts_route.post("/signup")
def sign_up(sent: dict):
    account = SubAccount()
    account.create_straight(sent)
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    validation = sends_validate(account, ["mail", "name", "password", "mispar_ishi", "telephone"])
    if validation == True:
        response = logic_sign_up(account, testing)
        if len(response) < 3:
            response = to_return(response[0], response[1]) 
        else:
            response = to_return(response[0], response[1], response[2]) 
        return response
    return to_return(validation[0], validation[1])

#Logic behind the sign up function
def logic_sign_up(account: SubAccount, testing):
    if testing != "update_account":
        validation = db_validating({"type" : 1, "mail": account.mail, "mispar_ishi": account.mispar_ishi})
        if validation == "error":
            return (500, 99)
        if validation == False:
            return (400, 14)
    token = token_generate()
    account_complete = complete_account(account, token)
    response_db = True
    db_open_session()
    if testing != "update_account":
        response_db = db_saving(account_complete, sub_accounts, testing)
    db_close_session()
    if response_db == "error":
        return (500, 99)
    if response_db == False:
        return (400, 99)
    response_mail = send_mail({"mail": account.mail, "name": account.name, "type": 1, "token": token.token})
    if response_mail == "error":
        return (500, 102)
    if response_mail == False:
        return (400, 4.1) 
    if testing == True:
        return (201, 0, token.token)
    if testing == "id":
        payload = {"token": token.token, "id": response_db}
        return (201, 0, payload)
    return (201, 0)

#Route called to resend the validation email to a account   
@accounts_route.post("/resendvalidation")
def resend_validation(sent: dict):
    account = SubAccount()
    account.create_straight(sent)
    testing = False
    if "testing" in sent:
        testing = sent.get("testing")
    validation = sends_validate(account, ["mail"])
    if validation == True:
        response = logic_resend_validation(account, testing)
        return to_return(response[0], response[1])
    return to_return(validation[0], validation[1])

#Logic behind the resend validation email function
def logic_resend_validation(account: SubAccount, testing: str):
    db_validation = db_validating({"type": 2, "conditionals" : {"mail": account.mail}})
    if testing == "validated":
        db_validation = "validated"
    if db_validation ==  "error":
        return (500, 99)
    if db_validation == False:
        return (400, 4)
    if db_validation == "validated":
        return (400, 15)
    token_validation = token_validating({"type" : 1, "token": db_validation.token, "refresh_token": db_validation.refresh_token, "expiration": db_validation.token_expiration})
    if testing == "token_missing":
        token_validation == "token"
    if token_validation == "token" or token_validation == "refresh_token" or token_validation == "token_expiration":
        token = token_generate()
        db_open_session()
        response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"mail" : account.mail}, "values" : {"token" : token.token, "refresh_token" : token.refresh_token, "token_expiration" : token.expiration}})
        db_close_session()
        if response == "error" or response == False:
            return(500, 99)
    else:
        token = Token (token=db_validation.token, refresh_token=db_validation.refresh_token, expiration=db_validation.token_expiration)
    name = db_validation.name
    response_mail = send_mail({"mail": account.mail, "type": 1, "name": name, "token": token.token})
    if response_mail == "error":
        return (500, 102)
    if response_mail == False:
        return (400, 4.1)
    return (200, 0)

#Route called to validate the account
@accounts_route.put("/validate/{sent}")
def account_validation(request: Request, sent: str, data: dict = None):
    token = Token(token=sent)
    testing = False
    if data != None:
        testing = data["testing"]
    if testing == "wrong_type":
        token.token = 123
    validation = sends_validate(token, ["token"])
    if validation == True:
        response = logic_account_validation(token, testing)
        return to_return(response[0], response[1])
    if validation == "token":
        return to_return(400, 16)
    return to_return(validation[0], validation[1])

#Logic behind the validation of an account
def logic_account_validation(token: str, testing: str):
    db_validation = db_validating({"type": 2, "conditionals" : {"token": token.token}})
    if testing == "validated":
        db_validation = "validated"
    if db_validation ==  "error":
        return (500, 99)
    if db_validation == False:
        return (400, 16)
    if db_validation == "validated":
        return (400, 15)
    account = db_validation    
    token_validation = token_validating({"type": 1, "token" : account.token, "refresh_token" : account.refresh_token, "token_expiration" : account.token_expiration})
    if  testing == "wrong_refresh_token":
        token_validation = "refresh_token"
    if testing == "expirated":
        token_validation = "token_expiration"
    if testing == "wrong_expiration":
        token_validation = "token_expiration"
    db_open_session()
    if token_validation == "token" or token_validation == "refresh_token" or token_validation == "token_expiration":
        new_token = token_generate()
        db_updating({"type": 1, "table": sub_accounts, "conditionals": {"name": account.name, "mail": account.mail}, "values": {"token": new_token.token, "refresh_token": new_token.refresh_token, "token_expiration": new_token.expiration}})
        send_mail({"type": 1, "name": account.name, "mail": account.mail, "token": new_token.token})
        return (400, 15.1)
    response = db_updating({"type": 1, "table": sub_accounts, "conditionals" : {"token": token.token}, "values" : {"validated" : True}})
    db_close_session()
    if response == "error":
        return (500, 102)
    if response == False:
        return (500, 99)
    return (200, 0)

#Route called to do the log in of a account
@accounts_route.post("/login")
def log_in(sent: dict):
    account = SubAccount()
    account.create_straight(sent)
    testing = False
    if "testing" in sent:
        testing = sent.get("testing")
    validation = sends_validate(account, ["mail", "password"])
    if validation == True:
        response = logic_log_in(account, testing)
        if len(response) < 3:
            return to_return(status_code= response[0], error= response[1])
        return to_return(status_code= response[0], error= response[1], data= response[2])
    return to_return(validation[0], validation[1])

#Logic behind the log in of a account
def logic_log_in(account: SubAccount, testing):
    db_validation = db_validating({"type": 3, "conditionals": {"mail": account.mail}})
    if db_validation == "error":
        return(500, 99)
    if db_validation == False:
        return (400, 4  )
    db_validation = db_validating({"type": 3, "conditionals": {"mail": account.mail, "password": account.password}})
    if db_validation == "error":
        return(500, 99)
    if db_validation == False:
        return (400, 4.2)
    if db_validation.validated == False and testing != "update_account":
        db_validation_mail = logic_resend_validation(SubAccount(mail=db_validation.mail), False)
        if db_validation_mail[0] != 200:
            return (db_validation_mail.status_code, db_validation_mail.content.get("error"))         
        else:
            return(400, 15.1)
    token = token_generate()
    db_open_session()
    response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id": db_validation.id}, "values": {"token": token.token, "refresh_token": token.refresh_token, "token_expiration": token.expiration}})
    db_close_session()
    if response == False or response == "error":
        return (500, 99)
    payload_token = {
        "token" : token.token,
        "refresh_token" : token.refresh_token,
        "account_id": db_validation.id,
        "name": db_validation.name,
        "account_type": db_validation.account_type
    } 
    jwt_token = jwt.encode(payload_token, secret_key, algorithm='HS256')
    payload_to_send = {
        "token" : jwt_token
    }
    return (200, 0, payload_to_send)
    
#Route called to log out a account
@accounts_route.post("/logout")
def log_out(JWToken: str = Header(...)):
    JWT_token = JWToken
    if JWT_token == None:
        return to_return(400, 16)
    validation = sends_validate({"JWT_token": JWT_token}, ["JWT_token"])
    if type(validation) != tuple:
        data = validation
        validation = sends_validate(validation, ["token", "account_id"])
        response = validation
        if type(validation) != tuple:
            response = logic_log_out(data)
        return to_return(response[0], response[1])
    if validation[1] == 400 and validation[2] == 18:
        validation = (400, 16)
    return to_return(validation[0], validation[1])

#Logic behind the log off of a account
def logic_log_out(jwt_token):
    response = token_validating({"type": 2, "token": jwt_token.get("token"), "id": jwt_token.get("account_id")})
    if response == "no_needed":
        return (400, 15)
    if response == False or response == "token":
        return (400, 16)
    if response == "error":
        return (500, 99)
    db_open_session()
    response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id": response.get("id")}, "values": {"token": None, "refresh_token": None, "token_expiration": None}})
    db_close_session()
    if response == False or response == "error":
        return (500, 99)
    return (200, 0)

#Route called to send an email to change the password
@accounts_route.post("/forgotpassword")
def forgot_password(sent: dict):
    account = SubAccount()
    account.create_straight(sent)
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    validation = sends_validate(account, ["mail"])
    if validation == True:
        response = logic_forgot_password(account, testing)
        if len(response) < 3:
            return to_return(response[0], response[1])
        return to_return(response[0], response[1], response[2])
    return to_return(validation[0], validation[1])

def logic_forgot_password(account: SubAccount, testing):
    validated, no_validated = db_validating({"type": 5, "conditionals": {"mail": account.mail}})
    if validated == "error" or no_validated == "error":
        return (500, 99)
    if validated == False or no_validated == False:
        return (400, 4)
    if validated == []:
        mail_name = db_getting({"type": 2, "table": sub_accounts, "values": ["mail", "name"], "conditionals": {"id": no_validated[0]}})
        mail_name = {"mail": mail_name[0][0], "name": mail_name[0][1]}
        account = SubAccount()
        account.create_straight(mail_name)
        response = logic_resend_validation(account, False)
        if response[0] != 200:
            return response
        return (400, 15.1)
    account = validated[0]
    new_token = token_generate()
    db_open_session()
    response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"mail": account.mail}, "values": {"token": new_token.token, "refresh_token": new_token.refresh_token, "token_expiration": new_token.expiration}})
    db_close_session()
    if response == False or response == "error":
        return (500, 99)
    response_mail = send_mail({"type": 2, "name": account.name, "mail": account.mail, "token": new_token.token})
    if response_mail == "error":
        return (500, 102)
    if response_mail == False:
        return (400, 4.1)
    if testing == True:
        return (200, 0, new_token.token)
    return (200, 0)

@accounts_route.put("/newpassword/{sent}")
def new_password(sent: str, data: dict):
    token = Token(token=sent)
    account = SubAccount()
    account.create_straight(data)
    testing = False
    if "testing" in data:
        testing = data["testing"]
    if testing == "wrong_type":
        token.token = 123
    validation = sends_validate(token, ["token"])
    if validation == True:
        validation = sends_validate(account, ["password", "mispar_ishi"])
        if validation == True:
            response = logic_new_password(token, account, testing)
            return to_return(response[0], response[1])
        return to_return(validation[0], validation[1])
    if validation == "token":
        return to_return(400, 16)
    return to_return(validation[0], validation[1])

def logic_new_password(token: Token, account: SubAccount, testing: str):
    db_validation = db_validating({"type": 3, "conditionals": {"mispar_ishi": account.mispar_ishi}})
    if db_validation == "error":
        return(500, 99)
    if db_validation == False:
        return(400, 3)
    token_validation = token_validating({"type": 2, "token": token.token, "refresh_token": db_validation.refresh_token, "token_expiration": db_validation.token_expiration, "id": db_validation.id})
    if testing == "expirated":
        token_validation = "token_expiration"
    if token_validation == "token" or token_validation == "refresh_token" or token_validation == "no_needed" or token_validation == False:
        return(400, 16)
    if token_validation == "token_expiration":
        token = token_generate()
        response_mail = send_mail({"mail": db_validation.mail, "type": 1, "name": db_validation.name, "token": token.token})
        if response_mail == "error":
            return (500, 102)
        if response_mail == False:
            return (400, 4.1)
        return (400, 15.1)
    db_open_session()
    response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id": db_validation.id, "mispar_ishi": account.mispar_ishi}, "values": {"password": account.password}})
    db_close_session()
    if response == False or response == "error":
        return (500, 99)
    return (200, 0)

@accounts_route.put("/updateaccount")
def update_account(sent: dict, JWToken : str = Header(...)):
    testing = False
    if "account_id" in sent or "id" in sent or "mispar_ishi" in sent or "account_type" in sent or "token" in sent or "validated" in sent or "authorized" in sent or "refresh_token" in sent or "token_expiration" in sent:
        return to_return(400, 101)
    if "testing" in sent:
        testing = sent["testing"]
    if JWToken == None:
        return to_return(400, 16)
    JWT_token = JWToken
    validation = sends_validate({"JWT_token": JWT_token}, ["JWT_token"])
    if type(validation) != tuple:
        token_sent = validation
        if "account_id" not in token_sent:
            validation = (400, 16)
        else:
            to_validate = list(token_sent.keys())
            validation = sends_validate(token_sent, to_validate)
        if (validation == "token" or "token" not in token_sent) and testing != "type":
            validation = (400, 16)
        if validation == True:
            to_validate = list(sent.keys())
            account = SubAccount()
            merged_account = sent | {"id": token_sent.get("account_id")}
            account.create_straight(merged_account)
            validation = sends_validate(account, to_validate)
            if validation == True:
                old_password = None
                if "old_password" in sent:
                    validation = sends_validate({"password": sent["old_password"]}, ["password"])
                    if validation == True:
                        old_password = sent["old_password"]
                response = logic_update_account(token_sent, account, testing, old_password)
                if len(response) == 2:
                    return to_return(response[0], response[1])
                else:
                    return to_return(response[0], response[1], response[2])
    return to_return(validation[0], validation[1])
    
def logic_update_account(token_sent: dict, account_to_change: SubAccount, testing, old_password: str):
    id = account_to_change.id
    old_token = token_sent.get("token")
    old_refresh_token = token_sent.get("refresh_token")
    token_validation = token_validating({"type": 2, "token": old_token, 
                                         "id": id,  "refresh_token": old_refresh_token})
    if token_validation == False or token_validation == "token"or token_validation == "wrong_token":
        return (400, 16)
    if token_validation == "error":
        return (500, 99)
    if token_validation == "no_needed":
        return (400, 15)
    token_renovated = ""
    if token_validation == "renovate_token":
        token_renovated = token_generate()
        response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id": id}, "values": 
                                {"token": token_renovated.token, "refresh_token": token_renovated.refresh_token, "token_expiration": token_renovated.expiration}})
        if response == False or response == "error":
                return (500, 9)
    db_validation = db_validating({"type": 6, "conditionals": {"id": id}})
    if db_validation == "error" or db_validation == False:
        return (500, 99)
    if db_validation == "validated":
        account = db_getting({"type": 2, "table": sub_accounts, "values": ["mail"], "conditionals": {"id": id}})
        account = account[0][0]
        db_validation_mail = logic_resend_validation(SubAccount(mail=account), False)
        if db_validation_mail[0] != 200:
            return (db_validation_mail.status_code, db_validation_mail.content.get("error"))         
        else:
            return(400, 15.1)
    if db_validation == "authorized" and testing != "old_password" and testing != "repeated_mail" and testing != "mail" and testing != "ok":
        return (400, 17)
    if account_to_change.mail != None:
        db_validation = db_validating({"type": 1, "mail": account_to_change.mail, "mispar_ishi": "123"})
        if db_validation != True:
            return (400, 4)
    if old_password != None:
        password_validation = db_validating({"type": 3, "conditionals": {"id": id, "password": old_password}})
        if password_validation == False or password_validation == "":
            return (400, 4.2)
    list_update = {key:value for key, value in account_to_change if value is not None} 
    db_open_session()
    response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id": id}, "values": list_update})
    db_close_session()
    if response == False or response == "error":
        return (500, 9)
    if account_to_change.mail != None:
        response = logic_sign_up(account_to_change, "update_account")
        if response[0] == 201:
            return (400, 15.1)
        return response
    if token_renovated != "":
        payload_token = {
            "token" : token_renovated.token,
            "refresh_token" : token_renovated.refresh_token,
            "account_id" : id
        } 
        jwt_token = jwt.encode(payload_token, secret_key, algorithm='HS256')
        return (200, 0, jwt_token)
    else:
        return (200, 0)

@accounts_route.get("/getaccountsauthorize")
def get_accounts_authorize(JWToken: str = Header(...), sent: dict = {}, init: int = Header(None)):
    if JWToken == None:
        return to_return(400, 16)
    JWT_token = JWToken
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    validation = sends_validate({"JWT_token": JWT_token}, ["JWT_token"])
    if type(validation) != tuple:
        token_sent = validation
        if "token" not in token_sent or "account_id" not in token_sent:
            return to_return(400, 16)
        to_validate = list(token_sent.keys())
        validation = sends_validate(token_sent, to_validate)
        if validation == "token":
            return to_return (400, 16)
        if validation == True:
            if init == None:
                init = 0
            response = logic_get_accounts_authorize(token_sent, testing, init)
            if len(response) < 3:
                return to_return(response[0], response[1])
            return to_return(response[0], response[1], response[2])                
    return to_return(validation[0], validation[1])

def logic_get_accounts_authorize(token_sent: dict, testing, init: int):
    id_admin = token_sent.get("account_id")
    if testing != "token" and testing != "type":
        db_validation = db_validating({"type": 6, "type_needed": 2, "conditionals": {"id": id_admin}})
        if db_validation == False or db_validating == "error":
            return (500, 99)
        if db_validation == "validated" or db_validation == "authorized" or db_validation == "wrong_type":
            return (400, 17)
    token_validation = token_validating({"type": 2, "token": token_sent.get("token"), "id":id_admin})
    if token_validation == False or token_validation == "token":
        return (400, 16)
    if token_validation == "error":
        return (500, 99)
    if token_validation == "token" or token_validation == "refresh_token" or token_validation == "token_expiration":
        token = token_generate()
        db_open_session()
        response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id" : id_admin}, "values" : {"token_expiration" : token.expiration}})
        db_close_session()
        if response == "error" or response == False:
            return(500, 99)
    accounts_authorize = db_getting({"type": 2, "table": sub_accounts, "values": ["id", "mail", "name", "mispar_ishi", "telephone"], "conditionals": {"authorized": False, "validated": True}})
    if accounts_authorize == False or accounts_authorize == "error":
        return (500,9)
    accounts_return = accounts_authorize[init:init+30]
    accounts_df = pandas.DataFrame(accounts_return, columns=["account_id", "mail", "name", "mispar_ishi", "telephone"])
    accounts_json = accounts_df.to_json(orient="records")
    json_return = {"amount" : len(accounts_authorize),"accounts" : accounts_json}
    return (200, 0, json_return)

@accounts_route.get("/getmyaccount")
def get_my_account(JWToken: str = Header(...), sent: dict = {}):
    if JWToken == None:
        return to_return(400, 16)
    JWT_token = JWToken
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    validation = sends_validate({"JWT_token": JWT_token}, ["JWT_token"])
    if type(validation) != tuple:
        token_sent = validation
        if "token" not in token_sent or "account_id" not in token_sent:
            return to_return(400, 16)
        to_validate = list(token_sent.keys())
        validation = sends_validate(token_sent, to_validate)
        if validation == "token":
            return to_return (400, 16)
        if validation == True:
            response = logic_get_my_account(token_sent, testing)
            if len(response) < 3:
                return to_return(response[0], response[1])
            return to_return(response[0], response[1], response[2])                
    return to_return(validation[0], validation[1])

def logic_get_my_account(token_sent: dict, testing):
    account_id = token_sent.get("account_id")
    token = token_sent.get("token")
    refresh_token = token_sent.get("refresh_token")
    token_validation = token_validating({"type": 2, "token": token, "refresh_token": refresh_token, "id": account_id})
    if token_validation == False or token_validation == "token" or token_validation == "refresh_token":
        return (400, 16)
    if token_validation == "error":
        return (500, 99)
    my_account = db_getting({"type": 2, "table": sub_accounts, "values": ["id", "name", "mispar_ishi", "mail", "telephone"], "conditionals": {"token": token}})
    token_renovated = ""
    if token_validation == "token" or token_validation == "refresh_token" or token_validation == "token_expiration" or token_validation == "renovate_token":
        id_account = my_account[0][0]
        token_renovated = token_generate()
        db_open_session()
        response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id" : id_account}, 
                                "values" : {"token": token_renovated.token, "refresh_token": token_renovated.refresh_token, "token_expiration" : token_renovated.expiration}})
        db_close_session()
        if response == "error" or response == False:
            return(500, 99)
    if my_account == False:
        return (400, 16)
    if my_account == "error":
        return (500,9)
    my_account = my_account[0]
    account_json = {"name": my_account.name, "mispar_ishi": my_account.mispar_ishi, "mail": my_account.mail, "telephone": my_account.telephone}
    if token_renovated != "":   
        payload = {
            "token" : token_renovated.token,
            "refresh_token" : token_renovated.refresh_token,
            "account_id": my_account.id
        }  
        token_encoded = jwt.encode(payload, secret_key, algorithm='HS256')
        payload_json = {
            "account": account_json,
            "token": token_encoded,
        }
        return(200, 0, payload_json)
    return (200, 0, account_json)

@accounts_route.put("/authorizeaccounts")
def authorize_accounts(sent: dict, JWToken: str = Header(...)):
    if JWToken == None:
        return to_return(400, 16)
    JWT_token = JWToken
    if "accounts" not in sent:
        return to_return(400, 18)
    accounts_id = sent["accounts"]
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    data = {"invalidIds": None, "authorizedIds": None}
    incorrectIds=[]
    correctIds=[]
    validation = sends_validate({"JWT_token": JWT_token}, ["JWT_token"])
    if type(validation) != tuple:
        token_sent = validation
        if "token" not in token_sent or "account_id" not in token_sent:
            return to_return(400, 16)
        validation = sends_validate(token_sent, ["account_id", "token"])
        if validation == "token":
            return to_return (400, 16)
        if validation == True:
            for currentId in accounts_id:
                validation = sends_validate({"account_id": currentId}, ["account_id"])
                if validation != True:
                    incorrectIds.append(currentId)
                else:
                    correctIds.append(currentId)
            data["invalidIds"] = incorrectIds
            if len(correctIds) > 0:
                response = logic_authorize_accounts(token_sent, correctIds, incorrectIds, testing)
                return to_return(response[0], 0, response[1])
            else:
                return to_return(validation[0], validation[1], data)
    return to_return(validation[0], validation[1])

def logic_authorize_accounts(token_sent: dict, ids_to_auth: int, incorrectIds, testing):
    id_admin = token_sent.get("account_id")
    if testing != "token" and testing != "type" and testing != "ok":
        db_validation = db_validating({"type": 6, "type_needed": 2, "conditionals": {"id": id_admin}})
        if db_validating == "error":
            return (500, 99)
        if db_validation == "validated" or db_validation == "authorized" or db_validation == "wrong_type" or db_validation == False:
            return (400, 17)
    token_validation = token_validating({"type": 2, "token": token_sent.get("token"), "id":id_admin})
    if token_validation == False or token_validation == "token":
        return (400, 16)
    if token_validation == "error":
        return (500, 99)
    if token_validation == "token" or token_validation == "refresh_token" or token_validation == "token_expiration":
        token = token_generate()
        db_open_session()
        response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id" : id_admin}, "values" : {"token_expiration" : token.expiration}})
        db_close_session()
        if response == "error" or response == False:
            return(500, 99)
    db_validation = db_validating({"type": 5, "conditionals": {"id": ids_to_auth}})
    if type(db_validation) == tuple:
        accounts_returned, validated_accounts = db_validation
        ids_success = [persona.id for persona in accounts_returned]
        failed_accounts = list(set(ids_to_auth) - set(ids_success) - set(validated_accounts))
        incorrectIds.extend(failed_accounts)
    if db_validation == "error":
        return (500, 9)
    if db_validation == False:
        return (400, 18)
    if db_validation == "validated":
        return(400, 17.1)
    db_open_session()
    response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id": ids_to_auth}, "values": {"authorized": True, "account_type": 1}})
    db_close_session()
    if response == "error" or response == False:
        return (500, 99)
    errorMail = []
    authorized_ids = []
    for account in accounts_returned:
        response_mail = send_mail({"type": 3, "name": account.name, "mail": account.mail, "name": account.name})
        if response_mail == "error" or response_mail == False:
            errorMail.append(account.id)
        else:
            authorized_ids.append(account.id)
    data = {"authorized_ids" : authorized_ids, "invalidIds" : incorrectIds, "notValidatedAccounts" : validated_accounts, "errorMail" : errorMail}
    return (200, data)

@accounts_route.get("/getallaccounts")
def get_all_accounts(variable: str, value: str, sent: dict = {}, JWToken: str = Header(...)):
    if JWToken == None:
        return to_return(400, 16)
    JWT_token = JWToken
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    if variable == None or value == None :
        return to_return(400, 103)
    validation = sends_validate({"JWT_token": JWT_token}, ["JWT_token"])
    if type(validation) != tuple:
        token_sent = validation
        if "token" not in token_sent or "account_id" not in token_sent:
            return to_return(400, 16)
        to_validate = list(token_sent.keys())
        validation = sends_validate(token_sent, to_validate)
        if validation == "token":
            return to_return (400, 16)
        if validation == True:
            validation = sends_validate({"variable":variable}, ["variable"])
            if validation == True:
                validation = sends_validate({"value":value}, ["value"])
                if validation == True:
                    response = logic_get_all_accounts(token_sent, variable, value, testing)
                    if len(response) < 3:
                        return to_return(response[0], response[1])
                    return to_return(response[0], response[1], response[2])                
    return to_return(validation[0], validation[1])

def logic_get_all_accounts(token_sent: dict, variable: str, value: str, testing):
    id_admin = token_sent.get("account_id")
    if testing != "token" and testing != "type":
        db_validation = db_validating({"type": 6, "type_needed": 3, "conditionals": {"id": id_admin}})
        if db_validation == False or db_validating == "error":
            return (500, 99)
        if db_validation == "validated" or db_validation == "authorized" or db_validation == "wrong_type":
            return (400, 17)
    token_validation = token_validating({"type": 2, "token": token_sent.get("token"), "id":id_admin})
    if token_validation == False or token_validation == "token":
        return (400, 16)
    if token_validation == "error":
        return (500, 99)
    if token_validation == "token" or token_validation == "refresh_token" or token_validation == "token_expiration":
        token = token_generate()
        db_open_session()
        response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id" : id_admin}, "values" : {"token_expiration" : token.expiration}})
        db_close_session()
        if response == "error" or response == False:
            return(500, 99)
    all_accounts = db_getting({"type": 3, "table": sub_accounts, "values": ["name", "mail", "mispar_ishi", "validated", "account_type", "telephone"], "conditionals": [{variable: value}]})
    if all_accounts == "error":
        return (400, 9)
    if all_accounts == False:
        return (400  , 104)
    accounts_df = pandas.DataFrame(all_accounts, columns=["name", "mail", "mispar_ishi", "validated", "account_type", "telephone"])
    accounts_json = accounts_df.to_json(orient="records")
    return (200, 0, accounts_json)

@accounts_route.post("/createadmin")
def create_admin(sent: dict, JWToken: str = Header(...)):
    if JWToken == None:
        return to_return(400, 16)
    JWT_token = JWToken
    if "account_id" not in sent:
        return to_return(400, 18)
    if "account_type" not in sent:
        return to_return(400, 19)
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    validation = sends_validate({"JWT_token": JWT_token}, ["JWT_token"])
    if type(validation) != tuple:
        token_sent = validation
        if "token" not in token_sent or "account_id" not in token_sent:
            return to_return(400, 16)
        to_validate = list(token_sent.keys())
        validation = sends_validate(token_sent, to_validate)
        if validation == "token":
            return to_return (400, 16)
        if validation == True:
            id_to_auth = sent["account_id"]
            validation = sends_validate({"account_id": id_to_auth}, ["account_id"])
            if validation == True:
                account_type = sent["account_type"]
                validation = sends_validate({"account_type": account_type}, ["account_type"])
                if validation == True:
                    response = logic_create_admin(token_sent, id_to_auth, account_type, testing)
                    return to_return(response[0], response[1])
    return to_return(validation[0], validation[1])

def logic_create_admin(token_sent: dict, id_to_auth: int, account_type: int, testing):
    id_admin = token_sent.get("account_id")
    if testing != "token" and testing != "type" and testing != "ok":
        db_validation = db_validating({"type": 6, "type_needed": 3, "conditionals": {"id": id_admin}})
        if testing != "type_2":
            if db_validation == False or db_validating == "error":
                return (500, 9)
        if db_validation == "validated" or db_validation == "authorized" or db_validation == "wrong_type":
            return (400, 17)
    token_validation = token_validating({"type": 2, "token": token_sent.get("token"), "id":id_admin})
    if token_validation == False or token_validation == "token":
        return (400, 16)
    if token_validation == "error":
        return (500, 99)
    if token_validation == "token" or token_validation == "refresh_token" or token_validation == "token_expiration":
        token = token_generate()
        db_open_session()
        response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id" : id_admin}, "values" : {"token_expiration" : token.expiration}})
        db_close_session()
        if response == "error" or response == False:
            return(500, 99)
    if testing == "ok":
        db_validation = db_validating({"type": 5, "conditionals": {"id": id_to_auth}}, testing)
    else:
        db_validation = db_validating({"type": 5, "conditionals": {"id": id_to_auth, "validated": True, "authorized": True}})
    if db_validation == "error":
        return (500, 9)
    if db_validation == False:
        return (400, 18)
    if db_validation == "validated" and testing != "ok":
        return(400, 17)
    if db_validation.account_type == account_type:
        return (400, 15)
    if account_type < 2:
        return (400, 19)
    db_open_session()
    response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"id": id_to_auth}, "values": {"account_type": account_type}})
    db_close_session()
    if response == "error" or response == False:
        return (500, 99)
    return (200, 0)