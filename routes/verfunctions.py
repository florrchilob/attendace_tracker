#Imports
from fastapi import APIRouter, Header, HTTPException, status, Request
from fastapi.responses import JSONResponse
from datetime import time, date, datetime
from sqlalchemy import select, or_
from config.db import conn
from models.table_meetings import meetings
from models.table_meetings import admin_accounts_x_licenses
from models.table_meetings import sub_accounts
from models.table_meetings import admin_accounts
from models.table_meetings import licenses
from schemas.meetingBD import MeetingBD
from schemas.meetingReceived import MeetingReceived
from schemas.sub_account import SubAccount
from schemas.license import License
from schemas.admin_account_x_license import AdminAccountXLicense
from schemas.meetingBD import MeetingBD
from datetime import timedelta, datetime
import httpx
import base64
import json
import pytz
import logging

#Checks that the sub_account is already approved and part of our system
async def check_sub_account(sub_account: SubAccount):
    query = (sub_accounts.select().filter(or_(sub_accounts.c.name == sub_accounts.name, sub_accounts.c.mispar_ishi == sub_accounts.mispar_ishi, sub_accounts.c.mail == sub_accounts.mail)))
    response = conn.execute(query).fetchall()
    print(response)
    return 1

#Returns the response in a valid way
def to_return(status_code, error):
    match error:
        case 1:
            detail = "Name not valid"
        case 2:
            detail = "Not full name"
        case 3: 
            detail = "Mispar ishi not valid"
        case 4:
            detail = "Mail not valid"
        case 5:
            detail = "Date type not valid"
        case 6:
            detail = "Since type not valid" 
        case 7:
            detail = "Until type not valid" 
        case 8:
            detail = "Amount of people not valid" 
        case 9:
            detail = "No connection to database" 
        case 10:
            detail  = "Account does not exists"
        case _:
            detail = "No problem"

    match status_code:
        case 200:
            status = "CREATED"
        case 400:
            status = "BAD_REQUEST"
        case _:
            status = "BAD_REQUEST"

    return {"status_code" : status_code, "status" : status, "error" : error ,"detail" : detail}

#Validates the meeting recieved
def validation(new_meeting: MeetingReceived):
    if len(new_meeting.name.strip()) < 0 or type(new_meeting.name) != str:
        to_return(400, 1)
    else:
        words = new_meeting.name.split(" ")
        if len(words) < 2:
            return(to_return(400, 2))
        elif type(new_meeting.mispar_ishi) != int or new_meeting.mispar_ishi < 1000:
            return(to_return(400, 3))
        else:
            no_spaces = (new_meeting.mail.strip()).split(" ")
            if len(no_spaces) > 1 or type(new_meeting.mail) != str or not ("@" in new_meeting.mail):
                return(to_return(400, 4))
            elif type(new_meeting.day) != date:
                return(to_return(400, 5))
            elif type(new_meeting.since) != time:
                return(to_return(400, 6))
            elif type(new_meeting.until) != time:
                return(to_return(400, 7))
            elif type(new_meeting.people_amount) != int or new_meeting.people_amount not in [100, 200, 300, 500, 1000]:
                return(to_return(400, 8))
    return True


#Split the meeting recived in diferent classes
def split_info(meeting_recived: MeetingReceived):
    sub_account = SubAccount(name = meeting_recived.name, mispar_ishi = meeting_recived.mispar_ishi, mail = meeting_recived.mail)
    meeting = MeetingBD(day = meeting_recived.day, since = meeting_recived.since, until = meeting_recived.until, people_amount = meeting_recived.people_amount)
    return sub_account, meeting

#Adds the margin to the meeting to make sure that theres anought time to change the licenses between the meetings
def update_hours_new_meeting(new_meeting: MeetingReceived):
    since_datetime = datetime.combine(new_meeting.day, new_meeting.since)
    until_datetime = datetime.combine(new_meeting.day, new_meeting.until)
    margin = timedelta(minutes=6, seconds=30)
    new_since = since_datetime - margin
    new_until = until_datetime + margin
    new_since = new_since.time().replace(microsecond=0)
    new_until = new_until.time().replace(microsecond=0)
    new_meeting.change_time (new_since, new_until)
    return new_meeting

