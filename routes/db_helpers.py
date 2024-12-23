from config.db import Session
from models.tables import attendees
from sqlalchemy import or_, select, and_
from schemas.attendee import Attendee
from sqlalchemy import func
import base64
import sqlalchemy
import datetime
import json

session = None

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
    global session
    if session is None:
        db_open_session()
    #Type 1 = mispar ishi or tehudat zehut in DB
    if type_function == 1:
        try:
            conditions = []
            if to_validate.get("mispar_ishi") is not None:
                conditions.append(attendees.c.mispar_ishi == to_validate["mispar_ishi"])
            if to_validate.get("tehudat_zehut") is not None:
                conditions.append(attendees.c.tehudat_zehut == to_validate["tehudat_zehut"])
            query = attendees.select().where(or_(*conditions))
            response_db = session.execute(query).fetchall()
            if response_db == []:
                return True
            return response_db[0]
        except:
            session.rollback()
            db_close_session()
            return "error"
    #Type 2 = id in database
    if type_function == 2:
        try:
            query = attendees.select().where(attendees.c.id == to_validate.get("id"))
            response_db = session.execute(query).fetchall()
            if response_db == []:
                return False
            return True
        except:
            session.rollback()
            db_close_session()
            return "error"

def db_deleting(to_delete):
    global session
    if session is None:
        db_open_session()
    id = to_delete.get("id")
    table = to_delete.get("table")
    try:
        query = table.delete().where(table.c.id == id)
        response = session.execute(query)
        if response.rowcount >= 1:
            session.commit()
            return True
        else:
            return False
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
            if response:
                if hasattr(response[0], '_asdict'):
                    return [row._asdict() for row in response]
                else:
                    # Access by column name (more robust)
                    column_names = response[0].keys()  # Get column names from the first row
                    result_list = []
                    for row in response:
                        row_dict = {}
                        for column in column_names:
                            row_dict[column] = getattr(row, column)
                        result_list.append(row_dict)
                    return result_list
            else:
                return []
            if isinstance(response, list):
                return [row.__dict__ for row in response] # Or row._asdict() if available
            # If it's a single Row
            else:
                return response.__dict__ # Or result._asdict() if available
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
    