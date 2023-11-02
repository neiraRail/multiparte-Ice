import threading, logging, time, traceback, Ice
from src.comms.CommsHandler import CommsHandler, TryAgainException, FatalException
import ZIceComms
from NodoI import NodoI



class IceCommsHandler(CommsHandler):
    def __init__(self, id, n=3):
        super().__init__(id)
        self.n = n
        self.object = None
        self.server_listo = False
        self.ic = None
        self.proxies = []


        self.server_thread = threading.Thread(target=self._start_server)
        self.server_thread.daemon = True # Para que finalize cuando el hilo principal muera
        self.server_thread.start()

        while not self.server_listo:
            time.sleep(1)
        logging.info("COMMS: Servidor listo")     


    def _start_server(self):
        try:
            self.ic = Ice.initialize()
            adapter = self.ic.createObjectAdapterWithEndpoints("NodoAdapter", "default -p 1000{}".format(self.id))
            self.object = NodoI({})
            adapter.add(self.object, self.ic.stringToIdentity("Nodo_{}".format(self.id)))
            adapter.activate()

            self.conectarme()

            self.server_listo = True

            self.ic.waitForShutdown()
        except:
            print("Antes del keyboard interrupt")
            traceback.print_exc()
            raise FatalException("Error al iniciar server")
        
        if self.ic:
            try:
                self.ic.destroy()
            except:
                traceback.print_exc()
                pass

    def conectarme(self):
        for i in range(self.n):
            if i != int(self.id): 
                logging.info("COMMS: Tengo que conectarme al nodo {}".format(i))
                base = self.ic.stringToProxy("Nodo_{}:default -p 1000{}".format(i,i))
                conectado = False
                while not conectado:
                    try:
                        logging.debug("COMMS: Intento")
                        proxy = ZIceComms.NodoPrx.checkedCast(base)
                        if not proxy:
                            raise RuntimeError("Invalid proxy")
                        self.proxies.append(proxy)
                        conectado = True
                        logging.info("COMMS: Conectado al nodo {} :D".format(i))
                    except BaseException as e:
                        logging.debug(e)
                        time.sleep(3)
            else:
                self.proxies.append(self.object)
        logging.info("---------------Conexión lista--------------------\n\n")
    

    def get(self, fromId, key, toId):
        logging.info("COMMS: estoy solicitando {} a {} :D".format(key, toId))
        try:
            return int(self.proxies[toId].get(key, fromId))
        except ZIceComms.NodoError as e:
            raise TryAgainException()
    
    def post(self, fromId, key, payload, toId):
        logging.info("COMMS: estoy llamando post a {} en {} con el payload: {} :D".format(toId, key, payload))
        return self.proxies[toId].post(key, payload, fromId)
    
    def addDataToId(self, key, value, toId):
        self.object.addDistributed(key, value, toId)
    
    def addDataGeneral(self, key, value):
        self.object.add(key, value)

    def deleteData(self, key):
        self.object.delete(key)

    def registerHook(self, key, function):
        self.object.register(key, function)