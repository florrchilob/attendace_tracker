#Imports
from fastapi import APIRouter, Header, HTTPException, status, Request
from fastapi.responses import JSONResponse
from config.db import conn
from models.table_meetings import meetings
from schemas.meetingBD import MeetingBD
from schemas.meetingReceived import MeetingReceived
from datetime import timedelta, datetime
import bcrypt
import httpx
import base64
import json
import pytz
import logging
from routes.verfunctions import update_hours_new_meeting,split_info, check_free_licenses, save_BD, validation, to_return, check_sub_account

#Log manage
logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
loggerRouter = logging.getLogger(__name__)
loggerRouter.addHandler(file_handler)
loggerRouter.propagate = False


# #Router
# meeting_route = APIRouter(prefix = "/meetings", tags = ["account"], responses={status.HTTP_404_NOT_FOUND: {"Message" : "Not Found"}})

# #Gets called just for texting to know all the meetings saved by that time
# @meeting_route.get("/")
# async def home(request: Request):
#     loggerRouter.info(f"An application was received in the home page. Endpoint: {request.url.path}")
#     result = (conn.execute(meetings.select())).fetchall()
#     result_json=[]
#     for meeting in result:
#         addRow = Meeting(**meeting._asdict())
#         addRow = addRow.make_jsonable()
#         addRow = dict(addRow)
#         result_json.append(addRow)
#     result_json = json.dumps(result_json)
#     return result_json

# @meeting_route.post("/example", response_model=dict)
# async def password_to_hash(sent: dict, request: Request):
#     password = sent.get("password")
#     hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
#     print (hash_password)
#     return {"ok" : "ok"}


# #Gets called from the frontend with the meeting thats wanted to save
# @meeting_route.post("/save", response_model=dict)
# async def check_avaliability(new_meeting: MeetingReceived, request: Request, account_agent: str = Header(None)):
#     loggerRouter.info(f"An application was received in the home page. Endpoint: {request.url.path}")
#     validated = validation(new_meeting)
#     if validated == True:
#         response = await logic(new_meeting)
#     else:
#         return validated

# #All the logic in the saving of the meeting
# async def logic(new_meeting: MeetingReceived):
#     sub_account, meeting = split_info(new_meeting)
#     exists = check_sub_account(sub_account)
#     if type(exists) == int:
#         #The account has to register
#         return to_return(400, 100)
#     else:
#         meeting_margins = update_hours_new_meeting(meeting)
#         license = check_free_licenses(meeting)
#         if(license == "error"):
#             return to_return(400, 9)
#         if(license == "licenses"):
#             print('buscar licencias cercanas')
#             response = {'ok' : 'ok'}
#             #lo guardo en la bd como no confirmado 
#             #y devuelvo no oki, el id de la meeting y el nuevo horario 
#         else:
#             response = await save_BD(sub_account, meeting, True, license)
#         #guardo la meeting y devuelvo un ok
#         return response


#recibo la meeting ✓
#Agrego margenes ✓
#Me fijo si en alguno de las admins hay un espacio libre ✓
    #Si si me fijo si la persona esta en algun mail bijlall (si esta pero no estan todos sus datos como mispar hishi agregarlo)
    #si la persona esta en algun admin me fijo si su admin tiene espacio libre (tengo lista de que admins tienen espacio libre)
        #si tiene lo guardo en la base de datos y listo agregar en bd en que admin se guardo
        #si no tiene en su/s admin/s me fijo en que otro admin esta libre y lo agrego al subaccount de zoom 
    #si no esta en ningun admin me fijo cualquier admin que tenga ese espacio libre y lo inscribo al subaccount de zoom 
#Si no, busco el espacio libre mas cercano sin importar en q admin
#si no hay ese dia busco al dia siguiente o al anterior si hay a esa hora o los horarios mas cercanos

# @meeting_route.post("/save", response_model=dict)
#     email_status = await check_email_zoom(new_meeting)
#     if ("status_code" in email_status) == False:
#         if ("status_code" in response) == False:
#             license = posible_license(new_meeting)
#             if ("status_code" in license) == False:
#                 response = await complete_meeting(new_meeting, license)
#                 response = save_meeting(response)
#                 if response["status_code"] == 201:
#                     #Saved right
#                     return JSONResponse(content=response)
#                 else:
#                     #Problem with the data base
#                     return JSONResponse(content=response)
#             else:
#                 #Mail not founded in the zoom page or problem with the Zoom credentials
#                 return JSONResponse(content=response)
#         else:
#                 #Not avaliable license
#             return response
#             return JSONResponse(content=license)
#     else:
#         return email_status