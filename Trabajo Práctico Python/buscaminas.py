import random
from typing import Any
import os
from queue import Queue as Cola
from typing import TextIO

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))


# Ejercicio 1
def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    """Crea una matriz de filas x columnas y coloca minas en posiciones aleatorias"""
    matriz: list[list[int]] = []

    for _ in range(filas):
        fila: list = []
        for _ in range(columnas):
            fila.append(0)
        matriz.append(fila)

    # Creamos una lista con todas las posiciones (fila, columna) en matriz y eligimos 
    # de esa lista, cantidad de minas elementos, y ahí colocamos las minas
    posicionesMatriz: list[tuple[int, int]] = posiciones_matriz(matriz)
    posicionesMinas: list[tuple[int, int]] = random.sample(posicionesMatriz, minas)

    for fila, columna in posicionesMinas:
        matriz[fila][columna] = -1

    return matriz

def posiciones_matriz(matriz: list[list[int]]) -> list[tuple[int, int]]:
    """Toma una matriz y devuelve todas sus posiciones de la manera (fila columna)
    dentro de una lista"""
    posicionesMatriz: list[tuple[int, int]] = []
    for numFila in range(len(matriz)):
        for numColumna in range(len(matriz[0])):
            posicionesMatriz.append((numFila, numColumna))

    return posicionesMatriz

# Ejercicio 2
def calcular_numeros(tablero: list[list[int]]) -> None:
    """A partir de un tablero, calcula la cantidad de minas adyacentes
    de todas las posiciones de ese tablero, que no contienen una mina"""
    for num_fila in range(len(tablero)):
        for num_columna in range(len(tablero[0])):
            if tablero[num_fila][num_columna] == 0: 
                tablero[num_fila][num_columna] = cant_minas_adyacentes(tablero, (num_fila, num_columna))

def cant_minas_adyacentes(tablero: list[list[int]], posicion: tuple[int, int]) -> int:
    """Toma un tablero y una posicion, y cuenta cuántas minas adyacentes tiene
    esa posición en el tablero"""
    elementosAdyacentes: list[tuple[int, int]] = elementos_adyacentes(tablero, posicion)
    cantMinasAdyacentes: int = 0

    for numFila, numColumna in elementosAdyacentes:
        if tablero[numFila][numColumna] == -1: cantMinasAdyacentes += 1

    return cantMinasAdyacentes

def elementos_adyacentes(tablero: list[list[int]], posicion: tuple[int, int]) -> list[tuple[int, int]]:
    """A partir de una posición en un tablero, te devuelve todas sus posiciones
    adyacentes en ese tablero. Por ejemplo a partir de un tablero de 3x3, y a partir 
    de la posición (1, 1), devuelve [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), 
    (2, 0), (2, 1), (2, 2)]]"""
    elementosAdyacentes: list[tuple[int, int]] = []
    posicionesMatriz: list[tuple[int, int]] = posiciones_matriz(tablero)

    for numFila in range(posicion[0] - 1, posicion[0] + 2):
        for numColumna in range(posicion[1] - 1, posicion[1] + 2):
            if (numFila, numColumna) == (posicion[0], posicion[1]): continue
            if (numFila, numColumna) in posicionesMatriz:
                elementosAdyacentes.append((numFila, numColumna))

    return elementosAdyacentes

# Ejercicio 3
def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    """Cuando se corre esta función, se crean y se inicializan todos los valores de estado.
    Esta función se corre cuando el juego está iniciando y se crea un tablero de manera
    aleatoria a partir de una cantidad de filas, columnas y minas mediante las funciones
    colocar_minas y calcular_numeros"""
    estado: EstadoJuego = {}
    estado['filas'] = filas
    estado['columnas'] = columnas
    estado['minas'] = minas

    juegoVacio: list[list[int]] = []
    for _ in range(filas):
        fila: list = []
        for _ in range(columnas):
            fila.append(VACIO)
        juegoVacio.append(fila)

    estado['tablero_visible'] = juegoVacio
    estado['juego_terminado'] = False

    tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
    calcular_numeros(tablero)
    estado['tablero'] = tablero

    return estado

# Ejercicio 4
def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    """Devuelve el tablero visibile del juego"""
    estadoTableroVisible = estado['tablero_visible']
    return estadoTableroVisible

