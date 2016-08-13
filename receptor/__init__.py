import logging as log

__MAP_BUFFER = {}

class RawData():

    timestamp = None
    downlinkformat = None
    frame = None

    def __init__(self, raw):
        self.timestamp = raw["timestamp"]["integer"]
        self.downlinkformat = raw["downlinkformat"]
        self.frame = raw["frame"]


def __onOpen(err):
    if err:
        log.error("Receptor open: %s" % str(err))
    else:
        log.error("Receptor open: opened!")


def __onClose(err):
    if err:
        log.error("Receptor close: %s" % str(err))
    else:
        log.error("Receptor close: closed!")


def __onMessage(data):
    if data:
        rawData = RawData(data)