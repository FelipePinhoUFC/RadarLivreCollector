import logging as log
log.basicConfig(level=log.DEBUG)
log.getLogger("requests").setLevel(log.WARNING)
log.getLogger("urllib3").setLevel(log.WARNING)

from time import sleep

from models import ADSBInfo


from threading import Thread

import requests

from config import LOGIN, PASSWORD, COLLECTOR_ID


class DataUploader(Thread):
    __adsbInfoBuffer = []
    __serverHost = None
    __running = False

    sendHelloInterval = None
    sendADSBInfoInterval = None
    bufferSizeLimit = None


    def __init__(self, serverHost="www.radarlivre.com", sendHelloInterval=10000, sendADSBInfoInterval=1000, bufferSizeLimit=256):
        Thread.__init__(self)
        self.__serverHost = serverHost
        self.sendHelloInterval = sendHelloInterval
        self.sendADSBInfoInterval = sendADSBInfoInterval
        self.bufferSizeLimit = bufferSizeLimit

        self.loadBuffer()

    def run(self):
        self.__running = True

        timeCount = 0
        while self.__running:

            if timeCount % self.sendHelloInterval == 0:
                self.__sendHelloToServer()

            if timeCount % self.sendADSBInfoInterval == 0:
                self.__sendADSBInfoToServer()

            timeCount += 1
            sleep(.001)

        self.onStop()


    def addADSBInfo(self, adsbInfo):
        if len(self.__adsbInfoBuffer) >= self.bufferSizeLimit:
            adsbInfo.save()
        else:
            self.__adsbInfoBuffer.append(adsbInfo)
            querySet = ADSBInfo.select()
            storeds = []
            for info in querySet:
                storeds.append(info)

            while len(self.__adsbInfoBuffer) < self.bufferSizeLimit:
                if storeds:
                    self.__adsbInfoBuffer.append(storeds[0])
                    storeds[0].delete_instance()
                    del storeds[0]
                else:
                    break

        log.info("DataUploader: Adding adsbInfo: %d" % len(self.__adsbInfoBuffer))



    def __sendHelloToServer(self):
        log.info("DataUploader: Sending hello to server...")
        try:
            response = requests.put("http://%s/api/collector/%s/" % (self.__serverHost, COLLECTOR_ID),
                                    json={"id": COLLECTOR_ID}, auth=(LOGIN, PASSWORD))
            if response.status_code >= 400:
                log.warning("DataUploader: %d: %s" % (response.status_code, str(response.json())))
        except Exception as err:
            log.error("DataUploader: %s" % str(err))


    def __sendADSBInfoToServer(self):
        if self.__adsbInfoBuffer:
            log.info("DataUploader: Sending data to server: %d" % len(self.__adsbInfoBuffer))

        while self.__adsbInfoBuffer:
            info = self.__adsbInfoBuffer[0]
            json = info.serialize()

            try:
                response = requests.post("http://%s/api/adsb_info/" % str(self.__serverHost), json=json, auth=(LOGIN, PASSWORD))
                if response.status_code >= 400:
                    log.warning("DataUploader: %d: %s" % (response.status_code, str(response.json())))
                    break
                else:
                    del self.__adsbInfoBuffer[0]

            except Exception as err:
                log.error("DataUploader: %s" % str(err))
                break



    def persistBuffer(self):
        for info in self.__adsbInfoBuffer:
            info.save()
        log.info("DataUploader: Persisting data before close")

    def loadBuffer(self):
        infos = ADSBInfo.select()
        for info in infos:
            self.__adsbInfoBuffer.append(info)
            info.delete_instance()
            if len(self.__adsbInfoBuffer) >= self.bufferSizeLimit:
                break

        log.info("DataUploader: loading from local data: %d" % len(self.__adsbInfoBuffer))


    def stop(self):
        log.info("DataUploader: Stoping...")
        self.persistBuffer()
        self.__running = False


    def onStop(self):
        log.info("DataUploader: Stoped!")