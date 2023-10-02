from TriviumNode import TriviumNode
import sys

uno = TriviumNode(int(sys.argv[1]))

iter = uno.run()

while True:
    print(next(iter))
    input("presiona Enter...")