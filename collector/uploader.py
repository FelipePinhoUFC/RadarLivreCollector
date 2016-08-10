import json
import os
import time

from adsb import decoder
from collector import report
from collector.adsb.decoder import LAST_ERROR
from collector.webapi import sendObservation
from config import SERVER_IP, MAX_MESSAGE_AGE, LOGIN, PASSWORD, LATITUDE, LONGITUDE
import requests
import webapi
import database as db

def sendMessageToServer(message):

    host = "http://" + SERVER_IP + "/api/"

    halfObservation = decoder.decodeMessage(message)
    halfObservation = db.saveHalfObservation(halfObservation)

    if halfObservation and halfObservation.isComplete():

        observation = decoder.fromHalfObservation(halfObservation)

        if observation:
            observation.timestampSent = time.time() * 1000

            data = observation.serialize()

            host += "observation/"

            if sendObservation(data):

                db.deleteHalfObservation(halfObservation.airplane)
                report.info("Collected info sent to server")
                return True

        else:
            report.log("erro ao decodificar halfObservation: " + str(LAST_ERROR["error"]))


    return False


def start(arg1, stopEvent):

    helloInterval = 0
    while not stopEvent.isSet():

        time.sleep(1)

        if helloInterval == 0:
            webapi.sendHello()
        helloInterval += 1
        helloInterval %= 60

        rawMessages = db.getAll()

        if not rawMessages:

            # Nothing to sent
            pass

        elif len(rawMessages) == 0:

            # Nothing to sent
            pass

        else:

            MIN_TIMESTAMP = time.time() - float(MAX_MESSAGE_AGE/1000)

            for m in rawMessages:

                timestamp = m[1]

                if timestamp < MIN_TIMESTAMP:

                    # report.info("Deleting message bacause is old.")
                    db.removeByTimestamp(timestamp)

                else:

                    data = m[0]
                    
                    message = {
                        "latitude": str(LATITUDE),
                        "longitude": str(LONGITUDE),
                        "data": str(data), 
                    }

                    if sendMessageToServer(message):
                        db.removeByTimestamp(timestamp)



