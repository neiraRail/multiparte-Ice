from src.trivium.TriviumNode import TriviumNode
from src.comms.IceCommsHandler import IceCommsHandler
from src.sum.MultipartSum import MultipartSum


class Listener:
    def __init__(self, id):
        self.id = id
        self.comms = IceCommsHandler(id, 3)

        multiparte = MultipartSum(id, self.comms)
        trivium = TriviumNode(id, multiparte)

        self.randomStream = trivium.run()
        self.listeningTo = None
        self.bit = next(self.randomStream)
        self.comms.registerHook("msgu", self.recieveMessage)
        while True:
            self.bit = next(self.randomStream)

    def recieveMessage(self, payload, id):
        print("Recieve message!!")
        self.listeningTo = id
        self.comms.registerHook("data", self.recieveBit)


    def recieveBit(self, payload, id):
        if id != self.listeningTo:
            raise Exception("Not my sender")
        value = int(payload[0]) ^ self.bit
        print("{} ^ {} = {}".format(self.bit, int(payload[0]), value))
        if payload[1] == 0:
            # TODO: Desconectar hook
            self.listeningTo = None
            pass

import sys
listener = Listener(int(sys.argv[1]))