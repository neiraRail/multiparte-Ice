# Trivium multiparte

Primero crear un ambiente virtual e instalar dependencias

```
python -m venv env
.\env\Scripts\activate //para windows
source env\bin\activate //para linux

pip install -r requirements.txt
```

En la carpeta **demos/**  hay 2 ejemplos: *testSuma* y *testTrivium*, para ejecutarlos correctamente se debe estar posicionado en la carpeta base del proyecto

## TestSuma
```
python -m demos.testSuma -id <id> -v <valor> [-n <nodos>] [--debug]
```

- **id** es el número que le corresponde al nodo, debe ser desde el 0 a n.
- **valor** es el valor a sumar
- **nodos** es el número de nodos que van a participar en la suma, por defecto es 3.
- **--debug** es una flag opcional para imprimir en terminal todos los detalles de los estados internos de cada nodo: partes, sumas parciales, suma total, intentos de solicitud e **importante**, requerirá presionar Enter para avanzar en cada iteración.

## TestTrivium
```
python -m demos.testTrivium -id <id> [--debug]
```
- **id** es el número que le corresponde al nodo, debe ser desde el 0 al 2.
- **--debug** es una flag opcional para imprimir en terminal todos los detalles de los estados internos de cada nodo: partes, sumas parciales, suma total, intentos de solicitud e **importante**, requerirá presionar Enter para avanzar en cada iteración.

