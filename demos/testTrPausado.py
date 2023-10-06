from TriviumNode import TriviumNode
import sys

uno = TriviumNode(int(sys.argv[1]))

stream = uno.run()

while True:
    print(next(stream))
    input("presiona Enter...")