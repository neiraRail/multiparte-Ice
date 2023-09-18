import threading
import Multiparte
import random, asyncio

n = 3

class NodoI(Multiparte.Nodo, threading.Thread):
    def __init__(self, id, key):
        self.id = id
        self.key = key

        threading.Thread.__init__(self)
        self.__threadCondition = threading.Condition()
        
        self.partes = self.separarKey()
        self.otrasPartes = []
        self.sumasParciales = []

        self.nroPartesEnviadas = 0

    def getMyPart(self, mensaje, current=None):
        if self.nroPartesEnviadas == 3:
            return 0
        
        tuParte = self.partes[self.nroPartesEnviadas]
        self.nroPartesEnviadas += 1

        return tuParte
    
    def getPartialSum(self, current=None):
        if len(self.otrasPartes) < n:
            raise Multiparte.NotReadyError()
        return sum(self.otrasPartes)
    
    def getFinalSum(self, current=None):
        if len(self.sumasParciales) < n:
            raise Multiparte.NotReadyError()
        return sum(self.sumasParciales)

    def separarKey(self):
        partes = []
        for i in range(n-1):
            partes.append(random.randint(-10,10))
        partes.append(self.key - sum(partes))
        return partes
    
    ## Hilo de ejecución para las operaciones de cliente.
    def run(self):
        with self.__threadCondition:
            print("Mi número secreto es {}".format(self.key))
            print("Las partes que voy a compartir son {}".format(self.partes))
            proxies = []
            for i in range(n):
                if i != int(self.id): 
                    print("Tengo que conectarme al nodo {}".format(i))
                    base = ic.stringToProxy("Nodo_{}:default -p 1000{}".format(i,i))
                    conectado = False
                    while not conectado:
                        try:
                            print("Intento")
                            proxy = Multiparte.NodoPrx.checkedCast(base)
                            if not proxy:
                                raise RuntimeError("Invalid proxy")
                            proxies.append(proxy)
                            conectado = True
                            print("Conectado al nodo {} :D".format(i))
                        except:
                            self.__threadCondition.wait(3)            

            # Pide todas las partes incluyendo la propia.
            self.otrasPartes.append(self.getMyPart(""))
            for i, proxy in enumerate(proxies):
                parteRecibida = False
                while not parteRecibida:
                    try:
                        print("Necesito la parte de {}".format(i), end=" ")
                        parte = proxy.getMyPart("")
                        self.otrasPartes.append(parte)
                        print("que es {}".format(parte))
                    except Multiparte.NotReadyError:
                        self.__threadCondition.wait(1)
                        print("")
                    else:
                        parteRecibida = True
            print("Las partes que he recolectado son: {}".format(self.otrasPartes), end=" ")
            print("Y suman {}".format(sum(self.otrasPartes)))

            # Suma las partes de otros y genera su suma parcial
            self.sumasParciales.append(sum(self.otrasPartes))

            # Solcita las sumas parciales de los otros
            for i, proxy in enumerate(proxies):
                sumaRecibida = False
                while not sumaRecibida:
                    try:
                        print("Necesito la suma parcial de {}".format(i), end=" ")
                        suma = proxy.getPartialSum()
                        self.sumasParciales.append(suma)
                        print("que es {}".format(suma))
                    except:
                        self.__threadCondition.wait(1)
                        print("")
                    else:
                        sumaRecibida = True
            print("Las sumas que he recolectado son: {}".format(self.sumasParciales))
            print("La suma final es: {}".format(sum(self.sumasParciales)))
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