#Calls to all the needed functions to return the free licenses or the proper return id theres none free licenses
def check_free_licenses(new_meeting: MeetingReceived):
    same_hour = get_same_hours(new_meeting)
    if (same_hour==False): 
        #error en la busqueda a BD
        return "error"
    all_licenses = get_all_licenses(new_meeting)
    licenses_left = check_licenses_left(all_licenses, same_hour)
    if (licenses_left == False):
        #No licenses avaliable
        return "licenses"
    return licenses_left

#Returns the meetings in the same hours
def get_same_hours(new_meeting: MeetingReceived):
    try:
        query = meetings.select().filter(meetings.c.day == new_meeting.day)
        same_day = conn.execute(query).fetchall()
    except:
        return []
    if(same_day == []):
        return []
    same_hour = []
    for this_meeting in same_day:
        this_meeting_class = MeetingBD(id = this_meeting.id, day = this_meeting.day, since = this_meeting.since, until = this_meeting.until, license_id = this_meeting.license_id, admin_account_id = this_meeting.admin_account_id)
        if new_meeting.since > this_meeting.since and new_meeting.since < this_meeting.until:
            same_hour.append(this_meeting_class)
        elif new_meeting.until > this_meeting.since and new_meeting.until < this_meeting.until: 
            same_hour.append(this_meeting_class)
        elif new_meeting.since < this_meeting.since and new_meeting.until > this_meeting.until:
            same_hour.append(this_meeting_class)
        elif new_meeting.since == this_meeting.since and new_meeting.until == this_meeting.until:
            same_hour.append(this_meeting_class)
    return same_hour

#Returns all the licenses that all the admins have
def get_all_licenses(new_meeting: MeetingReceived):
    query = (select(admin_accounts_x_licenses.c.id, admin_accounts_x_licenses.c.license_id, admin_accounts_x_licenses.c.admin_account_id, admin_accounts_x_licenses.c.amount_licenses)
             .select_from(
                licenses.join(
                    admin_accounts_x_licenses, 
                    licenses.c.id == admin_accounts_x_licenses.c.license_id
                ).join(
                    admin_accounts,
                    admin_accounts_x_licenses.c.admin_account_id == admin_accounts.c.id
                )
             )
            .filter(licenses.c.amount_people >= new_meeting.people_amount,
                     admin_accounts_x_licenses.c.amount_licenses > 0)
    )
    all_licenses = conn.execute(query).fetchall()
    licenses_to_return = []
    for license in all_licenses:
        new_license = AdminAccountXLicense(id = license.id, license_id = license.license_id, admin_account_id = license.admin_account_id, amount_licenses =  license.amount_licenses)
        licenses_to_return.append(new_license)
    return licenses_to_return

#Recieves all the licenses and the used ones to see which ones are left and returnes the ones left
def check_licenses_left(all_licenses, same_hours):
    free_licenses = all_licenses
    for usedLicense in same_hours:
        for index, license in enumerate(all_licenses): 
            if(usedLicense.license_id == license.id):
                license.update_amount(license)
                if(license.amount_licenses <= 0):
                    del free_licenses[index]
                    break
                free_licenses[index] = license
                break
    if(len(free_licenses) == 0):
        return False
    sorted_list = sorted(free_licenses, key=lambda x: x.license_id)
    return sorted_list[0]

#Saves the meeting in the database
async def save_BD(account: SubAccount, meeting: MeetingBD, confirmed: bool, license: AdminAccountXLicense):
    account_id = await save_account(account)
    response = await save_meeting(account_id, meeting, confirmed, license)
    return response


#Saves the meeting in the database
async def save_meeting(account_id : int, meeting: MeetingBD, confirmed: bool, license: AdminAccountXLicense):
    meeting.complete_meeting(sub_account_id = account_id, confirmed = confirmed, licensed_now = False, license_id = license.id, admin_account_id = license.admin_account_id)
    query = meetings.insert().values(**meeting.__dict__)
    # response = conn.execute(query)
    response = ''
    try:
        if response.rowcount == 1:
            conn.commit()
            return {"status_code" : 201, "status" : "CREATED", "ID" : response.lastrowid}
        else:
            return  {"status_code" : 400, "status" : "BAD_REQUEST", "error" : 1 ,"detail" : "No conection no database"}

    except Exception as e:
        return  {"status_code" : 400, "status" : "BAD_REQUEST", "error" : 1 ,"detail" : "No conection no database"}



