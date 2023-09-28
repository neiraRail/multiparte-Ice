from NodoI import NodoI
import logging
import sys, Ice, time, traceback
import threading

if "--debug" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

class NodoMP():
    def __init__(self, id):
        self.id = id
        self.server_listo = False
        self.object = None
        self.ic = None

        logging.debug("id es: {}".format(id))
        self.server_thread = threading.Thread(target=self._start_server)
        self.server_thread.daemon = True # Para que finalize cuando el hilo principal muera
        self.server_thread.start()

        while not self.server_listo:
            time.sleep(1)


    def _start_server(self):
        try:
            self.ic = Ice.initialize()
            adapter = self.ic.createObjectAdapterWithEndpoints("NodoAdapter", "default -p 1000{}".format(self.id))
            self.object = NodoI(self.id)
            adapter.add(self.object, self.ic.stringToIdentity("Nodo_{}".format(self.id)))
            adapter.activate()

            self.object.conectarme()

            self.server_listo = True

            self.ic.waitForShutdown()
            adapter.destroy()
        except:
            print("Antesdel keyboard interrupt")
            traceback.print_exc()
        
        if self.ic:
            try:
                self.ic.destroy()
            except:
                traceback.print_exc()
                pass

    

    def sumar(self, secreto):
        suma = self.object.sumar(secreto)
        print("SUMASUMASUMA: {}".format(suma))



nodo = NodoMP(sys.argv[1])
nodo.sumar(2)