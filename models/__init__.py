import os

from time import time as systemTimestamp
from receptor.rootConfig import DATABASE_DIR, COLLECTOR_ID
from peewee.peewee import Model, CharField, DecimalField, BigIntegerField, SqliteDatabase
from pyModeS import adsb
from receptor.rootConfig import MAX_MESSAGE_AGE

db = SqliteDatabase(os.path.join(DATABASE_DIR, "receptor.db"))


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
        return "RawData: [tt=%d, dl=%d, fm=%s]" % (self.timestamp, self.downlinkformat, self.frame)


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
            self.dataId = []
            self.dataId.append(rawData)
        elif type >= 9 and type <= 18:
            flag = adsb.oe_flag(rawData.frame[1:29])
            if flag == 0:
                self.dataPositionEven.append(rawData)
                self.dataPositionEven.sort()
            else:
                self.dataPositionOdd.append(rawData)
                self.dataPositionOdd.sort()
        elif type == 19:
            self.dataVelocity = []
            self.dataVelocity.append(rawData)

    def checkDataAge(self):
        for i in range(0, len(self.dataPositionEven)):
            if self.dataPositionEven[i].timestamp < systemTimestamp() - MAX_MESSAGE_AGE:
                del self.dataPositionEven[i]
                i -= 1

        for i in range(0, len(self.dataPositionOdd)):
            if self.dataPositionOdd[i].timestamp < systemTimestamp() - MAX_MESSAGE_AGE:
                del self.dataPositionOdd[i]
                i -= 1

        for i in range(0, len(self.dataVelocity)):
            if self.dataVelocity[i].timestamp < systemTimestamp() - MAX_MESSAGE_AGE:
                del self.dataVelocity[i]
                i -= 1

    def clearPositionMessages(self):
        del self.dataPositionEven[0]
        del self.dataPositionOdd[0]
        del self.dataVelocity[0]

    def isComplete(self):
        return self.dataId and self.dataPositionEven and self.dataPositionOdd and self.dataVelocity

    def __repr__(self):
        return "MsgBuff: [ic=%s, di=%d, do=%d, de=%d, dv=%d]" % (self.icao, len(self.dataId), len(self.dataPositionEven), len(self.dataPositionOdd), len(self.dataVelocity))


class ADSBInfo(Model):
    collector = CharField(max_length=64, null=True, default="")

    modeSCode = CharField(max_length=16, null=True, default="")
    callsign = CharField(max_length=16, null=True, default="")

    # Airplane position
    latitude = DecimalField(max_digits=40, decimal_places=20, default=0.0)
    longitude = DecimalField(max_digits=40, decimal_places=20, default=0.0)
    altitude = DecimalField(max_digits=40, decimal_places=20, default=0.0)

    # Airplane velocity
    verticalVelocity = DecimalField(max_digits=40, decimal_places=20, default=0.0)
    horizontalVelocity = DecimalField(max_digits=40, decimal_places=20, default=0.0)

    # Airplane angle
    groundTrackHeading = DecimalField(max_digits=40, decimal_places=20, default=0.0)

    # Observation date time generated by server
    timestamp = BigIntegerField(default=0)
    timestampSent = BigIntegerField(default=0)

    # Originals ADS-B messages
    messageDataId = CharField(max_length=100, default='')
    messageDataPositionEven = CharField(max_length=100, default='')
    messageDataPositionOdd = CharField(max_length=100, default='')
    messageDataVelocity = CharField(max_length=100, default='')

    class Meta:
        database= db

    @staticmethod
    def createFromMessageBuffer(messageBuffer):
        info = None
        if messageBuffer.isComplete():
            latLng = adsb.position(messageBuffer.dataPositionEven[0].frame[1:29],
                                   messageBuffer.dataPositionOdd[0].frame[1:29],
                                   messageBuffer.dataPositionEven[0].timestamp,
                                   messageBuffer.dataPositionOdd[0].timestamp)
            velocity = adsb.velocity(messageBuffer.dataVelocity[0].frame[1:29])
            if latLng:
                info = ADSBInfo(
                    collector=COLLECTOR_ID,
                    modeSCode=adsb.icao(messageBuffer.dataId[0].frame[1:29]),
                    callsign=adsb.callsign(messageBuffer.dataId[0].frame[1:29]).replace("_", ""),
                    latitude=latLng[0],
                    longitude=latLng[1],
                    altitude=adsb.altitude(messageBuffer.dataPositionEven[0].frame[1:29]),
                    horizontalVelocity=velocity[0],
                    groundTrackHeading=velocity[1],
                    verticalVelocity=velocity[2],
                    messagDataId=messageBuffer.dataId[0].frame[1:29],
                    messagDataPositionEven=messageBuffer.dataId[0].frame[1:29],
                    messagDataPositionOdd=messageBuffer.dataId[0].frame[1:29],
                    messagDataVelocity=messageBuffer.dataId[0].frame[1:29],
                    timestamp=int(systemTimestamp() * 1000),
                    timestampSent=int(systemTimestamp() * 1000)
                )

        messageBuffer.clearPositionMessages()
        return info

    def serialize(self):
        return {
            "collector": self.collector, 
    
            "modeSCode": self.modeSCode, 
            "callsign": self.callsign, 
    
            # Airplane position
            "latitude": str(self.latitude),
            "longitude": str(self.longitude),
            "altitude": str(self.altitude) if self.altitude else 0,
    
            # Airplane velocity
            "verticalVelocity": str(self.verticalVelocity) if self.verticalVelocity else 0,
            "horizontalVelocity": str(self.horizontalVelocity) if self.horizontalVelocity else 0,
    
            # Airplane angle
            "groundTrackHeading": str(self.groundTrackHeading) if self.groundTrackHeading else 0,
    
            # Observation date time generated by server
            "timestamp": str(self.timestamp),
            "timestampSent": str(self.timestampSent),
    
            # Originals ADS-B messages
            "messageDataId": self.messageDataId, 
            "messageDataPositionEven": self.messageDataPositionEven, 
            "messageDataPositionOdd": self.messageDataPositionOdd, 
            "messageDataVelocity": self.messageDataVelocity
        }

    def __repr__(self):
        return "ADSBInfo[icao=%s, callsign=%s, lat=%s, lng=%s]" % (self.modeSCode, self.callsign, str(self.latitude), str(self.longitude))


# db.connect()
# db.create_tables([ADSBInfo], safe=True)