# Ejercicio 5
def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """A partir de una posición, es decir, una fila y una columna 
    marca en el tablero visible, es decir, en el tablero que ve el usuario, 
    una bandera en caso de que la posición sea vacía o un vacío, si en la 
    posición había una bandera. Esto vendría a representar cuando un usuario
    hace click derecho en una casilla."""
    if estado['tablero_visible'][fila][columna] == VACIO:
        estado['tablero_visible'][fila][columna] = BANDERA
    elif estado['tablero_visible'][fila][columna] == BANDERA:
        estado['tablero_visible'][fila][columna] = VACIO

# Ejercicio 6
def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """Luego de que el usuario hace click izquierdo en una casilla, se entra a esta función.
    Si el usuario ha oprimido una bomba, se muestran todas las minas y se termina el juego.
    
    Si el usuario no ha oprimido una bomba, se divide en dos casos, si la casilla 
    contiene un 0, o un número mayor a 0. 
    
    Si es un número mayor a 0, solo muestra esa casilla en el tablero visible
    para que el usuario pueda verla y el juego continúa.
    
    Si esa casilla es un 0, luego se buscarán todas las casillas adyacentes a esa posición
    que no sean ceros, y si alguna de esas casillas adyacentes es un 0, seguimos buscando
    casillas adyacentes hasta que ninguna sea un 0. Luego, mostramos todas esas casillas
    y el juego continúa.
    
    Finalmente, si todas las celdas que no son bombas fueron descubiertas, 
    es decir, si el usuario puede ver la cantidad de minas adyacentes en todas las celdas,
    menos en las que hay una mina, el juego termina"""
    
    if estado['juego_terminado'] == True:
        return
    
    if estado['tablero'][fila][columna] == -1:
        estado['juego_terminado'] = True
        mostrar_todas_las_minas(estado)
        return
    
    caminosDescubiertos: list[list[tuple[int, int]]] = caminos_descubiertos(estado['tablero'], estado['tablero_visible'], fila, columna)

    for camino in caminosDescubiertos:
        for fila, columna in camino:
            estado['tablero_visible'][fila][columna] = str(estado['tablero'][fila][columna])

    if todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible']):
        estado['juego_terminado'] = True

def mostrar_todas_las_minas(estado: EstadoJuego) -> None:
    """Recorremos el tablero y le mostramos al usuario mediante el tablero visible,
    todas las posiciones de las minas. Esto sucede cuando el usuario ya ha perdido."""
    for i in range(estado['filas']):
        for j in range(estado['columnas']):
            if estado['tablero'][i][j] == -1:
                estado['tablero_visible'][i][j] = BOMBA

def todas_celdas_seguras_descubiertas(estadoTablero: list[list[int]], estadoTableroVisible: list[list[int]]) -> bool:
    """Recorremos todas las posiciones del tablero y nos fijamos lo siguiente:

    Si una casilla no tiene una mina, el usuario debe poder ver en esa casilla 
    la cantidad de minas adyacentes a esa posición
    
    Si una casilla tiene una mina, el usuario debe poder ver una casilla vacía o una bandera
    
    Si estas dos condiciones se cumplen para todas las casillas del tablero, esto significa
    que el usuario ya ha descubierto todas las casillas seguras, por lo que ha ganado el juego
    
    Si para alguna casilla, esto no se cumple, el juego continúa"""

    for i in range(len(estadoTablero)):
        for j in range(len(estadoTablero[0])):
            if estadoTablero[i][j] != -1 and estadoTableroVisible[i][j] == str(estadoTablero[i][j]):
                continue
            if estadoTablero[i][j] == -1 and (estadoTableroVisible[i][j] == VACIO or estadoTableroVisible[i][j] == BANDERA):
                continue
            return False
    return True    

