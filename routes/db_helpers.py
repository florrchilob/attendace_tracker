from config.db import Session
from models.tables import sub_accounts, meetings, admin_accounts_x_licenses, licenses, admin_accounts
from sqlalchemy import or_, select, and_
from schemas.sub_account import SubAccount
from routes.accounts_manage_functions import token_decode
from schemas.meetingReceived import MeetingReceived
from schemas.meetingBD import MeetingBD
from schemas.admin_account_x_license import AdminAccountXLicense
from sqlalchemy import func
import base64
import sqlalchemy
import datetime
import json

session = None
    
def get_all_licenses(new_meeting: MeetingReceived):
    global session
    if session is None:
        db_open_session()
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
    all_licenses = session.execute(query).fetchall()
    licenses_to_return = []
    for license in all_licenses:
        new_license = AdminAccountXLicense(id = license.id, license_id = license.license_id, admin_account_id = license.admin_account_id, amount_licenses =  license.amount_licenses)
        licenses_to_return.append(new_license)
    return licenses_to_return

def get_same_hours(new_meeting: MeetingReceived):
    global session
    if session is None:
        db_open_session()
    try:
        query = meetings.select().filter(meetings.c.day == new_meeting.day)
        same_day = session.execute(query).fetchall()
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

def db_open_session():
    global session
    if session is None:
        session = Session() 

def db_close_session():
    global session
    if session:
        session.close()


def db_validating(to_validate, testing = None):
    type_function = to_validate.get("type")
    #Type 1 = mispar ishi or email not on DB already
    global session
    if session is None:
        db_open_session()
    if type_function == 1:
        try:
            query = sub_accounts.select().filter(or_(sub_accounts.c.mail == to_validate.get("mail"),sub_accounts.c.mispar_ishi == to_validate.get("mispar_ishi")))
            response_db = session.execute(query).fetchall()
            if response_db == []:
                return True
            return False
        except:
            session.rollback()
            db_close_session()
            return "error"
    #Type 2 = checking that email is already in the database, not validated and with an existing valid token
    #Type 3 = checking that multiple values are in the database and match eachother       
    #Type 5 = checking that email is already in the database and validated
    if type_function == 2 or type_function == 3 or type_function == 5:
        conditionals = to_validate.get("conditionals")
        try:
            conditions = []
            for key, value in conditionals.items():
                column = getattr(sub_accounts.c, key)
                if isinstance(value, list):
                    conditions.append(column.in_(value))
                else:
                    conditions.append(column == value)
            query = sub_accounts.select().where(and_(*conditions))
            response_db = session.execute(query)
            values = response_db.fetchall()
        except:
            session.rollback()
            return "error"
        if values == []:
            return False
        if type_function != 5:
            account_returned = SubAccount()
            try:
                account_returned.create_straight(dict(values[0]))
            except:
                keys = response_db.keys()
                valuesDict = [dict(zip(keys, row)) for row in values]
                account_returned.create_straight(valuesDict[0])
            if type_function == 2:
                if account_returned.validated == True:
                    return "validated"
            return account_returned

        else:       
            accounts_returned = []
            invalid_accounts = []
            try:
                for value in values:
                    if value != None and value != "":
                        account_returned = SubAccount()
                        value_dict = dict(zip(response_db.keys(), value))
                        account_returned.create_straight(value_dict)
                        if account_returned.validated == False and testing != "ok":
                            invalid_accounts.append(account_returned.id)
                        else:
                            accounts_returned.append(account_returned)
                        account_returned = None
            except:
                keys = response_db.keys()
                valuesDict = [dict(zip(keys, row)) for row in values]
                for value in valuesDict:
                    account_returned = SubAccount()
                    value_dict = dict(zip(response_db.keys(), value))
                    account_returned.create_straight(value_dict)
                    accounts_returned.append(account_returned.id)
                    if account_returned.validated == False and testing != "ok":
                            invalid_accounts.append(account_returned)
                    else:
                        accounts_returned.append(account_returned)
                    account_returned = None
            return accounts_returned, invalid_accounts
    #Type 4 = checking that the token and the account id match
    if type_function == 4:
        key = to_validate.get("key")
        token = to_validate.get("token")
        id = to_validate.get("id")
        try:
            query = sub_accounts.select().where((sub_accounts.c.id == id))
            response = session.execute(query)
            data = response.fetchall()
        except:
            session.rollback()
            return "error"
        if len(data) < 1:
            return False
        account = data[0]
        column_names = ["id", "mail", "password", "name", "mispar_ishi", "telephone", "account_type", "validated", "authorized", "token", "refresh_token", "token_expiration"]
        account = dict(zip(column_names, account))
        if key == "token":
            if account.get("token") == None:
                return "no_needed"
            if account.get("token") != token:
                return False
            else:
                return account
        elif key == "refresh_token":
            if account.get("refresh_token") == token:
                return("renovate_token")   
            else:
                return("wrong_token")
            
    # Type 6 = checking that the account is validated and authorized 
    if type_function == 6:
        conditionals = to_validate.get("conditionals")
        conditions = [getattr(sub_accounts.c, key) == value for key, value in conditionals.items()]
        try:
            query = sub_accounts.select().where(and_(*conditions))
            response_db = session.execute(query).fetchall()
            if len(response_db) < 1:
                return False
            account = response_db[0]
            if account.validated == False:
                return "validated"
            if account.authorized == False:
                return "authorized"
            if "type_needed" in to_validate:
                if account.account_type < to_validate["type_needed"]:
                    return "wrong_type"
            return True
        except:
            session.rollback()
            return "error"

