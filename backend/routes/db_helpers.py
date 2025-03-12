from config.db import Session
from models.tables import attendees
from sqlalchemy import or_, select, and_, case, cast, Integer
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

async def db_validating(to_validate, testing = None):
    type_function = to_validate.get("type")
    async with Session() as session:
        async with session.begin():        
            #Type 1 = mispar ishi or tehudat zehut in DB
            if type_function == 1:
                try:
                    conditions = []
                    if to_validate.get("mispar_ishi") is not None:
                        conditions.append(attendees.c.mispar_ishi == to_validate["mispar_ishi"])
                    if to_validate.get("tehudat_zehut") is not None:
                        conditions.append(attendees.c.tehudat_zehut == to_validate["tehudat_zehut"])
                    query = attendees.select().where(or_(*conditions))
                    response_db = await session.execute(query)
                    data = response_db.fetchall()
                    if data == []:
                        return True
                    return data[0]
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
                    return "error"
            #Type 2 = id in database return true if exists
            #Type 3 = id in database return attendee
            
            if type_function == 2 or type_function == 3:
                try:
                    query = attendees.select().where(attendees.c.id == to_validate.get("id"))
                    response_db = await session.execute(query)
                    data = response_db.fetchall()
                    if data == []:
                        return False
                    if type_function == 2:
                        return True
                    return data[0]
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
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
                    response_db = await session.execute(query)
                    existing_records = response_db.fetchall()
                    existing_values = {getattr(record, column_name) for record in existing_records}
                    missing_values = set(values_list) - existing_values
                    return {
                        "existing_values": existing_values,
                        "missing_values": missing_values
                    }
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
                    return "error"

async def db_deleting(to_delete):
    type_delete = to_delete.get("type")
    async with Session() as session: 
        async with session.begin():        
            table = to_delete.get("table")
            if type_delete == 1:
                try:
                    query = table.delete()
                    response = await session.execute(query)
                    if response.rowcount >= 1:
                        await session.commit()
                        return True
                    else:
                        return False
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
                    return "error"
            else:
                id_to_delete = to_delete.get("id")
                try:
                    query = table.delete().where(table.c.id == id_to_delete)
                    response = await session.execute(query)
                    if response.rowcount >= 1:
                        await session.commit()
                        return True
                    else:
                        return False
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
                    return "error"

async def db_saving(to_save, table, testing = None):
    async with Session() as session: 
        async with session.begin():        
            try:
                query = table.insert().values(**to_save.__dict__)
                response = await session.execute(query)
                if response.rowcount >= 1:
                    await session.commit()
                    return response.lastrowid
                return False
            except Exception as e:
                print(f"Bulk save error: {str(e)}")
                return "error"

async def db_getting(to_get):
    type = to_get.get("type")
    #Type 1 = get all from table
    async with Session() as session: 
        async with session.begin():        
            if type == 1:
                try:
                    table = to_get.get("table")
                    query = table.select()
                    response = await session.execute(query)
                    data = response.fetchall()
                    result_list = []
                    if data:
                        for row in data:
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
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
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
                    response = await session.execute(query)
                    data = response.fetchall()
                    if data == []:
                        return False
                    return data
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
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
                    response = await session.execute(query)
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
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
                    return "error"
            
            # Type 4 = get total amount of rows and rows that did not arrived
            if type == 4:
                table = attendees
                query = select(
                    func.count(table.c.id).label("total_amount"),  
                    cast(func.sum(case((table.c.arrived == True, 0), else_=1)), Integer).label("not_arrived")
                )
                response = await session.execute(query)
                data = response.fetchone()
                try:
                    return data
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
                    return "error"

async def db_updating(to_update):
    #Type 1 = regular update
    async with Session() as session: 
        async with session.begin():        
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
                    response = await session.execute(query)
                    if response.rowcount >= 1:
                        await session.commit()
                        return True
                    return False
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
                    return "error"
            # Type 2 = restart attendace all attendees
            if to_update.get("type") == 2:
                try:
                    query = attendees.update().values(arrived = False, date_arrived = None)
                    response = await session.execute(query)
                    return True
                except Exception as e:
                    print(f"Bulk save error: {str(e)}")
                    return "error"
            return {"ok"}

async def db_bulk_saving(to_save_list, table, testing = None):
    async with Session() as session: 
        async with session.begin():        
            try:
                values = [attendee.__dict__ for attendee in to_save_list]
                await session.execute(table.insert(), values)
                await session.commit()
                return True
            except Exception as e:
                print(f"Bulk save error: {str(e)}")
                return "error"
    