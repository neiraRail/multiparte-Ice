from src.trivium.TriviumNode import TriviumNode
from src.sum.MultipartSum import MultipartSum
from src.comms.IceCommsHandler import IceCommsHandler
import sys

comms = IceCommsHandler(int(sys.argv[1]))
suma = MultipartSum(int(sys.argv[1]), comms)
uno = TriviumNode(int(sys.argv[1]), suma)

stream = uno.run()

while True:
    print(next(stream))
    input("presiona Enter...")