from src.sum.MultipartSum import MultipartSum
from src.comms.IceCommsHandler import IceCommsHandler as IceComms
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-id", help="Id of the node", type=int)
parser.add_argument("-v", help="Value to sum", type=int)
parser.add_argument("-n", help="Number of nodes", type=int, default=3)
args = parser.parse_args()

comms = IceComms(args.id, args.n)
uno = MultipartSum(args.id, comms, n=args.n)
print(uno.sumar(args.v))