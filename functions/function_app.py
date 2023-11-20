import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="DataFunction", auth_level=func.AuthLevel.ANONYMOUS)
def DataFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Data Function encoutered a request')

    bad_request_response = func.HttpResponse(
        status_code=400, 
        body="DataFunction endpoint expects a json body of the form: " +
            "{'id':int,temp:int[8-15],'wind':int[15-25]," +
            "'humid':int[40-70],'CO2':int[500-1500]}"
    )

    # this function expects a json body 
    try:
        req_body = req.get_json()
    except ValueError:
        return bad_request_response
    else:
        try: # will fail on wrong type and missing attribute
            sensorId = int(req_body.get('id'))
            temp     = int(req_body.get('temp'))
            wind     = int(req_body.get('wind'))
            humid    = int(req_body.get('humid'))
            CO2      = int(req_body.get('CO2'))
        except TypeError:
            return bad_request_response

    # attempt to update the databse with this data
    database_unavailable_response = func.HttpResponse(
        body=f"Unable to reach databse",
        status_code=503
    )  
    if False: 
        return database_unavailable_response

    # success 
    success_response = func.HttpResponse(
        body=f"Sensor {sensorId}'s data was successfully " +
            "recorded in the database",
        status_code=200
    )
    return success_response