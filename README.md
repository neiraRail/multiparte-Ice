# Trivium multiparte

Primero crear un ambiente virtual e instalar dependencias

```
python -m venv env
.\env\Scripts\activate //para windows
source env\bin\activate //para linux

pip install -r requirements.txt
```

En la carpeta *demos/*  hay ejemplos de aplicaciones, para ejecutarlos correctamente se debe estar posicionado en la carpeta base del proyecto

## TestSuma
Se pueden crear *n* nodos en *n* diferentes terminales y, se conectarán y sumarán secretamente sus valores.
```
python -m demos.testSuma -id <id> -v <valor> [-n <nodos>] [--debug]
```

- **id** es el número que le corresponde al nodo, debe ser desde el 0 a n.
- **valor** es el valor a sumar
- **nodos** es el número de nodos que van a participar en la suma, por defecto es 3.
- **--debug** es una flag opcional para imprimir en terminal todos los detalles de los estados internos de cada nodo: partes, sumas parciales, suma total, intentos de solicitud e **importante**, requerirá presionar Enter para avanzar en cada iteración.

## TestTrivium
Se pueden crear 3 nodos en 3 terminales diferentes y comenzarán a generar un stream de bits aleatorio que es impreso en consola.
```
python -m demos.testTrivium -id <id> [--debug]
```
- **id** es el número que le corresponde al nodo, debe ser desde el 0 al 2.
- **--debug** es una flag opcional para imprimir en terminal todos los detalles de los estados internos de cada nodo: partes, sumas parciales, suma total, intentos de solicitud e **importante**, requerirá presionar Enter para avanzar en cada iteración.

## TestTrPausado
Se puede reemplazar uno o más de los nodos del demo anterior por este ejemplo donde por cada bit nuevo se pide presionar *Enter*. De esta forma se comprueba que los nodos se esperan unos a otros para estar sincronizados.
```
python -m demos.testTrPausado <id>
```
- **id** es el número que le corresponde al nodo, debe ser desde el 0 al 2.
