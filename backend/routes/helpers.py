#Imports
from datetime import datetime
from fastapi.responses import JSONResponse

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
        case 5:
            message = "Date not valid"
        case 6:
            message = "Filter not valid"
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
        case 102:
            message = "ID not valid"
        case 104:
            message = "No matches to your search"
        case 8000: 
            message ="Test"
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


#Sends every value to validate
def sends_validate(to_validate, values):
    if type(to_validate) == dict:
        to_validate = to_validate.items()
    for key, value in to_validate:
        if key in values:
            validation = True
            validation = validating(key, value, type(value))
            if validation != True:
                if type(validation) == tuple:
                    return (validation[0], validation[1])
                return validation
    return True

#Validates all the necessary values
def validating(key, value, type_variable):
    match key:
        case "full_name":
            if value == None:
                return (400, 1)
            if len(value)>254:
                return (400, 1)
            if len(value) > 255:
                return (400, 1)
        case "mispar_ishi":
            if value == None:
                return (400, 3)
            if type_variable == str:
                if not value.isdigit():
                    return (400, 3)
                if len(value) < 6:
                    return(400, 3)
                if value[0] == "0":
                    return(400, 3)
            else:
                if len(str(value)) < 6:
                    return (400, 3)
        case "tehudat_zehut":
            if value == None:
                return (400, 4)
            if type_variable == str:
                if not value.isdigit():
                    return (400, 4)
                if len(value) != 9:
                    return(400, 4)
            else:
                if len(str(value)) != 9:
                    return (400, 4)
        case "arrived":
            if type_variable != bool:
                return (400, 101)
        case "id":
            if type_variable != int:
                return (400, 102)
            if value < 0:
                return (400, 102)
        case "date_arrived":
            if value == None:
                return (400, 5)
            if type_variable != str:
                return (400, 5)
            if "-" not in value:
                return (400, 5)
            if ":" not in value:
                (400, 5)
            try:
                datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except:    
                return (400, 5)
        case "filter":
            if value == None:
                return (400, 6)
            if type_variable != str:
                return (400, 6)
            if value not in ["id", "name", "full_name", "mispar_ishi", "tehudat_zehut"]:
                return (400, 6)
        case "value":
            if value == None:
                return (400, 6)
            if len(value) < 3:
                return (400, 6)
    return True