from NodoI import NodoI
import logging
import sys, Ice, time, traceback
import threading
import Multiparte

if "--debug" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

class NodoMP():
    def __init__(self, id, n=3):
        self.id = id
        self.n = n
        self.server_listo = False
        self.object = None
        self.ic = None
        self.proxies = []

        logging.debug("id es: {}".format(id))
        self.server_thread = threading.Thread(target=self._start_server)
        self.server_thread.daemon = True # Para que finalize cuando el hilo principal muera
        self.server_thread.start()

        while not self.server_listo:
            time.sleep(1)
        logging.info("Servidor listo")


    def _start_server(self):
        try:
            self.ic = Ice.initialize()
            adapter = self.ic.createObjectAdapterWithEndpoints("NodoAdapter", "default -p 1000{}".format(self.id))
            self.object = NodoI(self.id, self.n)
            adapter.add(self.object, self.ic.stringToIdentity("Nodo_{}".format(self.id)))
            adapter.activate()

            self.conectarme()

            self.server_listo = True

            self.ic.waitForShutdown()
        except:
            print("Antes del keyboard interrupt")
            traceback.print_exc()
        
        if self.ic:
            try:
                self.ic.destroy()
            except:
                traceback.print_exc()
                pass

    
    def conectarme(self):
        for i in range(self.n):
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
                    except BaseException as e:
                        logging.debug(e)
                        time.sleep(3)
        logging.info("---------------Conexión lista--------------------\n\n")

    def sumar(self, key):
        self.object.setKey(key)
        self.object.separarKey()
        logging.debug("Mi número secreto (s) es {}".format(self.object.key))
        logging.debug("Las partes que voy a compartir son {}".format(self.object.partes))


        # Pide todas las partes incluyendo la propia.
        otrasPartes = []
        otrasPartes.append(self.object.getMyPart(""))
        for i, proxy in enumerate(self.proxies):
            parteRecibida = False
            numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
            while not parteRecibida:
                try:
                    logging.debug("Necesito la parte de {}".format(numeroDelNodo))
                    parte = proxy.getMyPart("")
                    otrasPartes.append(parte)
                    logging.debug("que es {}".format(parte))
                except Multiparte.NotReadyError as e:
                    logging.debug(e)
                    #time.sleep(0.1)
                except Ice.ConnectionRefusedException as e:
                    logging.debug(e)
                    sys.exit()
                else:
                    parteRecibida = True

        self.object.borrarSumaFinal() # Importante borrar para no enviar por accidente
        self.object.setSumaParcial(sum(otrasPartes))
        logging.debug("Las partes que he recolectado son: {}".format(otrasPartes))
        logging.debug("Y suman {}".format(self.object.getPartialSum()))

        # Suma las partes de otros y genera su suma parcial
        sumasParciales = []
        sumasParciales.append(self.object.getPartialSum())

        # Solcita las sumas parciales de los otros
        for i, proxy in enumerate(self.proxies):
            sumaRecibida = False
            numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
            while not sumaRecibida:
                try:
                    logging.debug("Necesito la suma parcial de {}".format(numeroDelNodo))
                    suma = proxy.getPartialSum()
                    sumasParciales.append(suma)
                    logging.debug("que es {}".format(suma))
                except Multiparte.NotReadyError as e:
                    logging.debug(e)
                    #time.sleep(0.1)
                except Ice.ConnectionRefusedException as e:
                    logging.debug(e)
                    sys.exit()
                else:
                    sumaRecibida = True
        self.object.borrarPartes() # Es importante borrar partes para que en la siguiente iteración no se envíe una parte anterior por accidente
        self.object.setSumaFinal(sum(sumasParciales))
        logging.debug("Las sumas que he recolectado son: {}".format(sumasParciales))
        logging.debug("La suma final es: {}".format(self.object.getFinalSum()))
        
        sumasTotales = []
        sumasTotales.append(self.object.getFinalSum())
        for i, proxy in enumerate(self.proxies):
            sumaTotalRecibida = False
            numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
            while not sumaTotalRecibida:
                try:
                    logging.debug("Necesito la suma final de {}".format(numeroDelNodo))
                    total = proxy.getFinalSum()
                    sumasTotales.append(total)
                    logging.debug("que es {}".format(total))
                except Multiparte.NotReadyError as e:
                    logging.debug(e)
                    #time.sleep(0.1)
                except Ice.ConnectionRefusedException as e:
                    logging.debug(e)
                    sys.exit()
                else:
                    sumaTotalRecibida = True

        self.object.borrarSumaParcial() # Es importante borrar sumaParcial para que no se envíe por accidente en la siguiente iteración de otro nodo
        assert all(x == sumasTotales[0] for x in sumasTotales) # Si una de las sumas totales no coincide se detiene la ejecución
        
        logging.debug("Suma total es: {}".format(self.object.getFinalSum())) # Puede ser enviar a un server, etc.
        while self.object.nroSumasCheckeadas < self.n:
            pass
        return self.object.getFinalSum()