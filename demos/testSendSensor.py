from src.comms.IceCommsHandler import IceCommsHandler
from src.sum.MultipartSum import MultipartSum
from src.trivium.SensorNode import SensorNode
from src.Sender import Sender
import src.binary_utils as utils
import sys, time

id = int(sys.argv[1])

comms = IceCommsHandler(id, 3)
        
multiparte = MultipartSum(id, comms)
trivium = SensorNode(id, multiparte)

sender = Sender(id, comms, trivium)
while True:
    message = "Hola mamá"
    binary = utils.string_to_binary(message)
    sender.send(binary, 2)
    time.sleep(5)
