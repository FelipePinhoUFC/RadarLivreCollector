import logging as log
log.basicConfig(level=log.DEBUG)

import threading
from time import sleep

from network import AsyncServerSocket


class DataOutput(AsyncServerSocket):

    __lockDataBuffer = threading.RLock()
    __dataFuffer = []

    def __init__(self, host="127.0.0.1", port=30003):
        AsyncServerSocket.__init__(self, host, port)

    def addData(self, data):
        self.__lockDataBuffer.acquire()
        self.__dataFuffer.append(data)
        self.__lockDataBuffer.release()

        if len(self.__dataFuffer) > 256:
            del self.__dataFuffer[0]

    def getBufferSize(self):
        return len(self.__dataFuffer)

    def onClienteConnected(self, clientAddress):
        log.info("DataOutput: connected with: %s" % str(clientAddress))
        while self.isListening():
            if self.__dataFuffer:
                self.__lockDataBuffer.acquire()
                self.sendBroadcast(self.__dataFuffer[0])
                del self.__dataFuffer[0]
                self.__lockDataBuffer.release()
            sleep(0.1)
