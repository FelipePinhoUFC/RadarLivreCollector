import sys
import datetime
import time
import serial
import json
import os
from collector import report
from collector import database as db

from config import COLLECTOR_ADDRESS

def getCollector():

    report.info("Connecting to collector " + COLLECTOR_ADDRESS)

    conn = None
    try:

        conn = serial.Serial(COLLECTOR_ADDRESS, 115200, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, xonxoff=False, rtscts=False, dsrdtr=False, timeout=5)
        return conn

    except Exception as ex:

        report.error("Can't connect to receptor: " + str(ex))
        if conn:
            conn.close()

        

    return None
        

def start(arg1, stopEvent):

    report.log("Starting receptor... ")

    #report.log("Getting collector version...")
    #s_com.write("#00\r\n")
    #k = s_com.readline()  
    # report.info("Receptor version: \n" + str(k))

    #report.log("Start receiving mode...")
    #s_com.write("#43-02\r\n")
    #k = s_com.readline()
    # report.info("Initializing data receiving: \n" + str(k))\

    messageCounter = 0

    # msgs = open("msg.txt", "r").read().split("\n")
    # index = 0

    conn = None

    while not stopEvent.isSet():

        if not conn:
            conn = getCollector()

        if conn:

            line = ""

            try:
                line = conn.readline()
            except Exception as e:
                if conn:
                    conn.close()
                conn = None
                report.log("Receptor disconnected!")

            # line = msgs[index]
            # index += 1
            # line = ""

            if line and len(line) >= 28:

                line = line[14:][:-2]
                db.save(line)  
                
                report.info("New data received: \"" + line + "\" with length " + str(len(line)))
        
            else:

                report.log("Skipping...")

            messageCounter += 1

            if messageCounter >= 50:

                report.info("Clearing collector...")
                messageCounter = 0
                conn.flush()

            time.sleep(.5)

        else:
            report.error("Reconnecting with receptor...")
            time.sleep(5)

    report.log("Stopping receptor...")