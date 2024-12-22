#Imports
from datetime import time, datetime
from email.message import EmailMessage
from fastapi.responses import JSONResponse
from routes.db_helpers import db_validating
from fastapi import Request
import routes
import ssl 
import smtplib
import base64
import json
import jwt
import re

#Returns the response in a valid way
def to_return(status_code, error=0, data={}, testing= None):
    match error:
        case 1:
            message = "Name not valid"
        case 2:
            message = "Not full name"
        case 3: 
            message = "Mispar Ishi not valid"        
        case 4: 
            message = "Tehudat Zehut not valid"
        case 9:
            message = "No connection to database" 
        case 10:
            message = "Account does not exists"
        case 15:
            message = "No needed"
        case 99:
            message = "Database error"
        case 100: 
            message = "Error"
        case 101:
            message = "No valid"
        case 104:
            message = "No matches to your search"
        case _:
            message = "Page not exists"

    match status_code:
        case 200:
            status ="OK" 
        case 201:
            status = "CREATED"
        case 400:
            status = "BAD_REQUEST"
        case 500:
            status = "INTERNAL SERVER ERROR"
        case _:
            status = "BAD_REQUEST"
    if status_code == 200 or status_code == 201:
        if data == {}:
            content = {"status" : status}
        else:
            content = {"status": status, "data": data}
    else:
        if data == {}:
            content = {"status" : status, "error_code" : error, "message" : message}
        else:
            content = {"status" : status, "data": data, "error_code" : error, "message" : message}
    if testing == "no_json":
        return {"status_code": status_code} | content
    return JSONResponse (status_code=status_code, content=content)

#Formats all the data to unique standards
def to_standard(account, value, key):
    if type(value) == int:
        if value < 1 and value > 0:
            value = int(str(value[1:]))
            setattr(account, key, value)
            return value
    if key == "mail":
        if type(value) == str:
            value = value.lower()
            setattr(account, key, value)
            return value
    return value

#Sends every value to validate
def sends_validate(to_validate, values):
    since = None
    if type(to_validate) == dict:
        to_validate = to_validate.items()
    for key, value in to_validate:
        if key in values:
            validation = True
            if value is not None:
                value = to_standard(to_validate, value, key)
            validation = validating(key, value, type(value))
            if key == "since":
                since = value
            if key == "until":
                if value < since:
                    return (400, 4.1)
            if validation != True:
                token = any(k == "token" for k, v in to_validate)
                if key == "account_id" and token == True:
                    return (400, 16)
                if type(validation) == tuple:
                    return (validation[0], validation[1])
                return validation
    return True

#Validates all the necessary values
def validating(key, value, type_variable):
    match key:
        case "name":
            if value == None:
                return (400, 1)
            if type_variable != str or len(value.strip()) < 0:
                return (400, 1)
            else:
                words = value.split(" ")
                if len(words) < 2:
                    return (400, 2)
            if len(value)>254:
                return (400, 1)
            hebrew_pattern = re.compile(r'^[\u0590-\u05FF\s]+$')
            english_pattern = re.compile(r'^[a-zA-Z\s]+$')
            hebrew = bool(hebrew_pattern.match(value))
            english = bool(english_pattern.match(value))
            if not hebrew and not english:
                return (400, 1)
        case "mispar_ishi":
            if value == None:
                return (400, 3)
            if type_variable == str:
                try:
                    value = int(value)
                except:
                    return (400, 3)
            if len(str(value)) < 5 or len(str(value)) > 7:
                return (400, 3)
        case "tehudat_zehut":
            if value == None:
                return (400, 4)
            if type_variable == str:
                try:
                    value = int(value)
                except:
                    return (400, 4)
            if len(str(value)) != 9:
                return (400, 4)
        case "variable":
            if value == None: 
                return (400, 103)  
            if value not in ["name", "mail", "mispar_ishi", "telephone"]:
                return (400, 103) 
        case "value": 
            if value == None:
                return (400, 103) 
            if type_variable == int and value < 100:
                return (400, 103)
            if type_variable == str and len(value) < 3:
                return (400, 103)
    return True

