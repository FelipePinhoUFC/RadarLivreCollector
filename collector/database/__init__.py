import os
import sys
from collector import report
import sqlite3 as sql
import time

from config import DATABASE_DIR
from collector.adsb.decoder import HalfObservation

DATABASE_FILE = "local_database.db"
DATABASE_FILE_NAME = os.path.join(DATABASE_DIR, DATABASE_FILE)

def setupDatabaseDir():
    
    # Create the database dir if not exists
    if not os.path.exists(DATABASE_DIR):

        os.makedirs(DATABASE_DIR)

def executeQuery(query, databaseIndex = 0):

    result = None

    setupDatabaseDir()

    con = None

    try:

        con = sql.connect(DATABASE_FILE_NAME + "_" + str(databaseIndex))

        try:

            cur = con.cursor()
            cur.execute(query)
            con.commit()
            result = cur.fetchall()
            cur.close()

        except sql.OperationalError, msg:

            report.error("Can't execute query: " + str(msg))

    except sql.Error, e:

        report.error("Can't connect to local database: " + str(e))

    finally:
    
        if con:

            con.close()

    return result

def init():

    report.info("Opening local database")

    # Create the database dir if not exists
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)

    executeQuery("CREATE TABLE IF NOT EXISTS ADSB_MESSAGE (MESSAGE TEXT, _TIMESTAMP BIGINT)")
    executeQuery("CREATE TABLE IF NOT EXISTS HALF_OBSERVATION (" + \
        "AIRPLANE TEXT," + \
        "CALLSIGN TEXT," + \
        \
        "LATITUDE_COLLECTOR DECIMAL(20, 10), " + \
        "LONGITUDE_COLLECTOR DECIMAL(20, 10), " + \
        \
        "LATITUDE_EVEN DECIMAL(20, 10), " + \
        "LONGITUDE_EVEN DECIMAL(20, 10), " + \
        \
        "LATITUDE_ODD DECIMAL(20, 10), " + \
        "LONGITUDE_ODD DECIMAL(20, 10), " + \
        \
        "ALTITUDE INTEGER, " + \
        \
        "VERTICAL_VELOCITY INTEGER, " + \
        "HORIZONTAL_VELOCITY INTEGER, " + \
        \
        "ANGLE INTEGER, " + \
        \
        "_TIMESTAMP BIGINT, " + \
        \
        "MESSAGE_DATA_ID TEXT, " + \
        "MESSAGE_DATA_POSITION_EVEN TEXT, " + \
        "MESSAGE_DATA_POSITION_ODD TEXT, " + \
        "MESSAGE_DATA_VELOCITY TEXT, " + \
        \
        "LAST_RECEIVED TEXT, " + \
        "EVEN_RECEIVED INTEGER, " + \
        "ODD_RECEIVED INTEGER, " + \
        "VELOCITY_RECEIVED INTEGER, " + \
        "ID_RECEIVED INTEGER "\
        ")"
    , 1)
    
    

def save(data):

    report.info("Saving data received")

    executeQuery("INSERT INTO ADSB_MESSAGE (MESSAGE, _TIMESTAMP) VALUES('" + data + "', '" + str(time.time()) + "')")


def getAll():
    return executeQuery("SELECT * FROM ADSB_MESSAGE ORDER BY _TIMESTAMP")

def removeByTimestamp(timestamp):
    executeQuery("DELETE FROM ADSB_MESSAGE WHERE _TIMESTAMP = " + str(timestamp))


def halfObservationFrom(data):
    obs = HalfObservation()
    obs.airplane = data[0]
    obs.flight = data[1]
    obs.latitudeCollector = data[2]
    obs.longitudeCollector = data[3]
    obs.latitudeEven = data[4]
    obs.longitudeEven = data[5]
    obs.latitudeOdd = data[6]
    obs.longitudeOdd = data[7]
    obs.altitude = data[8]
    obs.verticalVelocity = data[9]
    obs.horizontalVelocity = data[10]
    obs.groundTrackHeading = data[11]
    obs.timestamp = data[12]
    obs.messageDataId = data[13]
    obs.messageDataPositionEven = data[14]
    obs.messageDataPositionOdd = data[15]
    obs.messageDataVelocity = data[16]
    obs.lastReceived = data[17]
    obs.evenReceived = data[18] == 1
    obs.oddReceived = data[19] == 1
    obs.velocityReceived = data[20] == 1
    obs.identityReceived = data[21] == 1

    return obs

def deleteHalfObservation(airplane):
    executeQuery("DELETE FROM HALF_OBSERVATION WHERE AIRPLANE = '" + airplane + "'", 1)

def getHalfObservation(airplane):
    results = executeQuery("SELECT * FROM HALF_OBSERVATION WHERE AIRPLANE = '" + airplane + "'", 1)

    if results and len(results) > 0:

        return halfObservationFrom(results[0])

    return None

def getAllHalfObservetions():
    results = executeQuery("SELECT * FROM HALF_OBSERVATION", 1)

    if results:

        observations = []
        for r in results:
            obs = halfObservationFrom(r)
            if obs:
                observations.append(obs)

        return observations

    return None


def saveHalfObservation(obs):
    if obs:
        halfObservation = getHalfObservation(obs.airplane)

        if halfObservation:
            halfObservation.update(obs)
            deleteHalfObservation(halfObservation.airplane)
            saveHalfObservation(halfObservation)

            return halfObservation

        elif not obs.airplane == "":

            executeQuery("INSERT INTO HALF_OBSERVATION VALUES(" + \
                "'" + obs.airplane + "', " + \
                "'" + obs.flight + "', " + \
                \
                str(obs.latitudeCollector) + ", " + \
                str(obs.longitudeCollector) + ", " + \
                \
                str(obs.latitudeEven) + ", " + \
                str(obs.longitudeEven) + ", " + \
                \
                str(obs.latitudeOdd) + ", " + \
                str(obs.longitudeOdd) + ", " + \
                \
                str(obs.altitude) + ", " + \
                \
                str(obs.verticalVelocity) + ", " + \
                str(obs.horizontalVelocity) + ", " + \
                \
                str(obs.groundTrackHeading) + ", " + \
                \
                str(obs.timestamp) + ", " + \
                \
                "'" + obs.messageDataId + "', " + \
                "'" + obs.messageDataPositionEven + "', " + \
                "'" + obs.messageDataPositionOdd + "', " + \
                "'" + obs.messageDataVelocity + "', " + \
                \
                "'" + obs.lastReceived + "', " + \
                ("1" if obs.evenReceived else "0") + ", " + \
                ("1" if obs.oddReceived else "0") + ", " + \
                ("1" if obs.velocityReceived else "0") + ", " + \
                ("1" if obs.identityReceived else "0") +  \
                \
                ")"
            , 1)

            return obs

    return None    
    

