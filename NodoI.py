import time
import Multiparte
import random, logging, Ice, traceback

n=3
class NodoI(Multiparte.Nodo):
    def __init__(self, id):
        # Variables para la suma multiparte
        self.id = id
        self.key = None
        self.partes = []
        self.otrasPartes = []
        self.sumaParcial = None
        self.sumasParciales = []
        self.sumaTotal = None

        self.proxies = []
        self.nroPartesEnviadas = 0
    
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
    

    def conectarme(self):
        self.ic = Ice.initialize()
        for i in range(n):
            if i != int(self.id): 
                logging.info("Tengo que conectarme al nodo {}".format(i))
                base = self.ic.stringToProxy("Nodo_{}:default -p 1000{}".format(i,i))
                conectado = False
                while not conectado:
                    try:
                        logging.debug("Intento")
                        proxy = Multiparte.NodoPrx.checkedCast(base)
                        if not proxy:
                            raise RuntimeError("Invalid proxy")
                        self.proxies.append(proxy)
                        conectado = True
                        logging.info("Conectado al nodo {} :D".format(i))
                    except:
                        time.sleep(3)     
        logging.info("---------------Conexión lista--------------------\n\n")
    

    def sumar(self, key):
        self.nroPartesEnviadas = 0
        self.key = key
        self.partes = self.separarKey()
        logging.debug("Mi número secreto (s) es {}".format(self.key))
        logging.debug("Las partes que voy a compartir son {}".format(self.partes))


        # Pide todas las partes incluyendo la propia.
        self.otrasPartes = []
        self.otrasPartes.append(self.getMyPart(""))
        for i, proxy in enumerate(self.proxies):
            parteRecibida = False
            numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
            while not parteRecibida:
                try:
                    logging.debug("Necesito la parte de {}".format(numeroDelNodo))
                    parte = proxy.getMyPart("")
                    self.otrasPartes.append(parte)
                    logging.debug("que es {}".format(parte))
                except:
                    time.sleep(0.1)
                    logging.debug("")
                    traceback.print_exc()
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
        for i, proxy in enumerate(self.proxies):
            sumaRecibida = False
            numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
            while not sumaRecibida:
                try:
                    logging.debug("Necesito la suma parcial de {}".format(numeroDelNodo))
                    suma = proxy.getPartialSum()
                    self.sumasParciales.append(suma)
                    logging.debug("que es {}".format(suma))
                except:
                    time.sleep(0.1)
                    logging.debug("")
                else:
                    sumaRecibida = True
        self.partes = [] # Es importante borrar partes para que en la siguiente iteración no se envíe una parte anterior por accidente
        self.sumaTotal = sum(self.sumasParciales)
        logging.debug("Las sumas que he recolectado son: {}".format(self.sumasParciales))
        logging.debug("La suma final es: {}".format(self.sumaTotal))
        
        sumasTotales = []
        for i, proxy in enumerate(self.proxies):
            sumaTotalRecibida = False
            numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
            while not sumaTotalRecibida:
                try:
                    logging.debug("Necesito la suma final de {}".format(numeroDelNodo))
                    total = proxy.getFinalSum()
                    sumasTotales.append(total)
                    logging.debug("que es {}".format(total))
                except:
                    time.sleep(0.1)
                    logging.debug("")
                else:
                    sumaTotalRecibida = True

        self.sumaParcial = None # Es importante borrar sumaParcial para que no se envíe por accidente en la siguiente iteración de otro nodo
        assert all(x == sumasTotales[0] for x in sumasTotales) # Si una de las sumas totales no coincide se detiene la ejecución
        
        St = sum(self.sumasParciales) ## Tambien puede ser el XOR de todas las sumas parciales
        logging.info("St es: {}".format(St)) # Puede ser enviar a un server, etc.
        return St