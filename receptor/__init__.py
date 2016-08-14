import logging as log
log.basicConfig(level=log.DEBUG)

from models import RawData, MessageBuffer
from receptor.microADSB import MicroADSB


from pyModeS import adsb


__running = False
__MAP_BUFFER = {}
__MICRO_ADSB = None


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
            log.info("Raw Message Received: %s" % rawData.frame)

            if not icao in __MAP_BUFFER:
                __MAP_BUFFER[icao] = MessageBuffer(icao=icao)

            __MAP_BUFFER[icao].addRawData(rawData)

            if __MAP_BUFFER[icao].isComplete():
                log.info("Complete Message Received: %s" % __MAP_BUFFER[icao])
                del __MAP_BUFFER[icao]

        else:
            log.info("Invalid Raw Message Received: %s" % rawData.frame)

def start():
    log.info("Starting receptor...")

    global __MICRO_ADSB
    __MICRO_ADSB = MicroADSB()
    __MICRO_ADSB.onOpen = onOpen
    __MICRO_ADSB.onClose = onClose
    __MICRO_ADSB.onMessage = onMessage
    __MICRO_ADSB.open()

    try:
        __running = True
        while __running:
            pass
    except:
        stop()

def stop():
    log.info("Stopping receptor...")
    __MICRO_ADSB.close()
    __MAP_BUFFER = None
