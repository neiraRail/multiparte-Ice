# Suma multiparte

Primero crear un ambiente virtual e instalar dependencias

```
python -m venv env
.\env\Scripts\activate //para windows
source env\bin\activate //para linux

pip install -r requirements.txt
```

Se deben ejecutar 3 nodos en 3 terminales distintas utilizando el comando 

```
python NodoI.py <id> <key>
```

- **id** es el número que le corresponde al nodo, debe ser desde el 0 al 2.
- **key** es el valor secreto del nodo



Los nodos intentaran conectarse al valor 0 si no hay un valor tomaran ese id.
Si ese nodo ya existe, intentará lo mismo con el siguiente y asi...

Una vez tenga su id, intentará establecer conexión con todos los N nodos de la red.




Aun existe el problema de saber con anticipación cuantos nodos hay en la red.