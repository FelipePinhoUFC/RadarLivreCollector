from time import sleep

from network import ClientSocket
from network.dataOutput import DataOutput

out = DataOutput()
out.start()

sleep(1)
client = ClientSocket(host="127.0.0.1", port=30003)
client.connect()
client = ClientSocket(host="127.0.0.1", port=30003)
client.connect()

try:
    while(True):
        print "Sending broadcast"
        out.sendBroadcast("Oi!")
        sleep(5)
except:
    out.stop()