# #Returns array with all the meetings that are already in the database in the same hours of the possible new meeting
# def get_same_hours(same_day, new_meeting): 
#     same_hour = []
#     used_licenses = []
#     print(same_day)
#     # for this_meeting in same_day:
#     #     if new_meeting.since > this_meeting.since and new_meeting.since < this_meeting.until:
#     #         same_hour.append(this_meeting)            
#     #         used_licenses.append(this_meeting.license_type_needed) 
#     #     elif new_meeting.until > this_meeting.since and new_meeting.until < this_meeting.until: 
#     #         same_hour.append(this_meeting)
#     #         used_licenses.append(this_meeting.license_type_needed)
#     #     elif new_meeting.since < this_meeting.since and new_meeting.until > this_meeting.until:
#     #         same_hour.append(this_meeting)
#     #         used_licenses.append(this_meeting.license_type_needed)
#     #     elif new_meeting.since == this_meeting.since and new_meeting.until == this_meeting.until:
#     #         same_hour.append(this_meeting)
#     #         used_licenses.append(this_meeting.license_type_needed) 
#     return same_hour, used_licenses


# async def check_email_zoom (new_meeting: Meeting) :
#     complete_token = await get_token()
#     complete_token = json.loads(complete_token)
#     token = complete_token["access_token"]
#     zoom_id = await get_id_zoom(token, new_meeting.mail)
#     if("status_code" in zoom_id) :
#         url = f"https://api.zoom.us/v2/accounts"
#         headers = {
#             "Host" : "zoom.us",
#             "Authorization" :  "Bearer " + token
#         }
#         body = {
#             "action": "create",
#             "account_info": {
#                 "email": "Aka12@ssltd.co.il",
#                 "type": 1
#             }
#         }
#         # print(body.json.)
#         async with httpx.AsyncClient() as client:
#             response = await client.post(url, headers=headers, json=body)
#             print(response)
#             if(response.status_code == 201):
#                 return  {"status_code" : 400, "status" : "New account In Zoom"}
#             else:
#                 return  {"status_code" : 400, "status" : "BAD_REQUEST", "error" : 4 ,"detail" : "Id from Zoom not returned, check later"}
#     else:
#         return True



# #gets all list of accounts from an admin 
#     clientId = '1Ds9iWO5QG6OwVATmcEF9A'
#     clientSecret = 'z7Y8FlvMefgA5mInHsVVj278VKnLJm9V'
#     accountId = '381NJiUnTpuB0dbEqVQdPA'
#     text = f"{clientId}:{clientSecret}"
#     encoded = base64.b64encode(text.encode("ascii"))
#     ids = str(encoded)
#     ids = ids[2:-1]
#     url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={accountId}"
#     headers = {
#         "Host" : "zoom.us",
#         "Authorization" : "Basic " + ids
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, headers=headers)
#     if response.status_code == 200:
#         data = (response.text)
#     else:
#         #needed to be changed after
#         data =  {"status_code" : 400, "status" : "BAD_REQUEST", "error" : 3 ,"detail" : "Token not returned from Zoom, check zoom credentials"}

#     access_token = json.loads(data)
#     token_to_header = access_token.get("token_type") + " " + access_token.get("access_token")
    
#     url = "https://api.zoom.us/v2/accounts"
#     headers = {
#         "Host" : "zoom.us",
#         "Authorization" : token_to_header,
#         "page_size" : "300"
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         print(response.text)

#     return {"ok" : "ok"}






# #Returns the meeting completed to be saved in the database
# async def complete_meeting(new_meeting: Meeting, license: dict):
#     complete_token = await get_token()
#     if ("status_code" in complete_token) == False:
#         complete_token = json.loads(complete_token)
#         token = complete_token["access_token"]
#         zoom_id = await get_id_zoom(token, new_meeting.mail)
#         if ("status_code" in zoom_id) == False:
#             zoom_id = json.loads(zoom_id)
#             zoom_id = zoom_id.get("id")
#             confirmed = True
#             licensed_now = False
#             license_type_needed = license["name_zoom"]
#             new_meeting.complete_meeting(zoom_id, confirmed, licensed_now, license_type_needed)
#             return new_meeting
#         else:
#             return zoom_id
#     else:
#         return complete_token
    
# #Returns the token returned from Zoom 
# async def get_token():
#     ids = get_credentials_encoded()
#     url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={meeting_route.CREDENTIALS_ZOOM['accountId']}"
#     headers = {
#         "Host" : "zoom.us",
#         "Authorization" : "Basic " + ids
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, headers=headers)
#     if response.status_code == 200:
#         return (response.text)
#     else:
#         return  {"status_code" : 400, "status" : "BAD_REQUEST", "error" : 3 ,"detail" : "Token not returned from Zoom, check zoom credentials"}

