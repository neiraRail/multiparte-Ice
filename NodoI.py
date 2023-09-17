import threading
import Multiparte
import random, asyncio

n = 3

class NodoI(Multiparte.Nodo, threading.Thread):
    def __init__(self, id, key):
        self.id = id

        threading.Thread.__init__(self)
        self.__threadCondition = threading.Condition()
        self.key = key
        self.parts = self.separateKey()
        self.otherParts = []
        self.partialSums = []

        self.partsSended = 0

    def getMyPart(self, mensaje, current=None):
        if self.partsSended == 3:
            return 0
        
        yourPart = self.parts[self.partsSended]
        self.partsSended += 1

        return yourPart
    
    def getPartialSum(self, current=None):
        if len(self.otherParts) < n:
            raise Multiparte.NotReadyError()
        return sum(self.otherParts)
    
    def getFinalSum(self, current=None):
        if len(self.partialSums) < n:
            raise Multiparte.NotReadyError()
        return sum(self.partialSums)

    def separateKey(self):
        parts = []
        for i in range(n-1):
            parts.append(random.randint(-10,10))
        parts.append(self.key - sum(parts))
        return parts
    
    def run(self):
        with self.__threadCondition:
            print("Mi número secreto es {}".format(self.key))
            print("Las partes que voy a compartir son {}".format(self.parts))
            proxies = []
            for i in range(n):
                if i != int(self.id): 
                    print("Tengo que conectarme al nodo {}".format(i))
                    base = ic.stringToProxy("Nodo_{}:default -p 1000{}".format(i,i))
                    connected = False
                    while not connected:
                        try:
                            print("Intento")
                            proxy = Multiparte.NodoPrx.checkedCast(base)
                            if not proxy:
                                raise RuntimeError("Invalid proxy")
                            proxies.append(proxy)
                            connected = True
                            print("Conectado al nodo {} :D".format(i))
                        except:
                            self.__threadCondition.wait(3)            

            # Pide todas las partes incluyendo la propia.
            self.otherParts.append(self.getMyPart(""))
            for i, proxy in enumerate(proxies):
                partRecieved = False
                while not partRecieved:
                    try:
                        print("Necesito la parte de {}".format(i), end=" ")
                        parte = proxy.getMyPart("")
                        self.otherParts.append(parte)
                        print("que es {}".format(parte))
                    except Multiparte.NotReadyError:
                        self.__threadCondition.wait(1)
                        print("")
                    else:
                        partRecieved = True
            print("Las partes que he recolectado son: {}".format(self.otherParts))
            print("Y suman {}".format(sum(self.otherParts)))

            # Suma las partes de otros y genera su suma parcial
            self.partialSums.append(sum(self.otherParts))

            # Solcita las sumas parciales de los otros
            for i, proxy in enumerate(proxies):
                sumRecieved = False
                while not sumRecieved:
                    try:
                        print("Necesito la suma parcial de {}".format(i))
                        suma = proxy.getPartialSum()
                        self.partialSums.append(suma)
                    except:
                        self.__threadCondition.wait(1)
                    else:
                        sumRecieved = True
            print("Las sumas que he recolectado son: {}".format(self.partialSums))
            print("La suma final es: {}".format(sum(self.partialSums)))
        # ic.waitForShutdown()

# CODIGO DEL SERVER ---------------------------------------------------------------------------------------------
# Está en el mismo archivo para ponder utilizar el objeto ic = Ice.initialize()

import sys, traceback, Ice


id = int(sys.argv[1])
key = int(sys.argv[2])
print("id es: {}".format(id))

status = 0
ic = None
try:
    ic = Ice.initialize()

    adapter = ic.createObjectAdapterWithEndpoints("NodoAdapter", "default -p 1000{}".format(id))
    object = NodoI(id, key)
    adapter.add(object, ic.stringToIdentity("Nodo_{}".format(id)))
    adapter.activate()

    object.daemon = True
    object.start()
    ic.waitForShutdown()

except:
    traceback.print_exc()
    status = 1

if ic:
    # Clean up
    try:
        ic.destroy()
    except:
        traceback.print_exc()
        status = 1

sys.exit(status)