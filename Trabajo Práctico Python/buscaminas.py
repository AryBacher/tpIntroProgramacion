import random
from typing import Any
import os
from queue import Queue as Cola

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
    matriz: list[list[int]] = []

    for _ in range(filas):
        fila: list = []
        for _ in range(columnas):
            fila.append(0)
        matriz.append(fila)

    posicionesMatriz: list[tuple[int, int]] = posiciones_matriz(matriz)
    posicionesMinas: list[tuple[int, int]] = random.sample(posicionesMatriz, minas)

    for fila, columna in posicionesMinas:
        matriz[fila][columna] = -1
    
    return matriz

def posiciones_matriz(matriz: list[list[int]]) -> list[tuple[int, int]]:
    posicionesMatriz: list[tuple[int, int]] = []
    for numFila in range(len(matriz)):
        for numColumna in range(len(matriz[0])):
            posicionesMatriz.append((numFila, numColumna))

    return posicionesMatriz

# Ejercicio 2
def calcular_numeros(tablero: list[list[int]]) -> None:
    for num_fila in range(len(tablero)):
        for num_columna in range(len(tablero[0])):
            if tablero[num_fila][num_columna] == 0: 
                tablero[num_fila][num_columna] = cant_minas_adyacentes(tablero, (num_fila, num_columna))


def elementos_adyacentes(tablero: list[list[int]], posicion: tuple[int, int]) -> list[tuple[int, int]]:
    elementosAdyacentes: list[tuple[int, int]] = []
    posicionesMatriz: list[tuple[int, int]] = posiciones_matriz(tablero)

    for numFila in range(posicion[0] - 1, posicion[0] + 2):
        for numColumna in range(posicion[1] - 1, posicion[1] + 2):
            if (numFila, numColumna) == (posicion[0], posicion[1]): continue
            if (numFila, numColumna) in posicionesMatriz:
                elementosAdyacentes.append((numFila, numColumna))

    return elementosAdyacentes

def cant_minas_adyacentes(tablero: list[list[int]], posicion: tuple[int, int]) -> int:
    elementosAdyacentes: list[tuple[int, int]] = elementos_adyacentes(tablero, posicion)
    cantMinasAdyacentes: int = 0

    for numFila, numColumna in elementosAdyacentes:
        if tablero[numFila][numColumna] == -1: cantMinasAdyacentes += 1

    return cantMinasAdyacentes

# Ejercicio 3
def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
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
    estadoTableroVisible = estado['tablero_visible']
    return estadoTableroVisible

# Ejercicio 5
def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if estado['tablero_visible'][fila][columna] == VACIO:
        estado['tablero_visible'][fila][columna] = BANDERA
    elif estado['tablero_visible'][fila][columna] == BANDERA:
        estado['tablero_visible'][fila][columna] = VACIO

# Ejercicio 6
def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if estado['juego_terminado'] == True:
        return
    
    if estado['tablero'][fila][columna] == -1:
        estado['juego_terminado'] = True
        mostrar_todas_las_minas(estado)
        return
    
    if todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible']):
        estado['juego_terminado'] = True

    caminosDescubiertos: list[list[tuple[int, int]]] = caminos_descubiertos(estado['tablero'], estado['tablero_visible'], fila, columna)

    for camino in caminosDescubiertos:
        for fila, columna in camino:
            estado['tablero_visible'][fila][columna] = str(estado['tablero'][fila][columna])

def mostrar_todas_las_minas(estado: EstadoJuego) -> None:
    for i in range(estado['filas']):
        for j in range(estado['columnas']):
            if estado['tablero'][i][j] == -1:
                estado['tablero_visible'][i][j] = BOMBA

def todas_celdas_seguras_descubiertas(estadoTablero: list[list[int]], estadoTableroVisible: list[list[int]]) -> bool:
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
        caminosAdyacentes: list[list[tuple[int, int]]] = caminos_adyacentes([(f, c)], tablero, tablero_visible)
        listas_no_terminadas_en_cero: list[list[tuple[int, int]]] = ultimo_elemento_no_cero(caminosAdyacentes, tablero)
        #print("Caminos Adyacentes", caminosAdyacentes)
        #print()
        #print("Listas No Terminadas En Cero", listas_no_terminadas_en_cero)

        while len(listas_no_terminadas_en_cero) != 0:
            nuevosCaminosAdyacentes: list[list[tuple[int, int]]] = []
            for lista in listas_no_terminadas_en_cero:
                caminosAdyacentes.remove(lista)
                nuevosCaminosAdyacentes += caminos_adyacentes(lista, tablero, tablero_visible)

            listas_no_terminadas_en_cero = ultimo_elemento_no_cero(nuevosCaminosAdyacentes, tablero)
            caminosAdyacentes += nuevosCaminosAdyacentes

            #print()
            #print("Caminos Adyacentes 2", caminosAdyacentes)
        
        caminos = caminosAdyacentes.copy()

        # ESTO NO ESTÁ TERMINADO
        # Pasos:
        
        # En el medio, chequear que en la posición en el tablero, no haya una bandera. 
        
        # Hacer una función (la llamo función 1), que dada una lista de tuplas de posiciones y un tablero, te devuelve una lista de tuplas de la manera: (tupla a1 de tupla original,..., tupla an de tupla original, posicion adyacente a tupla an)
        
        # Hacer una función (la llamo función 2), que dada una lista de tuplas de dos elementos, devuelva true si para todas las tuplas, se cumple que tablero[tupla[1]][tupla[2]] # 0
        
        # Si esa función es verdadera, significa que alrededor de mi posición 
        # no hay ceros, y devolvemos esa lista de tuplas como caminos
        
        # Si hay alguna tupla cuyo ultimo elemento tenga como valor en el tablero un 0,
        # saco ese elemento de la lista, y hago la función 1, con la lista de tuplas 
        
        # (Ej: con [(3, 3), (2, 2)], y quedaría 
        # [[(3, 3), (2, 2), (1, 1)], [(3, 3), (2, 2), (1, 2)]...])
        
        # Repito este proceso hasta que la función 2 me devuelva True.
    
    else:
        caminos.append([(f, c)])

    return caminos

