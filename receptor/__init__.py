import logging as log

from pyModeS import adsb

__MAP_BUFFER = {}

class RawData():

    timestamp = None
    downlinkformat = None
    frame = None

    def __init__(self, raw):
        self.timestamp = raw["timestamp"]["integer"]
        self.downlinkformat = raw["downlinkformat"]
        self.frame = raw["frame"]

    def __cmp__(self, other):
        return self.timestamp.__cmp__(other.timestamp)

    def __repr__(self):
        return "RawData: [tt=%d, dl=%d, fm=%s]" % self.timestamp, self.downlinkformat, self.frame


class MessageBuffer():

    dataId = None
    dataPositionEven = None
    dataPositionOdd = None
    dataVelocity = None

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def addRawData(self, rawData):
        type = adsb.typecode(rawData.frame[1:29])
        if type >= 1 and type <= 4:
            pass

    def isComplete(self):
        return self.dataId and self.dataPositionEven and self.dataPositionOdd and self.dataVelocity


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

        if rawData.downlinkformat == 17:
            icao24 = adsb.icao(rawData.frame[1:29])

            if not icao24 in __MAP_BUFFER:
                __MAP_BUFFER[icao24] = []

            __MAP_BUFFER[icao24].append(rawData)