def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f: int, c: int) -> list[list[tuple[int, int]]]:
    """
    Encuentra todos los caminos posibles desde la posición (f,c) que cumplan las condiciones:
    - Secuencias de posiciones válidas sin repetidos
    - Primer elemento es (f,c)
    - Si |s| > 1, todos los elementos salvo el último deben tener valor 0 en tablero
    - No debe haber posiciones con BANDERA en tablero_visible
    - Elementos contiguos deben ser adyacentes
    """
    caminos: list[list[tuple[int, int]]] = []

    if tablero[f][c] == 0:
        # Primero obtenemos todos los caminos adyacentes a la posición a analizar.
        # Si la posición que tenemos es (1, 1), los caminos obtenidos serán de la forma:
        # [[(1, 1), (0, 0)], [(1, 1), (0, 1)], [(1, 1), (0, 2)] ...]
        # Luego, observamos cuantos de esos caminos adyacentes, termina con un 0,
        # esto significaría que, por ejemplo, la posición (1, 1), en estado['tablero'] = 0

        caminosAdyacentes: list[list[tuple[int, int]]] = caminos_adyacentes([(f, c)], tablero, tablero_visible)
        listas_no_terminadas_en_cero: list[list[tuple[int, int]]] = ultimo_elemento_cero(caminosAdyacentes, tablero)

        # Si alguno de los caminos "termina" en 0, entramos al siguiente while y repetimos
        # este proceso la cantidad de veces necesaria hasta que ningún camino "termine" en 0

        while len(listas_no_terminadas_en_cero) != 0:
            nuevosCaminosAdyacentes: list[list[tuple[int, int]]] = []
            for lista in listas_no_terminadas_en_cero:
                caminosAdyacentes.remove(lista)
                nuevosCaminosAdyacentes += caminos_adyacentes(lista, tablero, tablero_visible)

            listas_no_terminadas_en_cero = ultimo_elemento_cero(nuevosCaminosAdyacentes, tablero)
            caminosAdyacentes += nuevosCaminosAdyacentes
        
        caminos = caminosAdyacentes.copy()
    
    else:
        caminos.append([(f, c)])

    return caminos

def caminos_adyacentes(listaDePosiciones: list[tuple[int, int]], tablero: list[list[int]], tablero_visible: list[list[int]]) -> list[tuple[int, int]]:
    """Obtenemos todos los caminos adyacentes a partir de una lista de posiciones.
    
    Por ejemplo, si listaDePosiciones = [(1, 1)], los caminos obtenidos serán de la forma:
    [[(1, 1), (0, 0)], [(1, 1), (0, 1)], [(1, 1), (0, 2)] ...]
    
    Pero, por ejemplo, si listaDePosiciones = [(2, 2), (1, 1)], los caminos obtenidos serán:
    [[(2, 2), (1, 1), (0, 0)], [(2, 2), (1, 1), (0, 1)], [(2, 2), (1, 1), (0, 2)] ...]"""
    
    listaPosicionesAdyacentes: list[list[tuple[int, int]]] = []
    ultimaPosicion = listaDePosiciones[len(listaDePosiciones) - 1]
    posicionesAdyacentes = elementos_adyacentes(tablero, ultimaPosicion)

    for posicionAdyacente in posicionesAdyacentes:
        if tablero_visible[posicionAdyacente[0]][posicionAdyacente[1]] != BANDERA:
            if posicionAdyacente not in listaDePosiciones:
                listaPosicionesAdyacentes.append(listaDePosiciones + [posicionAdyacente])

    return listaPosicionesAdyacentes

def ultimo_elemento_cero(listaPosiciones: list[list[tuple[int, int]]], tablero: list[list[int]]) -> bool:
    """A partir de una lista de posiciones, por ejemplo, la siguiente:
    [[(1, 1), (0, 0)], [(1, 1), (0, 1)], [(1, 1), (0, 2)] ...], chequeamos cual de
    esos caminos termina en 0, es decir, devolvemos todas las listas dentro de
    listasPosiciones tales que 
    estado['tablero'][lista[len(lista) - 1][0]][lista[len(lista) - 1][1]]] = 0"""

    ultimos_elementos: list[tuple[int, int]] = ultimo_elemento_de_todas_listas(listaPosiciones)
    listas_con_cero: list[tuple[int, int]] = []
    contador: int = 0

    for posicion in ultimos_elementos:
        if tablero[posicion[0]][posicion[1]] == 0:
            listas_con_cero.append(listaPosiciones[contador])
        contador += 1

    return listas_con_cero

def ultimo_elemento_de_todas_listas(listas: list[list]) -> list:
    """Para hacer la función de arriba más fácil, obtenemos todos los
    últimos elementos de todas las listas dentro de una lista de listas."""
    ultimos_elementos: list = []

    for lista in listas:
        ultimos_elementos.append(lista[len(lista) - 1])

    return ultimos_elementos

