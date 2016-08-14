
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

    icao = ""
    dataId = []
    dataPositionEven = []
    dataPositionOdd = []
    dataVelocity = []

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def addRawData(self, rawData):
        type = adsb.typecode(rawData.frame[1:29])
        if type >= 1 and type <= 4:
            self.dataId.append(rawData)
            self.dataId.sort(reverse=True)
        elif type >= 9 and type <= 18:
            flag = adsb.oe_flag()
            if flag == 0:
                self.dataPositionEven.append(rawData)
                self.dataPositionEven.sort(reverse=True)
            else:
                self.dataPositionOdd.append(rawData)
                self.dataPositionOdd.sort(reverse=True)
        elif type == 19:
            self.dataVelocity.append(rawData)
            self.dataVelocity.sort(reverse=True)

    def isComplete(self):
        return self.dataId and self.dataPositionEven and self.dataPositionOdd and self.dataVelocity

    def __repr__(self):
        return "MsgBuff: [ic=%s, di=%d, do=%d, de=%d, dv=%d]" % self.icao, len(self.dataId), len(self.dataPositionEven), len(self.dataPositionOdd), len(self.dataVelocity)


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
            icao = adsb.icao(rawData.frame[1:29])

            if not icao in __MAP_BUFFER:
                __MAP_BUFFER[icao] = MessageBuffer(icao=icao)

            __MAP_BUFFER[icao].addMessage(rawData)

            if __MAP_BUFFER[icao].isComplete():
                log.info("Message Received: %s" % __MAP_BUFFER[icao])
                del __MAP_BUFFER[icao]
