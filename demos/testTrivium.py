from TriviumNode import TriviumNode
import sys

uno = TriviumNode(int(sys.argv[1]))
for bit in uno.run():
    print(bit)