# #Returns the credentials of the account encoded
# def get_credentials_encoded():
#     text = f"{meeting_route.CREDENTIALS_ZOOM['clientId']}:{meeting_route.CREDENTIALS_ZOOM['clientSecret']}"
#     encoded = base64.b64encode(text.encode("ascii"))
#     ids = str(encoded)
#     ids = ids[2:-1]
#     return ids

# #Returns the id of the account in Zoom
# async def get_id_zoom(token, mail):
#     url = f"https://api.zoom.us/v2/accounts/{mail}"
#     headers = {
#         "Host" : "zoom.us",
#         "Authorization" :  "Bearer " + token
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.text
#     else:
#         return  {"status_code" : 400, "status" : "BAD_REQUEST", "error" : 4 ,"detail" : "Id from Zoom not returned, check mail"}

#funcion que cambia la licencia del account, falta adaptarla a agarrar las credenciales de la cuenta de la base de datos en vez de q esten aca escritas
#Getting the token de la account
    # clientId = 'NNQYaNoXTI26nCLxarAo1g'
    # clientSecret = 'yarmD2uyTE0r8k1sSV3crLbWpaYqWxQL'
    # accountId = 'zy6dMko4SkOYsMoXVKKgcw'
    # text = f"{clientId}:{clientSecret}"
    # encoded = base64.b64encode(text.encode("ascii"))
    # ids = str(encoded)
    # ids = ids[2:-1]
    # url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={accountId}"
    # headers = {
    #     "Host" : "zoom.us",
    #     "Authorization" : "Basic " + ids
    # }
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(url, headers=headers)
    # if response.status_code == 200:
    #     data = (response.text)
    # else:
    #     #needed to be changed after
    #     data =  {"status_code" : 400, "status" : "BAD_REQUEST", "error" : 3 ,"detail" : "Token not returned from Zoom, check zoom credentials"}


    # #esto de abajo no funciona cuando da error desde zoom
    # access_token = json.loads(data)
    # token_to_header = access_token.get("token_type") + " " + access_token.get("access_token")
    
    # #cambio la licencia del account
    # mail = 'itayab7@gmail.com'
    # if access_token.get("access_token") != "-99":
    #     url = "https://api.zoom.us/v2/accounts/features"
    #     headers = {
    #         "Host" : "zoom.us",
    #         "Authorization" : token_to_header
    #     }
    #     payload = {
    #         "feature_type" : "account_type",
    #         "feature_value" : 1,
    #         "large_meeting" : 0,
    #         "accounts": [{"email" : mail}]
    #     }

    #     async with httpx.AsyncClient() as client:
    #         response = await client.post(url, headers=headers ,json=payload)
    #         print(response.text)
    #         return {"ok":"ok"}


# #Creates the meeting in the DB
# def save_meeting(new_meeting: Meeting): 
#     try:
#         query = meetings.insert().values(**new_meeting.__dict__)
#         response = conn.execute(query)
#         if response.rowcount == 1:
#             conn.commit()
#             return {"status_code" : 201, "status" : "CREATED", "ID" : response.lastrowid}
#         else:
#             return  {"status_code" : 400, "status" : "BAD_REQUEST", "error" : 1 ,"detail" : "No conection no database"}
#     except Exception as e:
#         return  {"status_code" : 400, "status" : "BAD_REQUEST", "error" : 1 ,"detail" : e}



# #End of the saving functions start of the change of the license according the hour

