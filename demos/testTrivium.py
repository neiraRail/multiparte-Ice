from TriviumNode import TriviumNode
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-id", help="Id of the node", type=int)
args = parser.parse_args()

uno = TriviumNode(args.id)
for bit in uno.run():
    print(bit)
