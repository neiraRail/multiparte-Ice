from src.trivium.TriviumNode import TriviumNode
from src.sum.MultipartSum import MultipartSum
from src.comms.IceCommsHandler import IceCommsHandler
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-id", help="Id of the node", type=int)
args = parser.parse_args()

comms = IceCommsHandler(args.id)
suma = MultipartSum(args.id, comms)
uno = TriviumNode(args.id, suma)
for bit in uno.run():
    print(bit)
