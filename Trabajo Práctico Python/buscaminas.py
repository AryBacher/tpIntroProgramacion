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

# def calcular_numeros2(tablero: list[list[int]]) -> None:
#     tablero_nuevo: list[list[int]] = tablero
#     for fila in tablero:
#         for elemento in range(len(fila)):
#             if fila[elemento] == 0:
#                 fila[elemento] = cantidad_elementos(tablero,(-1))
    
#     return tablero_nuevo
            
    
# def cantidad_elementos(matriz: list[list[int]], n: int) -> int:
#     cantidad: int = 0
#     for fila in matriz:
#         for elemento in range(len(fila)):
#             if fila[elemento] == n:
#                 cantidad += 1
#     return cantidad 

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
    
    descubrir_celdas_seguras(estado, fila, columna)

    if todas_celdas_seguras_descubiertas(estado):
        estado['juego_terminado'] = True

def mostrar_todas_las_minas(estado: EstadoJuego) -> None:
    for i in range(estado['filas']):
        for j in range(estado['columnas']):
            if estado['tablero'][i][j] == -1:
                estado['tablero_visible'][i][j] = BOMBA

# Falta terminar, me mareé en el medio
def descubrir_celdas_seguras(estado: EstadoJuego, fila: int, columna: int) -> None:
    cola: Cola[tuple[int, int]] = Cola()
    cola.put((fila, columna))
    visitadas: list[tuple[int, int]] = []

    while not cola.empty():
        fila_actual, columna_actual = cola.get()
        
        # Verificar límites del tablero
        if not (0 <= fila_actual < estado['filas'] and 0 <= columna_actual < estado['columnas']):
            continue
            
        if ((fila_actual, columna_actual) in visitadas or 
            estado['tablero_visible'][fila_actual][columna_actual] != VACIO or 
            estado['tablero'][fila_actual][columna_actual] == -1):
            continue
            
        visitadas.append((fila_actual, columna_actual))
        estado['tablero_visible'][fila_actual][columna_actual] = str(estado['tablero'][fila_actual][columna_actual])
        
        if estado['tablero'][fila_actual][columna_actual] == 0:
            for i in range(fila_actual - 1, fila_actual + 2):
                for j in range(columna_actual - 1, columna_actual + 2):
                    if (i, j) != (fila_actual, columna_actual):
                        cola.put((i, j))


def todas_celdas_seguras_descubiertas(estadoTablero: EstadoJuego['tablero'], estadoTableroVisible: EstadoJuego['tablero_visible']) -> bool:
    for i in range(len(estadoTablero)):
        for j in range(len(estadoTablero[0])):
            if estadoTablero[i][j] != -1 and estadoTableroVisible[i][j] == VACIO:
                return False
    return True
        

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



def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    return


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False
