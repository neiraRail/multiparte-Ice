import sys, random, logging
from src.sum.SumHandler import SumHandler

class TriviumNode():
    def __init__(self, id, sumHandler: SumHandler):
        self.id = id
        self.sumHandler = sumHandler
        self.secreto = None

        self.vector = self.generarVector(id)
        self.intermedio1 = [66,69,66][id]
        self.intermedio2 = [69,78,87][id]

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

    
    def run(self):
        while True:
            self.secreto = self.primerXor()
            St = self.sumHandler.sumar(self.secreto) % 2
            logging.debug("GEN: Voy a soltar el bit: {}".format(St))
            yield St
            self.moverVector(St, self.secreto)

            if "--debug" in sys.argv:
                input("Presiona Enter para continuar...")