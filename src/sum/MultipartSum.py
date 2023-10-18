import logging, sys, random
from src.comms.CommsHandler import CommsHandler, TryAgainException, FatalException

if "--debug" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


class MultipartSum:
    def __init__(self, id: int, commsHandler: CommsHandler, n=3):
        self.id = id
        self.n = n
        self.comm = commsHandler

        self.key = None
        self.sumaTotal = None

        self.nroPartesEnviadas = 0
        self.nroSumasCheckeadas = 0

    def separarKey(self):
        partes = []
        for i in range(self.n):
            if i != self.id:
                parte = random.randint(-10, 10)
                partes.append(parte)
                self.comm.addDataToId("parte", parte, i)
        miParte = self.key - sum(partes)
        partes.append(miParte)
        self.comm.addDataToId("parte", miParte, self.id)

        self.nroPartesEnviadas = 0
        self.nroSumasCheckeadas = 0

    def setSumaParcial(self, sumaParcial):
        self.comm.addDataGeneral("sumaParcial", sumaParcial)

    def setSumaFinal(self, sumaFinal):
        self.comm.addDataGeneral("total", sumaFinal)

    def borrarSumaFinal(self):
        self.comm.deleteData("total")

    def borrarSumaParcial(self):
        self.comm.deleteData("sumaParcial")

    def borrarPartes(self):
        self.comm.deleteData("parte")

    def sumar(self, key):
        self.key = key
        self.separarKey()
        logging.debug("Mi número secreto (s) es {}".format(self.key))

        # Pide todas las partes incluyendo la propia.
        otrasPartes = []
        for i in range(self.n):
            parteRecibida = False
            while not parteRecibida:
                try:
                    parte = self.comm.get(self.id, "parte", i)
                    otrasPartes.append(parte)
                except TryAgainException as e:
                    logging.debug(e)
                except FatalException as e:
                    sys.exit()
                else:
                    parteRecibida = True
        
        self.borrarSumaFinal()  # Importante borrar para no enviar por accidente
        self.setSumaParcial(sum(otrasPartes))
        logging.debug("Las partes que he recolectado son: {}".format(otrasPartes))

        # Suma las partes de otros y genera su suma parcial
        sumasParciales = []
        for i in range(self.n):
            sumaRecibida = False
            while not sumaRecibida:
                try:
                    suma = self.comm.get(self.id, "sumaParcial", i)
                    sumasParciales.append(suma)
                except TryAgainException as e:
                    logging.debug(e)
                    # time.sleep(0.1)
                except FatalException as e:
                    logging.debug(e)
                    sys.exit()
                else:
                    sumaRecibida = True

        self.borrarPartes()  # Es importante borrar partes para que en la siguiente iteración no se envíe una parte anterior por accidente
        self.setSumaFinal(sum(sumasParciales))
        logging.debug("Las sumas que he recolectado son: {}".format(sumasParciales))
        
        sumasTotales = []
        for i in range(self.n):
            sumaTotalRecibida = False
            while not sumaTotalRecibida:
                try:
                    total = self.comm.get(self.id, "total", i)
                    sumasTotales.append(total)
                except TryAgainException as e:
                    logging.debug(e)
                    # time.sleep(0.1)
                except FatalException as e:
                    logging.debug(e)
                    sys.exit()
                else:
                    sumaTotalRecibida = True
        
        self.borrarSumaParcial()  # Es importante borrar sumaParcial para que no se envíe por accidente en la siguiente iteración de otro nodo
        assert all(
            x == sumasTotales[0] for x in sumasTotales
        )  # Si una de las sumas totales no coincide se detiene la ejecución

        # while self.nroSumasCheckeadas < self.n:
        #     pass
        return self.comm.get(self.id, "total", self.id)