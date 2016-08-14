import logging as log
log.basicConfig(level=log.DEBUG)

import socket
import sys

from threading import Thread, RLock
from time import sleep


socket.setdefaulttimeout(.5)

class AsyncTask(Thread):

    running = False
    __doInBackground = None
    __args = None

    def __init__(self, doInBackground, args=None):
        Thread.__init__(self)
        self.__doInBackground = doInBackground
        self.__args = args

    def run(self):
        self.running = True
        if self.__args:
            self.__doInBackground(self.__args)
        else:
            self.__doInBackground()

        self.running = False


class AsyncServerSocket():
    __lock = RLock()
    __socket = None
    __host = None
    __port = None
    __listening = False

    def __init__(self, host="127.0.0.1", port=7685):
        self.__host = host
        self.__port = port

    def __setListening(self, listening):
        self.__lock.acquire()
        self.__listening = listening
        self.__lock.release()

    def start(self):
        if self.__listening:
            log.error("Socket Server: Server is already listening!")
            return

        else:
            self.onStarted()

        try:
            self.__lock.acquire()
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__socket.bind((self.__host, self.__port))
            self.__socket.listen(1)
            self.__lock.release()

        except Exception as err:
            log.error("Socket Server: %s" % str(err))
            self.stop()
            return

        self.__setListening(True)

        while self.__listening:
            try:
                self.__lock.acquire()
                task = AsyncTask(self.__handleConnection, self.__socket.accept())
                self.__lock.release()
                task.start()

            except KeyboardInterrupt as err:
                log.info("Socket Server: Keyboard interrupted by user!")
                self.stop()

            except Exception as err:
                pass

        self.stop()

    def __handleConnection(self, connetionAndClientAddress):
        conn = connetionAndClientAddress[0]
        self.onClienteConnected(connetionAndClientAddress[1])

        try:
            while self.__listening:
                try:
                    request = conn.recv(2048)
                    if not request:
                        break
                    else:
                        response = self.onClientMessage(request)
                        conn.send(response)
                except socket.timeout:
                    pass

                sleep(.001)

        except KeyboardInterrupt as err:
            log.error("Socket Server: Handling connection: Keyboard interrupted by user")
            self.stop()

        except Exception as err:
            log.error("Socket Server: Handling connection: %s" % str(err))

        finally:
            try:
                conn.send("")
            except:
                pass

            conn.close()
            self.onClientDisconnected(connetionAndClientAddress[1])

    def stop(self):
        if self.__listening:
            self.__setListening(False)
            self.onStoped()

        self.__lock.acquire()
        self.__socket.close()
        self.__lock.release()

    def onClientMessage(self, msg):
        log.info("Server Socket: message from client: %s" % msg)
        return ""

    def onStarted(self):
        log.info("Socket Server: Server listening: waiting for client...")

    def onStoped(self):
        log.info("Socket Server: Server stoped!")

    def onClienteConnected(self, clientAddress):
        log.info("Socket Server: Connecting to: %s" % str(clientAddress))

    def onClientDisconnected(self, clientAddress):
        log.info("Socket Server: Disconnecting from: %s" % str(clientAddress))


class ClientSocket():
    __lock = RLock()
    __socket = None
    __host = None
    __port = None
    __running = False

    def __init__(self, host="127.0.0.1", port=7685):
        self.__host = host
        self.__port = port

    def __setRunning(self, running):
        self.__lock.acquire()
        self.__running = running
        self.__lock.release()

    def connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.__host, self.__port))
        except Exception as err:
            log.error("Client Socket: %s" % str(err))
            return

        self.__setRunning(True)
        task = AsyncTask(self.__handleConnection)
        task.start()

    def __handleConnection(self):

        try:
            while(self.__running):
                try:
                    request = self.__socket.recv(2048)
                    if not request:
                        break
                    else:
                        response = self.onServerMessage(request)
                        self.__socket.send(response)
                except socket.timeout:
                    pass

                sleep(0.001)
        except Exception as err:
            log.error("Client Socket: %s" % str(err))
        finally:
            self.__socket.close()

    def sendMessage(self, msg):
        if self.__socket and self.__running:
            self.__socket.send(msg)

    def disconnect(self):
        self.__setRunning(False)
        self.__lock.acquire()
        self.__socket.close()
        self.__lock.release()

    def onServerMessage(self, msg):
        log.info("Client Socket: message from server: %s" % msg)
        return ""

    def onConnected(self):
        log.info("Client Socket: connected with server!")

    def onDisconnected(self):
        log.info("Client Socket: disconnected from server!")