def caminos_adyacentes(listaDePosiciones: list[tuple[int, int]], tablero: list[list[int]], tablero_visible: list[list[int]]) -> list[tuple[int, int]]:
    listaPosicionesAdyacentes: list[tuple[int, int]] = []
    ultimaPosicion = listaDePosiciones[len(listaDePosiciones) - 1]
    posicionesAdyacentes = elementos_adyacentes(tablero, ultimaPosicion)

    for posicionAdyacente in posicionesAdyacentes:
        if tablero_visible[posicionAdyacente[0]][posicionAdyacente[1]] != BANDERA:
            if posicionAdyacente not in listaDePosiciones:
                listaPosicionesAdyacentes.append(listaDePosiciones + [posicionAdyacente])

    return listaPosicionesAdyacentes

def ultimo_elemento_no_cero(listaPosiciones: list[list[tuple[int, int]]], tablero: list[list[int]]) -> bool:
    ultimos_elementos: list[tuple[int, int]] = ultimo_elemento_de_todas_listas(listaPosiciones)
    listas_con_cero: list[tuple[int, int]] = []
    contador: int = 0

    for posicion in ultimos_elementos:
        if tablero[posicion[0]][posicion[1]] == 0:
            listas_con_cero.append(listaPosiciones[contador])
        contador += 1

    return listas_con_cero

def ultimo_elemento_de_todas_listas(listas: list[list]) -> list:
    ultimos_elementos: list = []

    for lista in listas:
        ultimos_elementos.append(lista[len(lista) - 1])

    return ultimos_elementos

# def elementos_diagonales_adyacentes(tablero: list[list[int]], fila: int, columna: int) -> list[tuple[int, int]]:
#     posicionesAdyacentes: list[tuple[int, int]] = elementos_adyacentes(tablero, (fila, columna))
#     posicionesAdyacentesCopia = posicionesAdyacentes.copy()

#     for f, c in posicionesAdyacentesCopia:
#         if fila == f or columna == c: posicionesAdyacentes.remove((f, c))

#     return posicionesAdyacentes

# Ejercicio 7
def verificar_victoria(estado: EstadoJuego) -> bool:
    return todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible'])

# Ejercicio 8
def reiniciar_juego(estado: EstadoJuego) -> None:
    estado['juego_terminado'] = False
    estado['tablero_visible'] = []
    for _ in range(estado['filas']):
        fila: list = []
        for _ in range(estado['columnas']):
            fila.append(VACIO)
        estado['tablero_visible'].append(fila)
    estado['tablero'] = colocar_minas(estado['filas'], estado['columnas'], estado['minas'])

# Ejercicio 9
def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    rutaArchivoTablero = os.path.join(ruta_directorio, "tablero.txt")
    rutaArchivoTableroVisible = os.path.join(ruta_directorio, "tablero_visible.txt")

    archivoTablero = open(rutaArchivoTablero, "w", encoding="utf-8")
    archivoTableroVisible = open(rutaArchivoTableroVisible, "w", encoding="utf-8")

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

def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False

tablero = [[1, 2, 3, 4, 5, 6, 7],
           [1, 0, 3, 4, 5, 6, 7],
           [1, 2, 0, 1, 2, 6, 7],
           [1, 2, 3, 0, 5, 6, 7],
           [1, 2, 1, 2, 0, 6, 7],
           [1, 2, 3, 4, 5, 6, 7],
           [1, 2, 3, 4, 5, 6, 7]]

tablero_visible = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                   [' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                   [' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                   [' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                   [' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                   [' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

estado: EstadoJuego = {'filas': 7,
                       'columnas': 7,
                       'minas': 3,
                       'tablero': tablero,
                       'tablero_visible': tablero_visible,
                       'juego_terminado': False}

# descubrir_celda(estado, 3, 3)

# print()
# print("Tablero: \n")
# for fila in estado['tablero']:
#     print(fila)

# print()
# print("Tablero Visible: \n")
# for fila in estado['tablero_visible']:
#     print(fila)

# print()

estado = {'filas': 2, 
          'columnas': 2, 
          'minas': 1, 
          'tablero': [[-1,1], [ 1,1]], 
          'tablero_visible': [[BANDERA,'1'],[' ',' ']],
          'juego_terminado': False}

guardar_estado(estado, "archivos")
print(estado)