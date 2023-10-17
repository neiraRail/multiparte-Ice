from NodoI import NodoI
import logging
import sys, Ice, random
import threading
import Multiparte
from Comunicator import Comunicator 

if "--debug" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


class NodoMP:
    def __init__(self, id: int, comm: Comunicator, n=3):
        self.id = id
        self.n = n
        self.comm = comm

        self.key = None
        self.partes = []
        self.sumaParcial = None
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
        self.partes = partes

    def setSumaParcial(self, sumaParcial):
        self.comm.addDataGeneral("sumaParcial", sumaParcial)
        self.sumaParcial = sumaParcial

    def setSumaFinal(self, sumaFinal):
        self.comm.addDataGeneral("total", sumaFinal)
        self.sumaTotal = sumaFinal

    def borrarSumaFinal(self):
        self.comm.deleteData("total")
        self.sumaTotal = None

    def borrarSumaParcial(self):
        self.comm.deleteData("sumaParcial")
        self.sumaParcial = None

    def borrarPartes(self):
        self.comm.deleteData("parte")
        self.partes = []

    def sumar(self, key):
        self.key = key
        self.separarKey()
        logging.debug("Mi número secreto (s) es {}".format(self.key))
        logging.debug("Las partes que voy a compartir son {}".format(self.partes))

        # Pide todas las partes incluyendo la propia.
        otrasPartes = []
        otrasPartes.append(self.partes[self.id])
        for i in range(self.n):
            parteRecibida = False
            while not parteRecibida:
                try:
                    parte = self.comm.get(self.id, "parte", i)
                    otrasPartes.append(parte)
                except Multiparte.NodoError as e:
                    logging.debug(e)
                except Ice.ConnectionRefusedException as e:
                    sys.exit()
                else:
                    parteRecibida = True

        # for i, proxy in enumerate(self.proxies):
        #     parteRecibida = False
        #     numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
        #     while not parteRecibida:
        #         try:
        #             logging.debug("Necesito la parte de {}".format(numeroDelNodo))
        #             parte = proxy.getMyPart("")
        #             otrasPartes.append(parte)
        #             logging.debug("que es {}".format(parte))
        #         except Multiparte.NotReadyError as e:
        #             logging.debug(e)
        #             # time.sleep(0.1)
        #         except Ice.ConnectionRefusedException as e:
        #             logging.debug(e)
        #             sys.exit()
        #         else:
        #             parteRecibida = True

        self.borrarSumaFinal()  # Importante borrar para no enviar por accidente
        self.setSumaParcial(sum(otrasPartes))
        logging.debug("Las partes que he recolectado son: {}".format(otrasPartes))
        logging.debug("Y suman {}".format(self.sumaParcial))

        # Suma las partes de otros y genera su suma parcial
        sumasParciales = []
        sumasParciales.append(self.sumaParcial)

        for i in range(self.n):
            sumaRecibida = False
            while not sumaRecibida:
                try:
                    suma = self.comm.get(self.id, "sumaParcial", i)
                    sumasParciales.append(suma)
                except Multiparte.NodoError as e:
                    logging.debug(e)
                    # time.sleep(0.1)
                except Ice.ConnectionRefusedException as e:
                    logging.debug(e)
                    sys.exit()
                else:
                    sumaRecibida = True

        # # Solcita las sumas parciales de los otros
        # for i, proxy in enumerate(self.proxies):
        #     sumaRecibida = False
        #     numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
        #     while not sumaRecibida:
        #         try:
        #             logging.debug(
        #                 "Necesito la suma parcial de {}".format(numeroDelNodo)
        #             )
        #             suma = proxy.getPartialSum()
        #             sumasParciales.append(suma)
        #             logging.debug("que es {}".format(suma))
        #         except Multiparte.NotReadyError as e:
        #             logging.debug(e)
        #             # time.sleep(0.1)
        #         except Ice.ConnectionRefusedException as e:
        #             logging.debug(e)
        #             sys.exit()
        #         else:
        #             sumaRecibida = True

        self.borrarPartes()  # Es importante borrar partes para que en la siguiente iteración no se envíe una parte anterior por accidente
        self.setSumaFinal(sum(sumasParciales))
        logging.debug("Las sumas que he recolectado son: {}".format(sumasParciales))
        logging.debug("La suma final es: {}".format(self.sumaTotal))

        sumasTotales = []
        sumasTotales.append(self.sumaTotal)
        for i in range(self.n):
            sumaTotalRecibida = False
            while not sumaTotalRecibida:
                try:
                    total = self.comm.get(self.id, "total", i)
                    sumasTotales.append(total)
                except Multiparte.NodoError as e:
                    logging.debug(e)
                    # time.sleep(0.1)
                except Ice.ConnectionRefusedException as e:
                    logging.debug(e)
                    sys.exit()
                else:
                    sumaTotalRecibida = True

        # for i, proxy in enumerate(self.proxies):
        #     sumaTotalRecibida = False
        #     numeroDelNodo = proxy.ice_toString().split(" ")[0].split("_")[1]
        #     while not sumaTotalRecibida:
        #         try:
        #             logging.debug("Necesito la suma final de {}".format(numeroDelNodo))
        #             total = proxy.getFinalSum()
        #             sumasTotales.append(total)
        #             logging.debug("que es {}".format(total))
        #         except Multiparte.NotReadyError as e:
        #             logging.debug(e)
        #             # time.sleep(0.1)
        #         except Ice.ConnectionRefusedException as e:
        #             logging.debug(e)
        #             sys.exit()
        #         else:
        #             sumaTotalRecibida = True

        self.borrarSumaParcial()  # Es importante borrar sumaParcial para que no se envíe por accidente en la siguiente iteración de otro nodo
        assert all(
            x == sumasTotales[0] for x in sumasTotales
        )  # Si una de las sumas totales no coincide se detiene la ejecución

        logging.debug("Suma total es: {}".format(self.sumaTotal))
        while self.nroSumasCheckeadas < self.n:
            pass
        return self.sumaTotal