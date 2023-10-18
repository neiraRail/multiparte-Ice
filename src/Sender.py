from src.trivium.TriviumNode import TriviumNode
# from src.comms.MockComms import MockComms as IceCommsHandler
from src.comms.IceCommsHandler import IceCommsHandler
from src.sum.MultipartSum import MultipartSum, TryAgainException

class Sender:
    def __init__(self, id):
        self.id = id
        self.comms = IceCommsHandler(id, 3)
        
        multiparte = MultipartSum(id, self.comms)
        trivium = TriviumNode(id, multiparte)

        self.randomStream = trivium.run()
        self.bit = next(self.randomStream)

        # Sender config
    
    def startSending(self):
        pass

    def send(self, message, toId: int):
        # Avisar a toId que se le va a enviar
        recieved = False
        while not recieved:
            try:
                recieved = self.comms.post(self.id, "msgu", None, toId)
            except TryAgainException:
                pass
        
        # por cada bit del mensaje generar un bit aleatorio y cruzarlos
        for i, bit in enumerate(message):
            value = int(bit)
            xor = value ^ self.bit
            print("{} ^ {} = {}".format(self.bit, bit, xor))
            if i < len(message) - 1:
                self.comms.post(self.id, "data", str(xor)+"1", toId)
            else:
                self.comms.post(self.id, "data", str(xor)+"0", toId)
                
            self.bit = next(self.randomStream)



sender = Sender(0)
message = input("Numero binario para 1: ")
sender.send(message, 1)
message = input("Numero binario para 2: ")
sender.send(message, 2)
while True:
    pass