# #Checks if there's a meeting in x minutes or less and changes that license to licensed and to the right amount of people and checks if a meeting already ended and changes the license to basic
# @meeting_route.get("/license")
# async def change_license():
#     future_time, current_date, now = get_time_to_check()
#     query = meetings.select().where(meetings.c.day == current_date, meetings.c.since < future_time, meetings.c.licensed_now == False)
#     meetings_to_start = conn.execute(query).fetchall()
#     query = meetings.select().where(meetings.c.day == current_date, meetings.c.until < now, meetings.c.licensed_now == True)
#     meetings_to_end = conn.execute(query).fetchall()
#     id_meetings_start, id_meetings_end, accounts_to_type1, accounts_to_type32, accounts_to_type64, accounts_to_type128, accounts_to_type256, accounts_to_end = get_variables(meetings_to_start, meetings_to_end)
# # CHANGE THE 0 IN LARGE MEETING WHEN DIFERENT LICENSES WITH DIFERENT AMOUNT OF PEOPLE
#     if len(accounts_to_end) > 0:
#         await change_zoom(accounts_to_end, feature_type = "account_type", feature_value = 1, large_meeting=0)
#     if len(accounts_to_type1) > 0:
#         await change_zoom(accounts_to_type1, feature_type = "account_type", feature_value = 2, large_meeting=0)
#     if len(accounts_to_type32) > 0:
#         await change_zoom(accounts_to_type32, feature_type = "account_type", feature_value = 2, large_meeting=0)
#     if len(accounts_to_type64) > 0:
#         await change_zoom(accounts_to_type64, feature_type = "account_type", feature_value = 2, large_meeting=0)
#     if len(accounts_to_type128) > 0:
#         await change_zoom(accounts_to_type128, feature_type = "account_type", feature_value = 2, large_meeting=0)
#     if len(accounts_to_type256) > 0:
#         await change_zoom(accounts_to_type256, feature_type = "account_type", feature_value = 2, large_meeting=0)
#     response = await save_in_db(id_meetings_end, id_meetings_start)
#     return response

# #Returns the time in and before x minutes
# def get_time_to_check():
#     here_time_zone = pytz.timezone('Asia/Jerusalem')
#     now = datetime.now(here_time_zone)
#     current_date = now.date()
#     current_time = now.time()
#     current_complete_date = datetime.combine(current_date, current_time)
#     time_to_check = timedelta(minutes=5)
#     future_time = current_complete_date + time_to_check
#     future_time = future_time.time().replace(microsecond=0)
#     return future_time, current_date, now

# #Returns the variables of the meetings that need to be updated
# def get_variables(meetings_start, meetings_end):
#     id_meetings_start = []
#     id_meetings_end = []
#     accounts_to_type1 = []
#     accounts_to_type32 = []
#     accounts_to_type64 = []
#     accounts_to_type128 = []
#     accounts_to_type256 = []
#     accounts_to_end = []

#     for meeting in meetings_start:
#         id_meetings_start.append(meeting["id"])
#         if meeting["license_type_needed"] == 1:
#             current_account = {"id" : meeting.zoom_id, "email" : meeting.mail}
#             accounts_to_type1.append(current_account)
#         elif meeting["license_type_needed"] == 32:
#             current_account = {"id" : meeting.zoom_id, "email" : meeting.mail}
#             accounts_to_type32.append(current_account)
#         elif meeting["license_type_needed"] == 64:
#             current_account = {"id" : meeting.zoom_id, "email" : meeting.mail}
#             accounts_to_type64.append(current_account)
#         elif meeting["license_type_needed"] == 128:
#             current_account = {"id" : meeting.zoom_id, "email" : meeting.mail}
#             accounts_to_type128.append(current_account)
#         elif meeting["license_type_needed"] == 256:
#             current_account = {"id" : meeting.zoom_id, "email" : meeting.mail}
#             accounts_to_type256.append(current_account)

#     for meeting in meetings_end:
#         id_meetings_end.append(meeting["id"])
#         current_account = {"id" : meeting.zoom_id, "email" : meeting.mail}
#         accounts_to_end.append(current_account)

#     return id_meetings_start, id_meetings_end, accounts_to_type1, accounts_to_type32, accounts_to_type64, accounts_to_type128, accounts_to_type256, accounts_to_end

# #Updeates the licenses in the zoom's page
# async def change_zoom(to_change, feature_type, feature_value, large_meeting):
#     access_token = json.loads(await get_token())
#     if access_token.get("access_token") != "-99":
#         token_to_header = access_token.get("token_type") + " " + access_token.get("access_token")
#         url = "https://api.zoom.us/v2/accounts/features"
#         headers = {
#             "Host" : "zoom.us",
#             "Authorization" : token_to_header
#         }
#         payload = {
#             "feature_type": feature_type,
#             "feature_value":feature_value,
#             "large_meeting" : large_meeting,
#             "accounts": to_change
#         }

#         async with httpx.AsyncClient() as client:
#             response = await client.post(url, headers=headers ,json=payload)

# #Updates the meetings's license in the database 
# async def save_in_db(id_to_false, id_to_true):
#     query = meetings.update().values(licensed_now = False).where(meetings.c.id.in_(id_to_false))
#     response = conn.execute(query)
#     query = meetings.update().values(licensed_now = True).where(meetings.c.id.in_(id_to_true))
#     response = conn.execute(query)
#     return conn.execute(meetings.select()).fetchall()