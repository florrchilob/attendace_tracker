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
    print(sent)
    if "attendees" not in sent:
        return to_return(400, 101)
    attendees = sent.get("attendees")
    if type(attendees) != list or attendees == []:
        return to_return(400, 101)
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    invalid = []
    valid = []    
    for attendee in attendees:
        if not "mispar_ishi" in attendee and not "tehudat_zehut" in attendee:
            invalid.append({"attendee": attendee, "error": to_return(400, 4, testing="no_json")})
        elif "full_name" not in attendee:
            invalid.append({"attendee": attendee, "error": to_return(400, 4, testing="no_json")})
        else:
            validation = sends_validate(attendee, ["mispar_ishi", "name", "tehudat_zehut"])
            if validation != True:
                invalid.append(attendee)
            else:
                validAttende = Attendee()
                validAttende.create_straight(attendee)
                valid.append(validAttende)
    response = logic_create_attendee(valid, invalid, testing)
    if len(response) < 3:
        return to_return(response[0], response[1]) 
    else:
        return to_return(response[0], response[1], response[2]) 

#Logic behind the create function
def logic_create_attendee(validAttendees: list, invalid: List, testing):
    already_mispar_ishi = []
    already_tehudat_zehut = []
    added_mispar_ishi = []
    added_tehudat_zehut = []
    for this_attendee in validAttendees:
        validation = db_validating({"type": 1, "mispar_ishi": this_attendee.mispar_ishi, "tehudat_zehut": this_attendee.tehudat_zehut})
        if validation != True:
            if this_attendee.mispar_ishi:
                already_mispar_ishi.append(this_attendee.mispar_ishi)
            else:
                already_tehudat_zehut.append(this_attendee.tehudat_zehut)
        else:
            db_open_session()
            response_db = db_saving(this_attendee, attendees, testing)
            db_close_session() 
            if response_db == "error":
                return (500, 99)
            else:
                if this_attendee.mispar_ishi:
                    added_mispar_ishi.append(this_attendee.mispar_ishi)
                else:
                    added_tehudat_zehut.append(this_attendee.tehudat_zehut)
    returning = {
        "misssing_data": invalid,
        "already_database":{
            "mispar_ishi": already_mispar_ishi,
            "tehudat_zehut": already_tehudat_zehut
        },
        "successfull": {
            "mispar_ishi": added_mispar_ishi,
            "tehudat_zehut": added_tehudat_zehut
        }
    }
    if len(added_mispar_ishi) > 0 or len(added_tehudat_zehut) > 0:
        return (201, 0, returning)
    return (400, 101, returning)
