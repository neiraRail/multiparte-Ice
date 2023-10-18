from SumHandler import SumHandler

class MockSum(SumHandler):
    def __init__(self):
        super().__init__()
    
    def sumar(self, myNumber):
        return myNumber
