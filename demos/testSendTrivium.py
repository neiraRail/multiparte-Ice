from src.comms.IceCommsHandler import IceCommsHandler
from src.sum.MultipartSum import MultipartSum
from src.trivium.TriviumNode import TriviumNode
from src.Sender import Sender
import sys, time

comms = IceCommsHandler(id, 3)
        
multiparte = MultipartSum(id, comms)
trivium = TriviumNode(id, multiparte)

sender = Sender(int(sys.argv[1]), comms, trivium)
while True:
    sender.send("111001011000", 2)
    time.sleep(5)
