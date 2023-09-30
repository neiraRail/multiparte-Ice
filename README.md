# Trivium multiparte

Primero crear un ambiente virtual e instalar dependencias

```
python -m venv env
.\env\Scripts\activate //para windows
source env\bin\activate //para linux

pip install -r requirements.txt
```

Se deben ejecutar 3 nodos en 3 terminales distintas utilizando el comando 

```
python NodoI.py <id> [--debug]
```

- **id** es el número que le corresponde al nodo, debe ser desde el 0 al 2.

- **--debug** es una flag opcional para imprimir en terminal todos los detalles de los estados internos de cada nodo: partes, sumas parciales, suma total, intentos de solicitud e **importante**, requerirá presionar Enter para avanzar en cada iteración.

Cada nodo, dependiendo del id se corresponderá con A, B o C.
