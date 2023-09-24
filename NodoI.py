import threading
import Multiparte
import random, logging

class NodoI(Multiparte.Nodo, threading.Thread):
    def __init__(self, id):
        # Variables para la suma multiparte
        self.id = id
        self.key = None
        self.partes = []
        self.otrasPartes = []
        self.sumaParcial = None
        self.sumasParciales = []
        self.sumaTotal = None

        self.nroPartesEnviadas = 0

        #Variables para el trilium
        self.vector = self.generarVector(id)
        self.intermedio1 = [66,69,66][id]
        self.intermedio2 = [69,78,87][id]

        threading.Thread.__init__(self)
        self.__threadCondition = threading.Condition()
        
    # Metodos trilium
    def generarVector(self, id, seed=42):
        random.seed(seed)
        largo = [93,84,111][id]

        # return [i % 2 for i in range(largo)]
        return [random.randint(0, 1) for _ in range(largo)]
    
    def primerXor(self):
        return (self.vector[-3] & self.vector[-2]) ^ self.vector[-1] ^ self.vector[self.intermedio1]
    
    def moverVector(self, St, s):
          nuevo = St ^ s ^ self.vector[self.intermedio2]
          self.vector.insert(0, nuevo)
          self.vector.pop()
        
    
    # Metodos suma multiparte
    def getMyPart(self, mensaje, current=None):
        #TODO: quitar self.nroPartesEnviadas y usar otra estrategia
        if len(self.partes) < n:
            raise Multiparte.NotReadyError()

        if self.nroPartesEnviadas == 3:
            return 0
        
        tuParte = self.partes[self.nroPartesEnviadas]
        self.nroPartesEnviadas += 1

        return tuParte
    
    def getPartialSum(self, current=None):
        if self.sumaParcial == None:
            raise Multiparte.NotReadyError()
        return sum(self.otrasPartes)
    
    def getFinalSum(self, current=None):
        if self.sumaTotal == None:
            raise Multiparte.NotReadyError()
        return self.sumaTotal

    def separarKey(self):
        partes = []
        for i in range(n-1):
            partes.append(random.randint(-10,10))
        partes.append(self.key - sum(partes))
        return partes
    
    ## Hilo de ejecución para las operaciones de cliente.
    def run(self):
        with self.__threadCondition:
            proxies = []
            for i in range(n):
                if i != int(self.id): 
                    logging.info("Tengo que conectarme al nodo {}".format(i))
                    base = ic.stringToProxy("Nodo_{}:default -p 1000{}".format(i,i))
                    conectado = False
                    while not conectado:
                        try:
                            logging.debug("Intento")
                            proxy = Multiparte.NodoPrx.checkedCast(base)
                            if not proxy:
                                raise RuntimeError("Invalid proxy")
                            proxies.append(proxy)
                            conectado = True
                            logging.info("Conectado al nodo {} :D".format(i))
                        except:
                            self.__threadCondition.wait(3)     
            logging.info("---------------Conexión lista--------------------\n\n")
            while True:
                self.nroPartesEnviadas = 0
                self.key = self.primerXor()
                self.partes = self.separarKey()
                logging.debug("Mi número secreto (s) es {}".format(self.key))
                logging.debug("Las partes que voy a compartir son {}".format(self.partes))
                logging.debug("Mi vector tiene largo: {}".format(len(self.vector)))


                # Pide todas las partes incluyendo la propia.
                self.otrasPartes = []
                self.otrasPartes.append(self.getMyPart(""))
                for i, proxy in enumerate(proxies):
                    parteRecibida = False
                    numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
                    while not parteRecibida:
                        try:
                            logging.debug("Necesito la parte de {}".format(numeroDelNodo))
                            parte = proxy.getMyPart("")
                            self.otrasPartes.append(parte)
                            logging.debug("que es {}".format(parte))
                        except:
                            self.__threadCondition.wait(0.1)
                            logging.debug("")
                        else:
                            parteRecibida = True

                self.sumaTotal = None # Importante borrar para no enviar por accidente
                self.sumaParcial = sum(self.otrasPartes)
                logging.debug("Las partes que he recolectado son: {}".format(self.otrasPartes))
                logging.debug("Y suman {}".format(self.sumaParcial))

                # Suma las partes de otros y genera su suma parcial
                self.sumasParciales = []
                self.sumasParciales.append(self.sumaParcial)

                # Solcita las sumas parciales de los otros
                for i, proxy in enumerate(proxies):
                    sumaRecibida = False
                    numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
                    while not sumaRecibida:
                        try:
                            logging.debug("Necesito la suma parcial de {}".format(numeroDelNodo))
                            suma = proxy.getPartialSum()
                            self.sumasParciales.append(suma)
                            logging.debug("que es {}".format(suma))
                        except:
                            self.__threadCondition.wait(0.1)
                            logging.debug("")
                        else:
                            sumaRecibida = True
                self.partes = [] # Es importante borrar partes para que en la siguiente iteración no se envíe una parte anterior por accidente
                self.sumaTotal = sum(self.sumasParciales)
                logging.debug("Las sumas que he recolectado son: {}".format(self.sumasParciales))
                logging.debug("La suma final es: {}".format(self.sumaTotal))
                
                sumasTotales = []
                for i, proxy in enumerate(proxies):
                    sumaTotalRecibida = False
                    numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
                    while not sumaTotalRecibida:
                        try:
                            logging.debug("Necesito la suma final de {}".format(numeroDelNodo))
                            total = proxy.getFinalSum()
                            sumasTotales.append(total)
                            logging.debug("que es {}".format(total))
                        except:
                            self.__threadCondition.wait(0.1)
                            logging.debug("")
                        else:
                            sumaTotalRecibida = True

                self.sumaParcial = None # Es importante borrar sumaParcial para que no se envíe por accidente en la siguiente iteración de otro nodo
                assert all(x == sumasTotales[0] for x in sumasTotales) # Si una de las sumas totales no coincide se detiene la ejecución
                
                St = sum(self.sumasParciales) % 2
                logging.info("St es: {}".format(St))
                self.moverVector(St, self.key)

                if "--debug" in sys.argv:
                    input("Presiona Enter para continuar...")
                else:
                    pass
            # ic.waitForShutdown()

# CODIGO DEL SERVER ---------------------------------------------------------------------------------------------
# Está en el mismo archivo para ponder utilizar el objeto ic = Ice.initialize()

import sys, traceback, Ice

if "--debug" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


id = int(sys.argv[1])
logging.debug("id es: {}".format(id))

n = 3
status = 0
ic = None
try:
    ic = Ice.initialize()

    adapter = ic.createObjectAdapterWithEndpoints("NodoAdapter", "default -p 1000{}".format(id))
    object = NodoI(id)
    adapter.add(object, ic.stringToIdentity("Nodo_{}".format(id)))
    adapter.activate()

    object.daemon = True
    object.start()
    ic.waitForShutdown()

except:
    traceback.logging.debug_exc()
    status = 1

if ic:
    # Clean up
    try:
        ic.destroy()
    except:
        traceback.logging.debug_exc()
        status = 1

sys.exit(status)