from NodoMP import NodoMP
import sys

uno = NodoMP(int(sys.argv[1]))
print(uno.sumar(int(sys.argv[2])))