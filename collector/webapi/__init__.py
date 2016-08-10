from collector import report
from config import LOGIN, PASSWORD, COLLECTOR_ID, SERVER_IP
import requests
import json

_URL_SERVER_COLLECTOR = "collector/"
_URL_SERVER_OBSERVATION = "observation/"

_AUTH = (LOGIN, PASSWORD)

def sendHello():

    # report.log("Sending Hello!")
    response = None
    
    try:
        
        host = "http://" + SERVER_IP + "/api/collector/" + COLLECTOR_ID + "/"
        data = {
            "id": COLLECTOR_ID
        }

        response = requests.put(host, data=data, auth=_AUTH)

        if response.status_code >= 400:
            report.log(str(response.status_code) + " - " + json.dumps(response.json()))
        #report.log(str(response.status_code) + " - " + json.dumps(data))


    except Exception as e:
        report.error("Error while send hello!")
        if response:
            report.log(str(response.status_code) + " - " + json.dumps(response.json()))


def sendObservation(data):
    response = None

    try:

        host = "http://" + SERVER_IP + "/api/adsb_info/"
        response = requests.post(host, data=data, auth=_AUTH)

        if response.status_code >= 400:
            report.log(str(response.status_code) + " - " + json.dumps(response.json()))
        #report.log(str(response.status_code) + " - " + json.dumps(data))

        return True

    except Exception as e:
        report.error("Error while send halfObservation!")
        if response:
            report.log(str(response.status_code) + " - " + json.dumps(response.json()))

    return False