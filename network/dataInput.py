import logging as log

from config import COLLECTOR_ID
from models import ADSBInfo
from time import time as systemTimestamp

log.basicConfig(level=log.DEBUG)

from network import ClientSocket


class DataInput(ClientSocket):
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

                self.onADSBInfoReceived(info)

    def onADSBInfoReceived(self, info):
        log.info("DataInput: New adsb Info received!")