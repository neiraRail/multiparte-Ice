import Multiparte

#TODO Agregar n como parametro y ajustar metodos a n.
#TODO Utilizar id y si el valor es una lista, utilizar el id, sino es una lista solo envíar.
class NodoI(Multiparte.Nodo):
    '''Contiene un objeto data que puede ser accedido por el método get'''
    def __init__(self, data):
        self.data = data

    def get(self, key, id):
        if key in self.data:
            return str(self.data[key])
        else:
            raise Multiparte.NodoError("No existe key")
    
    def post(self, key, value, id):
        self.data[key] = value
        return True
