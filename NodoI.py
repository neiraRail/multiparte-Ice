import Multiparte
import random


class NodoI(Multiparte.Nodo):
    def __init__(self, id, n=3):
        # Variables para la suma multiparte
        self.n = n
        self.id = id
        self.key = None
        self.partes = []
        self.sumaParcial = None
        self.sumaTotal = None

        self.nroPartesEnviadas = 0
    
    # Metodos suma multiparte
    def getMyPart(self, mensaje, current=None):
        #TODO: quitar self.nroPartesEnviadas y usar otra estrategia
        if len(self.partes) < self.n:
            raise Multiparte.NotReadyError()

        if self.nroPartesEnviadas == self.n:
            return Multiparte.AllPartsAlreadySended()
        
        tuParte = self.partes[self.nroPartesEnviadas]
        self.nroPartesEnviadas += 1

        return tuParte
    
    def getPartialSum(self, current=None):
        if self.sumaParcial == None:
            raise Multiparte.NotReadyError()
        return self.sumaParcial
    
    def getFinalSum(self, current=None):
        if self.sumaTotal == None:
            raise Multiparte.NotReadyError()
        return self.sumaTotal

    def separarKey(self):
        partes = []
        for _ in range(self.n-1):
            partes.append(random.randint(-10,10))
        partes.append(self.key - sum(partes))
        self.nroPartesEnviadas = 0
        self.partes = partes

    def setKey(self, key):
        self.key = key

    def setSumaParcial(self, sumaParcial):
        self.sumaParcial = sumaParcial
    
    def setSumaFinal(self, sumaFinal):
        self.sumaTotal = sumaFinal

    def borrarSumaFinal(self):
        self.sumaTotal = None
    
    def borrarSumaParcial(self):
        self.sumaParcial = None

    def borrarPartes(self):
        self.partes = []