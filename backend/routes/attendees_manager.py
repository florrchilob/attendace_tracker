#Imports
from fastapi import APIRouter, status
import logging
from typing import List
from schemas.attendee import Attendee
from routes.helpers import to_return, sends_validate
from routes.db_helpers import db_validating, db_saving, db_getting, db_updating, db_close_session, db_open_session, db_deleting
from models.tables import attendees
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
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
            invalid.append({"attendee": attendee, "error": to_return(400, 102, testing="no_json")})
        elif "full_name" not in attendee:
            invalid.append({"attendee": attendee, "error": to_return(400, 4, testing="no_json")})
        else:
            validation = sends_validate(attendee, attendee.keys())
            if validation != True:
                invalid.append({"attendee": attendee, "error": to_return(400, validation[1], testing="no_json")})
            else:
                validAttende = Attendee()
                if "date_arrived" in attendee:
                    attendee["date_arrived"] = datetime.strptime(attendee["date_arrived"], "%Y-%m-%d %H:%M:%S")
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
            if this_attendee.mispar_ishi and not this_attendee.tehudat_zehut:
                already_mispar_ishi.append(this_attendee.mispar_ishi)
            elif not this_attendee.mispar_ishi and this_attendee.tehudat_zehut:
                already_tehudat_zehut.append(this_attendee.tehudat_zehut)
            else:
                if validation.mispar_ishi == this_attendee.mispar_ishi:
                    already_mispar_ishi.append(this_attendee.mispar_ishi)
                else:
                    already_tehudat_zehut.append(this_attendee.tehudat_zehut)
        else:
            db_open_session()
            if testing != "Ok" and testing != "zeros":
                response_db = db_saving(this_attendee, attendees, testing)
            else:
                response_db = True
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

@attendees_route.get("/get")
async def get_attendees():
    response = db_getting({"type": 1, "table": attendees})
    if response == "error":
        return to_return(500, 99)
    return to_return(200, 0, response)

@attendees_route.put ("/edit")
def edit_attendees(sent: dict):
    if "id" not in sent:
        return to_return(400, 102)
    if "mispar_ishi" not in sent and "tehudat_zehut" not in sent and "full_name" not in sent and "arrived" not in sent and "date_arrived" not in sent:
        return to_return(400, 101)
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    keys = sent.keys()
    validation = sends_validate(sent, keys)
    if validation == True:
        attendee = Attendee()
        if "date_arrived" in sent:
            sent["date_arrived"] = datetime.strptime(sent["date_arrived"], "%Y-%m-%d %H:%M:%S")
        attendee.create_straight(sent)
        response = logic_edit_attendee(attendee, testing)
        return to_return(response[0], response[1]) 
    return to_return(validation[0], validation[1])

def logic_edit_attendee(attendee_to_edit, testing):
    db_validation = db_validating({"type": 3, "id": attendee_to_edit.id})
    if db_validation == "error":
        return (500, 99)
    if db_validation == False:
        return (400, 101)
    if type(db_validation) != bool:
        if attendee_to_edit.mispar_ishi:
            db_validation = db_validating({"type": 1, "mispar_ishi": attendee_to_edit.mispar_ishi}) 
            if db_validation != True and db_validation.id != attendee_to_edit.id:
                return (400, 3)
        if attendee_to_edit.tehudat_zehut:
            db_validation = db_validating({"type": 1, "tehudat_zehut": attendee_to_edit.tehudat_zehut})
            if db_validation != True and db_validation.id != attendee_to_edit.id:
                return (400, 4)
    to_edit = attendee_to_edit.dict(exclude_none=True, exclude={"id"})
    if "date_arrived" in to_edit:
        to_edit["date_arrived"] = datetime.strftime(to_edit["date_arrived"], "%Y-%m-%d %H:%M:%S")
    response = db_updating({"type": 1, "table": attendees, "conditionals": {"id": attendee_to_edit.id}, "values": to_edit})
    if response == "error":
        return (500, 99)
    if response != True:
        return (500, 9)
    return (200, 0)

@attendees_route.delete("/delete/{id}")
def delete_attendee(id: int, testing: str = None):
    validation = sends_validate({"id": id}, ["id"])
    if validation == True:
        response = logic_delete_attendee(id, testing)
        return to_return(response[0], response[1])
    return to_return(validation[0], validation[1])

def logic_delete_attendee(id: int, testing: dict):
    db_validation = db_validating({"type": 2, "id": id})
    if db_validation == "error":
        return (500, 99)
    if db_validation == False:
        return (400, 102)
    db_delete = db_deleting({"id": id, "table": attendees})
    if db_delete == "error":
        return (500, 99)
    if db_delete != True:
        return (500, 9)
    return(200, 0)

@attendees_route.put("/arrived")
def attendee_arrived(sent: dict, testing: str = None):
    if "tehudat_zehut" not in sent and "mispar_ishi" not in sent:
        return to_return(400, 101)
    keys = sent.keys()
    validation = sends_validate(sent, keys)
    if validation == True:
        attendee = Attendee()
        attendee.create_straight(sent)
        response = logic_attendee_arrived(attendee, testing)
        return to_return(response[0], response[1])
    return to_return(validation[0], validation[1])

def logic_attendee_arrived(attendee: Attendee, testing: str = None):
    db_validation = db_validating({"type": 1, "mispar_ishi": attendee.mispar_ishi, "tehudat_zehut": attendee.tehudat_zehut})
    if db_validation == "error":
        return (500, 99)
    if db_validation == True:
        return (400, 104)
    response = db_updating({"type": 1, "table": attendees, "conditionals": {"id": db_validation.id}, "values": {"arrived": True}})
    if response == "error":
        return (500, 99)
    if response != True:
        return (500, 9)
    return (200, 0)

@attendees_route.put("/restart")
def restart_attendace():
    response = db_updating({"type": 2})
    if response == "error":
        return to_return(500, 99)
    return to_return(200, 0)