#sends email to Account
def send_mail(to_send):
    #type_variable 1 = validation new Account
    email_sender = "zoomidfcalendar@gmail.com"
    email_password = "meps hymc gpog qrvu"
    email_receiver = to_send.get("mail")
    type_variable = to_send.get("type")
    name = ""
    if to_send.get("name") != None:
        name = to_send.get("name").title()
    if type_variable == 1:
        token = to_send.get("token")
        href = f"http://localhost:5173/validateaccount/{token}"
        subject = "אנא אמת את משתמש שלך "
        body = f"""
            <!DOCtype_variable html>
                <html lang="he">
                <head>
                    <meta charset="UTF-8">
                    <title>Verification Email</title>
                </head>
                <body dir="rtl">
                    <h1>שלום רב, {name}</h1>
                    <p style="font-size:20px;">אנא אמת את המשתמש שלך </p>
                    <p style="font-size:20px;">נא ללחוץ על הקישור <a href="{href}">{href}</a></p>
                    <br/>
                    <br/>
                    <br/>
                    <p style="font-size:13px;">אם אינך מצליח לפתוח את הקישור, העתק את ה-"{href}" הזה אל Google</p>
                    <p style="font-size:18px;">בברכה,</p>
                    <h2>תקשוב פיקוד אכ"א</h2>
                    <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Logo-aka.png" width="150"/>
                </body>
                </html>        
            """
        try:
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em = EmailMessage()
            em['subject'] = subject
            em.set_content(body, subtype="html")
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:

                smtp.login(email_sender, email_password)
                response = smtp.sendmail(email_sender, email_receiver, em.as_string())
                if(response == {}):
                    return True
                else:
                    return False
        except:
            email_sender = "newonetrying@gmail.com"
            email_password = "ynqq fnmm dcdj hpxy"
            try:
                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em = EmailMessage()
                em['subject'] = subject
                em.set_content(body, subtype="html")
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    response = smtp.sendmail(email_sender, email_receiver, em.as_string())
                    if(response == {}):
                        return True
                    else:
                        return False
            except:
                email_sender = "t7192759@gmail.com"
                email_password = "gefv cvff ldjl mnil"
                try:
                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_receiver
                    em = EmailMessage()
                    em['subject'] = subject
                    em.set_content(body, subtype="html")
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        response = smtp.sendmail(email_sender, email_receiver, em.as_string())
                        if(response == {}):
                            return True
                        else:
                            return False
                except:
                    return "error"
    #type 2 = forgot password
    if type_variable == 2:
        token = to_send.get("token")
        href = f"http://localhost:5173/newpassword/{token}"
        subject = "איפוס סיסמה"
        body = f"""
            <!DOCtype_variable html>
                <html lang="he">
                <head>
                    <meta charset="UTF-8">
                    <title>Forgot password</title>
                </head>
                <body dir="rtl">
                    <h1>שלום רב, {name}</h1>
                    <p style="font-size:20px;">קיבלנו את בקשתך לאיפוס סיסמה</p>
                    <p style="font-size:20px;">נא ללחוץ על הקישור <a href={href}>{href}</a></p>
                    <br/>
                    <br/>
                    <br/>
                    <p style="font-size:18px;">בברכה,</p>
                    <h2>תקשוב פיקוד אכ"א</h2>
                    <div>
                        <br/>
                        <br/>
                        <br/>
                        <p style="font-size:13px;">אם אינך מצליח לפתוח את הקישור, העתק את ה-"{href}" הזה אל Google</p>
                        <div style="color:red; display: inline-block;">
                            <p style="font-size:15px; margin-right: 5px; margin-left: 5px;">אם לא ביקשת זאת, התעלם מהודעה זו</p>
                        </div>
                        <br/>
                        <div style="width: 100%;">
                            <br/>
                            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Logo-aka.png" width="150"/>
                        </div>
                    </div>
                </body>
                </html>        
            """
        try:
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em = EmailMessage()
            em['subject'] = subject
            em.set_content(body, subtype="html")
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                response = smtp.sendmail(email_sender, email_receiver, em.as_string())
                if(response == {}):
                    return True
                else:
                    return False
        except:
                email_sender = "t7192759@gmail.com"
                email_password = "gefv cvff ldjl mnil"
                try:
                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_receiver
                    em = EmailMessage()
                    em['subject'] = subject
                    em.set_content(body, subtype="html")
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        response = smtp.sendmail(email_sender, email_receiver, em.as_string())
                        if(response == {}):
                            return True
                        else:
                            return False
                except:
                    return "error"
    
    if type_variable == 3:
        name = to_send.get("name").title()
        href = f"http://localhost:5173/login"
        subject = "החשבון שלך אושר"
        body = f"""
            <!DOCtype_variable html>
                <html lang="he">
                <head>
                    <meta charset="UTF-8">
                    <title>Verification Email</title>
                </head>
                <body dir="rtl">
                    <h1>שלום רב, {name}</h1>
                    <p style="font-size:20px;">חשבונך אושר</p>
                    <p style="font-size:20px;">היכנס לקישור כדי להיכנס לחשבונך ותוכל להשתמש בדף שלנו, <a href="{href}">{href}</a></p>
                    <br/>
                    <br/>
                    <br/>
                    <p style="font-size:13px;">אם אינך מצליח לפתוח את הקישור, העתק את ה-"{href}" הזה אל Google</p>
                    <p style="font-size:18px;">בברכה,</p>
                    <h2>תקשוב פיקוד אכ"א</h2>
                    <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Logo-aka.png" width="150"/>
                </body>
                </html>        
            """
        try:
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em = EmailMessage()
            em['subject'] = subject
            em.set_content(body, subtype="html")
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                response = smtp.sendmail(email_sender, email_receiver, em.as_string())
                if(response == {}):
                    return True
                else:
                    return False
        except:
            email_sender = "newonetrying@gmail.com"
            email_password = "ynqq fnmm dcdj hpxy"
            try:
                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em = EmailMessage()
                em['subject'] = subject
                em.set_content(body, subtype="html")
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    response = smtp.sendmail(email_sender, email_receiver, em.as_string())
                    if(response == {}):
                        return True
                    else:
                        return False
            except:
                email_sender = "t7192759@gmail.com"
                email_password = "gefv cvff ldjl mnil"
                try:
                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_receiver
                    em = EmailMessage()
                    em['subject'] = subject
                    em.set_content(body, subtype="html")
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        response = smtp.sendmail(email_sender, email_receiver, em.as_string())
                        if(response == {}):
                            return True
                        else:
                            return False
                except:
                    return "error"
        

