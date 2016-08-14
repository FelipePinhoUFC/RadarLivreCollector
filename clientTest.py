import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 7685)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
try:
    while(True):
        print sock.recv(1024)
except:
    print "Closing except"
    try:
        sock.close()
    except:
        pass
finally:
    print "Closing finally"
    sock.close()