#Imports
from fastapi import APIRouter, status, Request, Header
from datetime import datetime
from fastapi.responses import JSONResponse
import logging
from typing import List
from schemas.meetingReceived import MeetingReceived
from schemas.token import Token
from routes.helpers import to_return, sends_validate, send_mail, token_validating
from routes.db_helpers import db_validating, db_saving, db_getting, db_updating, db_close_session, db_open_session
from routes.accounts_manage_functions import token_generate, complete_account
from models.tables import sub_accounts
from dotenv import find_dotenv, load_dotenv
from routes.meetings_manage_functions import check_free_licenses
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
meetings_route = APIRouter(prefix = "/meetings", tags = ["meeting"], responses={status.HTTP_404_NOT_FOUND: {"Message" : "Not Found"}})
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

secret_key=os.getenv("secret_key")
@meetings_route.get("/")
def home():
    print("aca")
    return to_return(200)

@meetings_route.post("/savemeeting")
async def saveMeeting(sent: dict, JWToken:str = Header(...)):
    meeting = MeetingReceived()
    meeting.create_straight(sent)
    testing = False
    if "testing" in sent:
        testing = sent["testing"]
    validation = sends_validate(meeting, ["day", "since", "until", "people_amount"])
    if validation == True:
        validation = sends_validate({"JWT_token" : JWToken}, ["JWT_token"])
        if type(validation) is dict:
            token = Token(token = validation.get('token'), refresh_token= validation.get('refresh_token'))
            account_id = validation.get("account_id")
            response = await logic_save_meeting(meeting, token, account_id, testing)
            return to_return(response[0], response[1])
    return to_return(validation[0], validation[1])

async def logic_save_meeting(meeting: MeetingReceived, token: str, account_id: int, testing: str):
    token_validation = token_validating({"type": 2, "token": token.token, "id": account_id, "refresh_token": token.refresh_token})
    if token_validation == False or token_validation == "token":
        return (400, 16)
    if token_validation == "error":
        return (500, 99)
    token_renovated = ""
    if token_validation == "token" or token_validation == "refresh_token" or token_validation == "token_expiration" or token_validation == "renovate_token":
        token_renovated = token_generate()
        db_open_session()
        response = db_updating({"type": 1, "table": sub_accounts, "conditionals": {"token" : token.token}, 
                                "values" : {"token": token_renovated.token, "refresh_token": token_renovated.refresh_token, "token_expiration" : token_renovated.expiration}})
        db_close_session()
        if response == "error" or response == False:
            return(500, 99)
    response_licenses = check_free_licenses(meeting)
    print(response_licenses)
    return(200, 0)

   
    #     meeting_margins = update_hours_new_meeting(meeting)
    #     license = check_free_licenses(meeting)
    #     if(license == "error"):
    #         return to_return(400, 9)
    #     if(license == "licenses"):
    #         print('buscar licencias cercanas')
    #         response = {'ok' : 'ok'}
    #         #lo guardo en la bd como no confirmado 
    #         #y devuelvo no oki, el id de la meeting y el nuevo horario 
    #     else:
    #         response = await save_BD(sub_account, meeting, True, license)
    #     #guardo la meeting y devuelvo un ok
    #     return response