# Ejercicio 7
def verificar_victoria(estado: EstadoJuego) -> bool:
    """El usuario gana si y solo si todas las celdas están descubiertas, de 
    lo contrario, el juego continúa"""
    return todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible'])

# Ejercicio 8
def reiniciar_juego(estado: EstadoJuego) -> None:
    """Cuando el usuario oprime el botón de reiniciar, se inicializan nuevamente todos los
    valores, así como en la función crear_juego. """
    estado['juego_terminado'] = False
    estado['tablero_visible'] = []
    for _ in range(estado['filas']):
        fila: list = []
        for _ in range(estado['columnas']):
            fila.append(VACIO)
        estado['tablero_visible'].append(fila)
    estado['tablero'] = colocar_minas(estado['filas'], estado['columnas'], estado['minas'])
    calcular_numeros(estado['tablero'])

# Ejercicio 9
def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    """Guardamos en dos archivos externos el estado del juego actual:
    
    En tablero.txt guardamos la información no visible para el usuario separada
    por comas y por filas, por ejemplo si el tablero era [[1, 1], [1, 0]] guardamos:
    1,1
    1,0
    
    En tablero_visible.txt guardamos la información visible para el usuario separada
    por comas y por filas, con la particularidad que en donde había un casillero vacío,
    guardamos un '?' y donde había una bandera, guardamos un '*'. 
    Por ejemplo si el tablero visible era [[VACIO, 1], [1, BANDERA]] guardamos:
    ?,1
    1,*
    """
    rutaArchivoTablero = os.path.join(ruta_directorio, "tablero.txt")
    rutaArchivoTableroVisible = os.path.join(ruta_directorio, "tablero_visible.txt")

    archivoTablero: TextIO = open(rutaArchivoTablero, "w", encoding="utf-8")
    archivoTableroVisible: TextIO = open(rutaArchivoTableroVisible, "w", encoding="utf-8")

    for numFila in range(len(estado['tablero'])):
        for numColumna in range(len(estado['tablero'][0])):
            archivoTablero.write(str(estado['tablero'][numFila][numColumna]))
            
            if numColumna != (len(estado['tablero'][0]) - 1):
                archivoTablero.write(',')

        if numFila != (len(estado['tablero']) - 1):
            archivoTablero.write("\n")

    for numFila in range(len(estado['tablero_visible'])):
        for numColumna in range(len(estado['tablero_visible'][0])):
            valorTablero: str = str((estado['tablero_visible'][numFila][numColumna]))

            if valorTablero == BANDERA: archivoTableroVisible.write('*')
            elif valorTablero == VACIO: archivoTableroVisible.write('?')
            else: archivoTableroVisible.write(valorTablero)
            
            if numColumna != (len(estado['tablero_visible'][0]) - 1):
                archivoTableroVisible.write(',')

        if numFila != (len(estado['tablero_visible']) - 1):
            archivoTableroVisible.write("\n")

    archivoTablero.close()
    archivoTableroVisible.close()

