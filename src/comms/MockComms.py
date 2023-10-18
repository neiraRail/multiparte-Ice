from src.comms.CommsHandler import CommsHandler

class MockComms(CommsHandler):
    def __init__(self, id, n):
        super().__init__(id)
        self.mockPartes = [[0 for i in range(n)] for i in range(n)]
    
    def get(self, fromId, key, toId):
        if key == "parte":
            return self.mockPartes[toId][fromId]
        if key == "sumaParcial":
            return self.mockPartes[self.id][toId]
        if key == "total":
            return sum(self.mockPartes[self.id])


    def addDataToId(self, key, value, id):
        if key == "parte":
            self.mockPartes[self.id][id] = value
        return True
    
    def addDataGeneral(self, key, value):
        return True
    
    def deleteData(self, key):
        return True