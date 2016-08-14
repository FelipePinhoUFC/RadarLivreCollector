import logging as log

from config import COLLECTOR_ID
from models import ADSBInfo
from time import time as systemTimestamp

log.basicConfig(level=log.DEBUG)

from network import ClientSocket


class DataInput(ClientSocket):

    __adsbBuffer = {}

    def onServerMessage(self, msg):
        log.info("DataInput: Server message %s" % str(msg))

        entries = msg.split("\n")
        for entry in entries:
            entry = entry.split(",")
            if len(entry) >= 17:
                info = ADSBInfo(
                    collector=COLLECTOR_ID,
                    modeSCode=entry[4],
                    callsign=entry[10],
                    latitude=entry[14],
                    longitude=entry[15],
                    altitude=entry[11],
                    horizontalVelocity=entry[12],
                    groundTrackHeading=entry[13],
                    verticalVelocity=entry[16],
                    messagDataId="",
                    messagDataPositionEven="",
                    messagDataPositionOdd="",
                    messagDataVelocity="",
                    timestamp=int(systemTimestamp() * 1000),
                    timestampSent=int(systemTimestamp() * 1000)
                )

                info = self.__addToBuffer(info)
                if info.icao and info.callsign and info.latitude and info.longitude:
                    self.onADSBInfoReceived(info)

    def onADSBInfoReceived(self, info):
        log.info("DataInput: New adsb Info received!")

    def __addToBuffer(self, info):
        if info.icao in self.__adsbBuffer:
            old = self.__adsbBuffer[info.icao]
            attrs = filter(lambda x: not x.endswith('__'), dir(old))
            for attr in attrs:
                if getattr(info, attr):
                    setattr(old, attr, getattr(info, attr))

            return old
        else:
            self.__adsbBuffer[info.icao] = info
            return info