# Ejercicio 10
def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    # Verificamos que existan ambos archivos
    if existe_archivo(ruta_directorio, "tablero.txt") == False or existe_archivo(ruta_directorio, "tablero_visible.txt") == False:
        return False
    
    # Leemos los archivos
    ruta_tablero = os.path.join(ruta_directorio, "tablero.txt")
    ruta_tablero_visible = os.path.join(ruta_directorio, "tablero_visible.txt")
    
    archivo_tablero: TextIO = open(ruta_tablero, "r", encoding="utf-8")
    lineas_tablero: list[str] = archivo_tablero.read().strip().split("\n")
    
    archivo_tablero_visible: TextIO = open(ruta_tablero_visible, "r", encoding="utf-8")
    lineas_tablero_visible: list[str] = archivo_tablero_visible.read().strip().split("\n")
    
    archivo_tablero.close()
    archivo_tablero_visible.close()
    
    if len(lineas_tablero) == 0 or len(lineas_tablero_visible) == 0 or len(lineas_tablero) != len(lineas_tablero_visible):
        return False
    
    # Procesar columnas por linea
    columnas_tablero: int = len(lineas_tablero[0].split(","))
    columnas_tablero_visible: int = len(lineas_tablero_visible[0].split(","))
    for i in range(len(lineas_tablero)):
        columnas_linea: list[str] = lineas_tablero[i].split(",")
        columnas_linea_visible: list[str] = lineas_tablero_visible[i].split(",")
        if len(columnas_linea) != columnas_tablero or len(columnas_linea_visible) != columnas_tablero_visible:
            return False
    
    # Validar formato y construir matrices
    tablero_cargado: list[list[int]] = []
    tablero_visible_cargado: list[list[str]] = []
    contador_minas: int = 0
    
    for i in range(len(lineas_tablero)):
        # Validar tablero.txt
        valores_tablero: list[str] = lineas_tablero[i].split(",")
        
        fila_tablero: list[int] = []
        for valor_str in valores_tablero:
            valor: int = int(valor_str)
            if valor == -1:
                contador_minas += 1
            elif valor < 0 or valor > 8:
                return False
            fila_tablero.append(valor)
        
        # Validar tablero_visible.txt
        valores_visible: list[str] = lineas_tablero_visible[i].split(",")
        
        fila_visible: list[str] = []
        for valor_str in valores_visible:
            if valor_str == "*":
                fila_visible.append(BANDERA)
            elif valor_str == "?":
                fila_visible.append(VACIO)
            elif valor_str.isdigit() and 0 <= int(valor_str) <= 8:
                fila_visible.append(valor_str)
            else:
                return False
        
        tablero_cargado.append(fila_tablero)
        tablero_visible_cargado.append(fila_visible)
    
    # Validar que haya al menos una mina
    if contador_minas == 0:
        return False
    
    # Validar que los números en tablero correspondan a minas adyacentes
    for i in range(len(lineas_tablero)):
        for j in range(columnas_tablero):
            if tablero_cargado[i][j] != -1:
                minas_adyacentes_esperadas = cant_minas_adyacentes(tablero_cargado, (i, j))
                if tablero_cargado[i][j] != minas_adyacentes_esperadas:
                    return False
    
    # Validar correspondencia entre tablero y tablero_visible
    for i in range(len(lineas_tablero)):
        for j in range(columnas_tablero):
            valor_visible = tablero_visible_cargado[i][j]
            if valor_visible != BANDERA and valor_visible != VACIO and valor_visible.isdigit():
                if int(valor_visible) != tablero_cargado[i][j]:
                    return False
    
    # Si llegamos aquí, todo es válido - actualizar estado
    estado['filas'] = len(lineas_tablero)
    estado['columnas'] = len(lineas_tablero[0].split(","))
    estado['minas'] = contador_minas
    estado['juego_terminado'] = False
    estado['tablero'] = tablero_cargado
    estado['tablero_visible'] = tablero_visible_cargado
    
    return True

# tablero = [[1, 2, 3, 4, 5, 6, 7],
#            [1, 0, 3, 4, 5, 6, 7],
#            [1, 2, 0, 1, 2, 6, 7],
#            [1, 2, 3, 0, 5, 6, 7],
#            [1, 2, 1, 2, 0, 6, 7],
#            [1, 2, 3, 4, 5, 6, 7],
#            [1, 2, 3, 4, 5, 6, 7]]

# tablero_visible = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], 
#                    [' ', ' ', ' ', ' ', ' ', ' ', ' '], 
#                    [' ', ' ', ' ', ' ', ' ', ' ', ' '], 
#                    [' ', ' ', ' ', ' ', ' ', ' ', ' '], 
#                    [' ', ' ', ' ', ' ', ' ', ' ', ' '], 
#                    [' ', ' ', ' ', ' ', ' ', ' ', ' '], 
#                    [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

# estado: EstadoJuego = {'filas': 7,
#                        'columnas': 7,
#                        'minas': 3,
#                        'tablero': tablero,
#                        'tablero_visible': tablero_visible,
#                        'juego_terminado': False}

# estado = {'filas': 2, 
#           'columnas': 2, 
#           'minas': 1, 
#           'tablero': [[-1,1], [ 1,1]], 
#           'tablero_visible': [[BANDERA,'1'],[' ',' ']],
#           'juego_terminado': False}