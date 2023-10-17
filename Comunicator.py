from NodoI import NodoI
import threading, logging, time, traceback
import Multiparte, Ice

class Comunicator:
    def __init__(self, id, n=3):
        self.id = id
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
        logging.info("Servidor listo")     


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
    

    def get(self, fromId, key, toId):
        return self.proxies[toId].get(key, fromId)
    
    def addDataToId(self, key, value, toId):
        self.object.postDistributed(key, value, toId)
    
    def addDataGeneral(self, key, value):
        self.object.post(key, value)

    def deleteData(self, key):
        self.object.delete(key)