def token_validating(token_sent):
    #type_variable 1 = It has to have token, refresh and expiration valid (type_variable and expiration on time)
    type_variable = token_sent.get("type")
    if type_variable == 1 or type_variable == 2:
        validation = True
        if "token" in token_sent:
            validation = sends_validate({"token": token_sent.get("token")},["token"])
        if validation == True:
            if "refresh_token" in token_sent:
                validation = sends_validate({"refresh_token": token_sent.get("refresh_token")}, ["token", "refresh_token", "token_expiration"])
            if validation == True:
                if "token_expiration" in token_sent:    
                    expiration = token_sent.get("token_expiration")
                    validation = sends_validate({"token_expiration" : expiration}, ["token_expiration"])
                    if validation == True:
                        if expiration < datetime.now():
                            return "token_expiration"
        # type_variable 2 = sends to validate the token to the database
                if type_variable == 2:
                    validation = db_validating({"type": 4, "key": "token", "token": token_sent.get("token"), "id": token_sent.get("id")})
                    if type(validation) == dict:
                        expiration = validation.get("token_expiration")
                        if expiration < datetime.now():
                            refreshValidation = db_validating({"type": 4, "key": "refresh_token", "token": token_sent.get("refresh_token"), "id": token_sent.get("id")})
                            return refreshValidation
    return validation


def managingCors (response, request):
    try:
        if request.headers.get("Origin") != None:
            origin = request.headers.get("Origin")
            if origin == "http://localhost:5173":
                response.header = {"Access-Control-Allow-Origin": origin}
                return response.header
        else:
            return response
    except:
        return response