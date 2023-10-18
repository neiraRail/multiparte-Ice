from src.trivium.TriviumNode import TriviumNode
from src.comms.IceCommsHandler import IceCommsHandler
from src.sum.MultipartSum import MultipartSum

class Helper:
    def __init__(self, id):
        self.id = id
        self.comms = IceCommsHandler(id, 3)

        multiparte = MultipartSum(id, self.comms)
        trivium = TriviumNode(id, multiparte)
        self.stream = trivium.run()

        while True:
            next(self.stream)

import sys
helper = Helper(int(sys.argv[1]))


        