def db_saving(to_save, table, testing = None):
    global session
    if session is None:
        db_open_session()
    try:
        query = table.insert().values(**to_save.__dict__)
        response = session.execute(query)
        if response.rowcount >= 1:
            session.commit()
            if testing == "id":
                return response.lastrowid
            return True
        return False
    except:
        session.rollback()
        return "error"

def db_getting(to_get):
    type = to_get.get("type")
    #Type 1 = get all from table
    global session
    if session is None:
        db_open_session()
    if type == 1:
        try:
            table = to_get.get("table")
            query = table.select()
            response = session.execute(query).fetchall()
            return response 
        except:
            return "error"
    
    #Type 2 = get values from table where conditions
    if type == 2:
        table = to_get.get("table")
        values_list = to_get.get("values")
        values = [getattr(table.c, key) for key in values_list]
        conditionals = to_get.get("conditionals")
        conditions = [getattr(table.c, key) == value for key, value in conditionals.items()]
        try:
            query = select(*values).where(and_(*conditions))
            response = session.execute(query)
            data = response.fetchall()
            if data == []:
                return False
            return data
        except:
            return "error"
        
    # Type 3 = get values from table where includes value
    if type == 3:
        table = to_get.get("table")
        values_list = to_get.get("values")
        values = [getattr(table.c, key) for key in values_list]
        conditionals = to_get.get("conditionals")
        conditions = [func.lower(getattr(table.c, key)).like(func.lower(f"%{value}%")) 
                      for cond in conditionals for key, value in cond.items()]        
        try:
            query = select(*values).where(and_(*conditions))
            response = session.execute(query)
            data = response.fetchall()
            if data == []:
                return False
            return data
        except:
            return "error"

def db_updating(to_update):
    #Type 1 = regular update
    global session
    if session is None:
        db_open_session()
    if to_update.get("type") == 1:
        table = to_update.get("table")
        conditionals = to_update.get("conditionals")
        conditions = []
        for key, value in conditionals.items():
                column = getattr(table.c, key)
                if isinstance(value, list):
                    conditions.append(column.in_(value))
                else:
                    conditions.append(column == value)
        values = to_update.get("values")
        try:
            query = table.update().where(and_(*conditions)).values(**values)
            response = session.execute(query)
            if response.rowcount >= 1:
                session.commit()
                return True
            return False
        except:
            session.rollback()
            return "error"
    # Type 2 = eliminates token from a user knowing the mail   
    if to_update.get("type") == 2:
        try:
            query = table.update().where(table.c.mail == to_update.get("mail")).values(token = None)
            response = session.execute(query)
            if response.rowcount == 1:
                session.commit()
                return True
        except:
            session.rollback()
            return False
    return {"ok"}
    