class CommsHandler:
    def __init__(self, id):
        self.id = id
        self.data = dict()

    def get(self, fromId, key, toId):
        pass

    def addDataToId(self, key, value, id):
        pass

    def addDataGeneral(self, key, value):
        pass

    def deleteData(self, key):
        pass

class TryAgainException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FatalException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)