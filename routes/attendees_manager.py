#Imports
from fastapi import APIRouter, status, Request, Header
from datetime import datetime
from fastapi.responses import JSONResponse
import logging
from typing import List
from schemas.attendee import Attendee
from routes.helpers import to_return, sends_validate, send_mail, token_validating
from routes.db_helpers import db_validating, db_saving, db_getting, db_updating, db_close_session, db_open_session
from models.tables import attendees
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
attendees_route = APIRouter(prefix = "/attendees", tags = ["attendees"], responses={status.HTTP_404_NOT_FOUND: {"Message" : "Not Found"}})
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

secret_key=os.getenv("secret_key")

@attendees_route.get("/")
def home():
    return to_return(200)

#Route called to sign up a new account to the system
@attendees_route.post("/create")
def createattendees(sent: dict):
    print(len(sent.get("attendees")))
    if "attendees" not in sent:
        return to_return(400, 101)
    attendees = sent.get("attendees")
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    for attendee in attendees:
        if not "mispar_ishi" in attendee and not "tehudat_zehut" in attendee:
            return to_return(400, 3)
        if "full_name" not in attendee:
            return to_return(400, 1)
        attendee = Attendee()
        attendee.create_straight(sent)
        validation = sends_validate(attendee, ["mispar_ishi", "name"])
    if validation == True:
        response = logic_create_attendee(attendee, testing)
        if len(response) < 3:
            response = to_return(response[0], response[1]) 
        else:
            response = to_return(response[0], response[1], response[2]) 
        return response
    return to_return(validation[0], validation[1])

#Logic behind the create function
def logic_create_attendee(attendee: Attendee, testing):
    validation = db_validating({"type": 1, "mispar_ishi": attendee.mispar_ishi})
    
    print(validation)
    return(200,0)
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
