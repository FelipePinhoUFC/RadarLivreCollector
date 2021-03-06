import logging.handlers
import os

from network.dataUploader import DataUploader


from receptor.rootConfig import DATA_OUTPUT_ENABLED, DATA_OUTPUT_HOST, DATA_OUTPUT_PORT, SERVER_HOST, LOG_DIR
from network.dataOutput import DataOutput


from models import RawData, MessageBuffer, ADSBInfo
from receptor.microADSB import MicroADSB


from pyModeS import adsb

log = logging.getLogger("receptor")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.handlers.RotatingFileHandler(
    os.path.join(LOG_DIR, "receptor.log"), maxBytes=4294967296, backupCount=6)
handler.setFormatter(formatter)
log.addHandler(handler)

__running = False
__RAW_BUFFER = {}
__DATA_UPLOADER = DataUploader(serverHost=SERVER_HOST)
__MICRO_ADSB = MicroADSB(autoReconnect=True)
__DATA_OUTPUT = DataOutput(DATA_OUTPUT_HOST, DATA_OUTPUT_PORT)


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


def onErr(err):
    if err:
        log.error("Receptor error: %s" % str(err))

def onMessage(data):
    if data:
        rawData = RawData(data)

        if rawData.downlinkformat == 17 and len(rawData.frame) == 30:
            icao = adsb.icao(rawData.frame[1:29])
            log.info("Raw Message Received: %s" % str(rawData.frame))

            __DATA_OUTPUT.addData(rawData.frame)

            if not icao in __RAW_BUFFER:
                __RAW_BUFFER[icao] = MessageBuffer(icao=icao)

            __RAW_BUFFER[icao].addRawData(rawData)

            if __RAW_BUFFER[icao].isComplete():
                log.info("Complete Message Received: %s" % str(__RAW_BUFFER[icao]))
                adsbInfo = ADSBInfo.createFromMessageBuffer(__RAW_BUFFER[icao])
                log.info("Processed Complete Message: %s" % str(__RAW_BUFFER[icao]))
                __DATA_UPLOADER.addADSBInfo(adsbInfo)

        else:
            log.info("Invalid Raw Message Received: %s" % str(rawData.frame))


def onUploaderStart():
    log.info("Uploader started!")

def onUploaderStop():
    log.info("Uploader stoped!")


def start():
    log.info("Starting receptor...")

    global __MICRO_ADSB
    __MICRO_ADSB.onOpen = onOpen
    __MICRO_ADSB.onClose = onClose
    __MICRO_ADSB.onMessage = onMessage
    __MICRO_ADSB.open()

    global __DATA_UPLOADER
    __DATA_UPLOADER.onStart = onUploaderStart
    __DATA_UPLOADER.onStop = onUploaderStop
    __DATA_UPLOADER.start()

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
    global __running
    __running = False


def __stop():
    global __MAP_BUFFER

    log.info("Stopping receptor...")
    __MICRO_ADSB.close()
    __DATA_UPLOADER.stop()
    __DATA_OUTPUT.stop()
    __MAP_BUFFER = None
