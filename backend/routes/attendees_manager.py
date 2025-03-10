#Imports
from fastapi import APIRouter, status, FastAPI
import asyncio
import logging
from fastapi.responses import StreamingResponse
from typing import List
from schemas.attendee import Attendee
from routes.helpers import to_return, sends_validate
from routes.db_helpers import db_validating, db_saving, db_getting, db_updating, db_close_session, db_open_session, db_deleting, db_bulk_saving
from models.tables import attendees
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
import json
import os


#Log manager
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

app = FastAPI()

active_connections: List[asyncio.Queue] = []

@attendees_route.get("/clients")
async def get_clients():
    queue = asyncio.Queue()
    active_connections.append(queue)

    async def event_stream():
        try:
            while True:
                message = await queue.get()
                print("sent okey")
                yield f"event: {message['action']}\ndata: {json.dumps(message['data'])}\n\n"
        except asyncio.CancelledError:
            print("error")
            active_connections.remove(queue)
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@attendees_route.get("/")
def home():
    return to_return(200)

#Route called to sign up a new account to the system
@attendees_route.post("/create")
async def createattendees(sent: dict):
    if sent == None:
        return to_return(400, 101)
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
        if "mispar_ishi" not in attendee and "tehudat_zehut" not in attendee:
            invalid.append({"attendee": attendee, "error": to_return(400, 102, testing="no_json")})
        elif "full_name" not in attendee:
            invalid.append({"attendee": attendee, "error": to_return(400, 1, testing="no_json")})
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
    response = await logic_create_attendees(valid, invalid, testing)
    if len(response) < 3:
        return to_return(response[0], response[1]) 
    else:
        return to_return(response[0], response[1], response[2])
    

#Logic behind the create function
async def logic_create_attendees(validAttendees: list, invalid: List, testing):
    already_mispar_ishi = []
    already_tehudat_zehut = []
    added_mispar_ishi = []
    added_tehudat_zehut = []
    full_attendees_added = []
    new_attendees_to_save = []

    mispar_ishi_list = [attendee.mispar_ishi for attendee in validAttendees if attendee.mispar_ishi is not None]
    tehudat_zehut_list = [attendee.tehudat_zehut for attendee in validAttendees if attendee.tehudat_zehut is not None]

    mispar_validation = db_validating({
        "type": 4,
        "column_name": "mispar_ishi",
        "values_list": mispar_ishi_list
    }) if mispar_ishi_list else {"existing_values": set(), "missing_values": set()}

    tehudat_validation = db_validating({
        "type": 4,
        "column_name": "tehudat_zehut",
        "values_list": tehudat_zehut_list
    }) if tehudat_zehut_list else {"existing_values": set(), "missing_values": set()}

    if mispar_validation == "error" or tehudat_validation == "error":
        return (500, 99)

    current_time = datetime.now()
    for attendee in validAttendees:
        is_existing = False
        if attendee.mispar_ishi and str(attendee.mispar_ishi) in mispar_validation["existing_values"]:
            already_mispar_ishi.append(attendee.mispar_ishi)
            is_existing = True
        
        if attendee.tehudat_zehut and str(attendee.tehudat_zehut) in tehudat_validation["existing_values"]:
            already_tehudat_zehut.append(attendee.tehudat_zehut)
            is_existing = True
        
        if not is_existing:
            if attendee.arrived:
                attendee.date_arrived = current_time
            new_attendees_to_save.append(attendee)
    if new_attendees_to_save and testing != "Ok" and testing != "zeros":
        result = db_bulk_saving(new_attendees_to_save, attendees, testing)
        if result == "error":
            return (500, 99)
        
        for attendee in new_attendees_to_save:
            full_attendees_added.append(attendee.return_dict())
            date_arrived_json = attendee.date_arrived.strftime("%H:%M") if attendee.date_arrived else None
            
            if attendee.mispar_ishi:
                added_mispar_ishi.append({
                    "id": attendee.mispar_ishi,
                    "full_name": attendee.full_name,
                    "date_arrived": date_arrived_json
                })
            else:
                added_tehudat_zehut.append({
                    "id": attendee.tehudat_zehut,
                    "full_name": attendee.full_name,
                    "date_arrived": date_arrived_json
                })

    returning = {
        "missing_data": invalid,
        "already_database": {
            "mispar_ishi": already_mispar_ishi,
            "tehudat_zehut": already_tehudat_zehut
        },
        "successfull": {
            "mispar_ishi": added_mispar_ishi,
            "tehudat_zehut": added_tehudat_zehut
        }
    }

    if len(added_mispar_ishi) > 0 or len(added_tehudat_zehut) > 0:      
        message = {
            "action": "create",
            "data": {"attendees": full_attendees_added}
        }
        for queue in active_connections:
            try:
                await queue.put(message)
            except Exception as e:
                logging.error(f"Error sending the message: {e}")
        return (201, 0, returning)
    return (400, 101, returning)

@attendees_route.get("/getby/{filter}/{value}")
async def get_attendees(filter: str, value: str):
    validation = sends_validate({"filter": filter, "value": value}, ["filter", "value"])
    if validation == True:
        response = await logic_get_attendees(filter, value)
        if len(response) == 3:
            return to_return(response[0], response[1], response[2])
        return to_return(response[0], response[1])
    return to_return(validation[0], validation[1])


