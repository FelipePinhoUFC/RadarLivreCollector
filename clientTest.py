from network import ClientSocket

client = ClientSocket()
client.connect()
client.sendMessage("Hello!")
client.disconnect()