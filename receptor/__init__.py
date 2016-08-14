import logging as log

from network.dataInput import DataInput

log.basicConfig(level=log.DEBUG)

from network.dataUploader import DataUploader


from config import DATA_OUTPUT_ENABLED, DATA_OUTPUT_HOST, DATA_OUTPUT_PORT, DATA_INPUT_HOST, DATA_INPUT_PORT, \
    DATA_INPUT_ENABLED, SERVER_HOST
from network.dataOutput import DataOutput


from models import RawData, MessageBuffer, ADSBInfo
from receptor.microADSB import MicroADSB


from pyModeS import adsb


__running = False
__RAW_BUFFER = {}
__DATA_UPLOADER = DataUploader(serverHost=SERVER_HOST)
__MICRO_ADSB = MicroADSB()
__DATA_OUTPUT = DataOutput(DATA_OUTPUT_HOST, DATA_OUTPUT_PORT)
__DATA_INPUT = DataInput(DATA_INPUT_HOST, DATA_INPUT_PORT)


def onOpen(err):
    if err:
        log.error("Receptor open: %s" % str(err))
    else:
        log.info("Receptor open: opened!")


def onClose(err):
    if err:
        log.error("Receptor close: %s" % str(err))
    else:
        log.info("Receptor close: closed!")


def onMessage(data):
    if data:
        rawData = RawData(data)

        if rawData.downlinkformat == 17:
            icao = adsb.icao(rawData.frame[1:29])
            log.info("Raw Message Received: %s" % str(rawData.frame))

            __DATA_OUTPUT.addData(rawData.frame)

            if not icao in __RAW_BUFFER:
                __RAW_BUFFER[icao] = MessageBuffer(icao=icao)

            __RAW_BUFFER[icao].addRawData(rawData)

            if __RAW_BUFFER[icao].isComplete():
                adsbInfo = ADSBInfo.createFromMessageBuffer(__RAW_BUFFER[icao])
                __DATA_UPLOADER.addADSBInfo(adsbInfo)
                log.info("Complete Message Received: %s" % str(__RAW_BUFFER[icao]))

        else:
            log.info("Invalid Raw Message Received: %s" % str(rawData.frame))


def onADSBInfo(info):
    __DATA_UPLOADER.addADSBInfo(info)
    # log.info("Complete Message Received from ADSBHub.com: %s" % str(info))


def start():
    log.info("Starting receptor...")

    global __MICRO_ADSB
    __MICRO_ADSB.onOpen = onOpen
    __MICRO_ADSB.onClose = onClose
    __MICRO_ADSB.onMessage = onMessage
    __MICRO_ADSB.open()

    global __DATA_UPLOADER
    __DATA_UPLOADER.start()

    if DATA_OUTPUT_ENABLED:
        global __DATA_OUTPUT
        __DATA_OUTPUT.start()

    if DATA_INPUT_ENABLED:
        global __DATA_INPUT
        __DATA_INPUT.onADSBInfoReceived = onADSBInfo
        __DATA_INPUT.connect()

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
    __DATA_UPLOADER.stop()
    __DATA_OUTPUT.stop()
    __DATA_INPUT.disconnect()
    __MAP_BUFFER = None