async def logic_get_attendees(filter: str, value: str):
    if filter == "name":
        filter = "full_name"
    attendees = db_getting(
        {
            "type": 3, 
            "values": ["id", "mispar_ishi", "tehudat_zehut", "full_name", "arrived", "date_arrived"], 
            "conditionals": [{filter: value}]
        }
    )
    if attendees == False:
        return (400, 104)
    return (200, 0, attendees)

@attendees_route.put ("/edit")
async def edit_attendees(sent: dict):
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
        response = await logic_edit_attendee(attendee, testing)
        return to_return(response[0], response[1]) 
    return to_return(validation[0], validation[1])

async def logic_edit_attendee(attendee_to_edit, testing):
    db_validation = db_validating({"type": 3, "id": attendee_to_edit.id})
    if db_validation == "error":
        return (500, 99)
    if db_validation == False:
        return (400, 101)

    changes = {"id": attendee_to_edit.id}

    if type(db_validation) != bool:
        for key, value in attendee_to_edit.dict(exclude_none=True).items():
            if key != "id" and getattr(db_validation, key, None) != value:
                changes[key] = value

    if "date_arrived" in changes:
        changes["date_arrived"] = datetime.strftime(changes["date_arrived"], "%Y-%m-%d %H:%M:%S")
        changes["arrived"] = True

    if len(changes) == 1:
        return (400, 102)

    response = db_updating({
        "type": 1,
        "table": attendees,
        "conditionals": {"id": attendee_to_edit.id},
        "values": changes
    })

    if response == "error":
        return (500, 99)
    if response != True:
        return (500, 9)

    message = {
        "action": "update",
        "data": changes
    }

    for queue in active_connections:
        try:
            await queue.put(message)
        except Exception as e:
            logging.error(f"Error sending the message: {e}")

    return (200, 0)

@attendees_route.delete("/delete/{id}")
async def delete_attendee(id: int, testing: str = None):
    validation = sends_validate({"id": id}, ["id"])
    if validation == True:
        response = await logic_delete_attendee(id, testing)
        return to_return(response[0], response[1])
    return to_return(validation[0], validation[1])

async def logic_delete_attendee(id: int, testing: dict):
    db_validation = db_validating({"type": 2, "id": id})
    if db_validation == "error":
        return (500, 99)
    if db_validation == False:
        return (400, 102)
    db_delete = db_deleting({"type": 2, "id": id, "table": attendees})
    if db_delete == "error":
        return (500, 99)
    if db_delete != True:
        return (500, 9)
    message = {
        "action": "delete_user",
        "data": {"id": id}
    }
    for queue in active_connections:
        try:
            await queue.put(message)
        except Exception as e:
            logging.error(f"Error sending the message: {e}")
    return(200, 0)

@attendees_route.put("/arrived")
async def attendee_arrived(sent: dict, testing: str = None):
    if "tehudat_zehut" not in sent and "mispar_ishi" not in sent:
        return to_return(400, 101)
    keys = sent.keys()
    validation = sends_validate(sent, keys)
    if validation == True:
        attendee = Attendee()
        attendee.create_straight(sent)
        response = await logic_attendee_arrived(attendee, testing)
        if len(response) == 3:
            return to_return(response[0], response[1], response[2])
        else:
            return to_return(response[0], response[1])
    return to_return(validation[0], validation[1])

async def logic_attendee_arrived(attendee: Attendee, testing: str = None):
    db_validation =  db_validating({"type": 1, "mispar_ishi": attendee.mispar_ishi, "tehudat_zehut": attendee.tehudat_zehut})
    if db_validation == "error":
        return (500, 99)
    if db_validation == True:
        return (400, 104)
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S")
    response = db_updating({"type": 1, "table": attendees, "conditionals": {"id": db_validation.id}, "values": {"arrived": True, "date_arrived": formatted_date}})
    if response == "error":
        return (500, 99)
    if response != True:
        return (500, 9)
    response = db_getting({"type": 2, "table": attendees, "values":["full_name", "date_arrived"], "conditionals": {"id": db_validation.id}})
    if response == "error" or response == []:
        return (500, 99)
    row_dict = response[0]._asdict()
    row_dict["date_arrived"] = row_dict["date_arrived"].strftime("%H:%M")
    message = {
        "action": "update",
        "data": {"id": db_validation.id, "arrived": True, "date_arrived": formatted_date}
    }
    for queue in active_connections:
        try:
            await queue.put(message)
        except Exception as e:
            logging.error(f"Error sending the message: {e}")
    return (200, 0, row_dict)

@attendees_route.put("/restart")
async def restart_attendace():
    response = db_updating({"type": 2})
    if response == "error":
        return to_return(500, 99)
    message = {
    "action": "restart_all",
    "data": {}
    }
    for queue in active_connections:
        try:
            await queue.put(message)
        except Exception as e:
            logging.error(f"Error sending the message: {e}")
    return to_return(200, 0)


@attendees_route.delete("/deleteall")
async def delete_all_attendees():
    response = db_deleting({"type": 1, "table": attendees})
    if response == "error":
        return to_return(500, 99)
    message = {
        "action": "delete_all",
        "data": {}
    }
    for queue in active_connections:
        try:
            await queue.put(message)
        except Exception as e:
            logging.error(f"Error sending the message: {e}")
    return to_return(200, 0)