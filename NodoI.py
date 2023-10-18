import ZIceComms

#TODO Agregar n como parametro y ajustar metodos a n.
#TODO Utilizar id y si el valor es una lista, utilizar el id, sino es una lista solo envíar.
class NodoI(ZIceComms.Nodo):
    '''Contiene un objeto data que puede ser accedido por el método get'''
    def __init__(self, data):
        self.data = data

    def get(self, key, id, current=None):
        if key in self.data:
            if type(self.data[key]) == list:
                return str(self.data[key][id])
            else:
                return str(self.data[key])
        else:
            raise ZIceComms.NodoError("No existe key")
    
    def post(self, key, value, current=None):
        self.data[key] = value
        return True
    
    def postDistributed(self, key, value, id):
        if not key in self.data:    
            self.data[key] = None
        if type(self.data[key]) != list:
            self.data[key] = []
        if len(self.data[key]) <= id:
            while len(self.data[key]) <= id:
                self.data[key].append(None)
                
        self.data[key][id] = value

    def delete(self, key):
        if key in self.data:
            del self.data[key]