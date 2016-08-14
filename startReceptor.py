import atexit
import logging as log
import socket
import sys

from threading import Thread
from time import sleep

log.basicConfig(level=log.DEBUG)

socket.setdefaulttimeout(.5)
server = None

@atexit.register
def exitHandler():
    server.stop()
    log.info("Stopping receptor...")


class AsyncTask(Thread):

    running = False
    __doInBackground = None
    __args = None

    def __init__(self, doInBackground, args):
        Thread.__init__(self)
        self.__doInBackground = doInBackground
        self.__args = args

    def run(self):
        self.running = True
        self.__doInBackground(self.__args)
        self.running = False


class AsyncServerSocker():
    __socket = None
    __host = None
    __port = None
    __listening = True

    def __init__(self, host="127.0.0.1", port=7685):
        self.__host = host
        self.__port = port

    def start(self):
        log.info("Server listening: waiting for client...")
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__host, self.__port))
        self.__socket.listen(1)

        self.__listening = True
        while self.__listening:
            try:
                task = AsyncTask(self.handleConnection, self.__socket.accept())
                task.start()
            except KeyboardInterrupt:
                self.stop()
            except Exception as err:
                pass

    def handleConnection(self, connetionAndClientAdress):
        print "Connection from: " + str(connetionAndClientAdress[1])
        conn = connetionAndClientAdress[0]

        try:
            while self.__listening:
                conn.send("Hello")
                sleep(1)
        except Exception as err:
            log.error("Handling connection: %s" % str(err))
        finally:
            log.error("Handling connection: stoping...")
            conn.close()

    def stop(self):
        self.__listening = False
        self.__socket.close()
        log.info("Server stoped!")


server = AsyncServerSocker()
server.start()
