from network import AsyncServerSocket


class DataOutput(AsyncServerSocket):

    dataFuffer = []

    def __init__(self, host="127.0.0.1", port=30003):
        AsyncServerSocket.__init__(self, host, port)

    def onClienteConnected(self, clientAddress):
        pass