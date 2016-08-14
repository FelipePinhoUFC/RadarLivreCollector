import logging as log
log.basicConfig(level=log.DEBUG)

from config import DATA_OUTPUT_ENABLED, DATA_OUTPUT_HOST, DATA_OUTPUT_PORT
from network.dataOutput import DataOutput


from models import RawData, MessageBuffer
from receptor.microADSB import MicroADSB


from pyModeS import adsb


__running = False
__MAP_BUFFER = {}
__MICRO_ADSB = MicroADSB()
__DATA_OUTPUT = DataOutput(DATA_OUTPUT_HOST, DATA_OUTPUT_PORT)


def onOpen(err):
    if err:
        log.error("Receptor open: %s" % str(err))
    else:
        log.error("Receptor open: opened!")


def onClose(err):
    if err:
        log.error("Receptor close: %s" % str(err))
    else:
        log.error("Receptor close: closed!")


def onMessage(data):
    if data:
        rawData = RawData(data)

        if rawData.downlinkformat == 17:
            icao = adsb.icao(rawData.frame[1:29])
            log.info("Raw Message Received: %s" % str(rawData.frame))

            __DATA_OUTPUT.addData(rawData.frame)

            if not icao in __MAP_BUFFER:
                __MAP_BUFFER[icao] = MessageBuffer(icao=icao)

            __MAP_BUFFER[icao].addRawData(rawData)

            if __MAP_BUFFER[icao].isComplete():
                log.info("Complete Message Received: %s" % str(__MAP_BUFFER[icao]))
                del __MAP_BUFFER[icao]

        else:
            log.info("Invalid Raw Message Received: %s" % str(rawData.frame))

def start():
    log.info("Starting receptor...")

    global __MICRO_ADSB
    __MICRO_ADSB.onOpen = onOpen
    __MICRO_ADSB.onClose = onClose
    __MICRO_ADSB.onMessage = onMessage
    __MICRO_ADSB.open()

    if DATA_OUTPUT_ENABLED:
        global __DATA_OUTPUT
        __DATA_OUTPUT.start()

    try:
        __running = True
        while __running:
            pass
    except:
        __stop()

def stop():
    __running = False


def __stop():
    log.info("Stopping receptor...")
    __MICRO_ADSB.close()
    __DATA_OUTPUT.stop()
    __MAP_BUFFER = None
