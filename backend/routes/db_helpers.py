from config.db import Session
from models.tables import attendees
from sqlalchemy import or_, select, and_
from sqlalchemy import func
from datetime import datetime
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
    #Type 2 = id in database return true if exists
    #Type 3 = id in database return attendee

    if type_function == 2 or type_function == 3:
        try:
            query = attendees.select().where(attendees.c.id == to_validate.get("id"))
            response_db = session.execute(query).fetchall()
            if response_db == []:
                return False
            if type_function == 2:
                return True
            return response_db[0]
        except:
            session.rollback()
            db_close_session()
            return "error"
    # Type 4 = check if values exist in specified column
    if type_function == 4:
        try:
            column_name = to_validate.get("column_name")
            values_list = to_validate.get("values_list")
            if not column_name or not values_list:
                return "error"
            column = getattr(attendees.c, column_name)
            query = attendees.select().filter(column.in_(values_list))
            existing_records = session.execute(query).fetchall()
            existing_values = {getattr(record, column_name) for record in existing_records}
            missing_values = set(values_list) - existing_values
            return {
                "existing_values": existing_values,
                "missing_values": missing_values
            }
        except:
            session.rollback()
            db_close_session()
            return "error"

def db_deleting(to_delete):
    type_delete = to_delete.get("type")
    global session
    if session is None:
        db_open_session()
    table = to_delete.get("table")
    if type_delete == 1:
        try:
            query = table.delete()
            response = session.execute(query)
            if response.rowcount >= 1:
                session.commit()
                return True
            else:
                return False
        except: 
            session.rollback()
            return "error"
    else:
        id_to_delete = to_delete.get("id")
        try:
            query = table.delete().where(table.c.id == id_to_delete)
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
            return response.lastrowid
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
            result_list = []
            if response:
                for row in response:
                    if hasattr(row, "_asdict"):
                        row_dict = row._asdict() 
                    else:
                        column_names = row.keys()
                        row_dict = {column: getattr(row, column) for column in column_names}
                    for key, value in row_dict.items():
                        if isinstance(value, datetime): 
                            row_dict[key] = value.isoformat()
                    result_list.append(row_dict)

            return result_list
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
        table = attendees
        values_list = to_get.get("values")
        values = [getattr(table.c, key) for key in values_list]
        conditionals = to_get.get("conditionals")
        conditions = [func.lower(getattr(table.c, key)).like(func.lower(f"%{value}%")) 
                      for cond in conditionals for key, value in cond.items()]   
        try:
            query = select(*values).where(and_(*conditions))
            response = session.execute(query)
            data = response.fetchall()
            data_array = []
            for row in data:
                    if hasattr(row, "_asdict"):
                        row_dict = row._asdict() 
                    else:
                        column_names = row.keys()
                        row_dict = {column: getattr(row, column) for column in column_names}
                    for key, value in row_dict.items():
                        if isinstance(value, datetime): 
                            row_dict[key] = value.isoformat()
                    data_array.append(row_dict)
            if data == []:
                return False
            return data_array
        except:
            return "error"

def db_updating(to_update):
    #Type 1 = regular update
    global session
    if session is None:
        db_open_session()
    if to_update.get("type") == 1:
        table = attendees
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
    # Type 2 = restart attendace all attendees
    if to_update.get("type") == 2:
        try:
            query = attendees.update().values(arrived = False, date_arrived = None)
            response = session.execute(query)
            return True
        except:
            session.rollback()
            return "error"
    return {"ok"}

def db_bulk_saving(to_save_list, table, testing = None):
    global session
    if session is None:
        db_open_session()
    try:
        values = [attendee.__dict__ for attendee in to_save_list]
        result = session.execute(table.insert(), values)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Bulk save error: {str(e)}")
        return "error"
    finally:
        db_close_session()
    