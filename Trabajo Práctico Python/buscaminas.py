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
    """Toma una matriz y devuelve todas sus posiciones de la manera (fila, columna)
    dentro de una lista"""
    posicionesMatriz: list[tuple[int, int]] = []
    for numFila in range(len(matriz)):
        for numColumna in range(len(matriz[0])):
            posicionesMatriz.append((numFila, numColumna))

    return posicionesMatriz

# Ejercicio 2
def calcular_numeros(tablero: list[list[int]]) -> None:
    """A partir de un tablero, calcula la cantidad de minas adyacentes
    de todas las posiciones de ese tablero que no contienen una mina"""
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
    
    caminosYCeros: tuple[list[list[tuple[int, int]]], list[tuple[int, int]]] = caminos_descubiertos(estado['tablero'], estado['tablero_visible'], fila, columna)
    caminosDescubiertos: list[list[tuple[int, int]]] = caminosYCeros[0]
    ceros_visitados: list[tuple[int, int]] = caminosYCeros[1]

    for camino in caminosDescubiertos:
        for fila, columna in camino:
            estado['tablero_visible'][fila][columna] = str(estado['tablero'][fila][columna])

    for fila, columna in ceros_visitados:
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

def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f: int, c: int) -> tuple[list[list[tuple[int, int]]], list[tuple[int, int]]]:
    """
    Encuentra todos los caminos posibles desde la posición (f,c) que cumplan las condiciones:
    - Secuencias de posiciones válidas sin repetidos
    - Primer elemento es (f,c)
    - Si |s| > 1, todos los elementos salvo el último deben tener valor 0 en tablero
    - No debe haber posiciones con BANDERA en tablero_visible
    - Elementos contiguos deben ser adyacentes
    """
    caminos: list[list[tuple[int, int]]] = []
    ceros_visitados: list[tuple[int, int]] = []

    if tablero[f][c] == 0:
        # Primero obtenemos todos los caminos adyacentes a la posición a analizar.
        # Si la posición que tenemos es (1, 1), los caminos obtenidos serán de la forma:
        # [[(1, 1), (0, 0)], [(1, 1), (0, 1)], [(1, 1), (0, 2)] ...]
        # Luego, observamos cuantos de esos caminos adyacentes, termina con un 0,
        # esto significaría que, por ejemplo, la posición (1, 1), en estado['tablero'] = 0

        caminosAdyacentes: list[list[tuple[int, int]]] = caminos_adyacentes([(f, c)], tablero, tablero_visible, [])
        listas_terminadas_en_cero: list[list[tuple[int, int]]] = ultimo_elemento_cero(caminosAdyacentes, tablero)
        ceros_visitados = ultimo_elemento_de_todas_listas(listas_terminadas_en_cero)

        # Si alguno de los caminos "termina" en 0, entramos al siguiente while y repetimos
        # este proceso la cantidad de veces necesaria hasta que ningún camino "termine" en 0

        while len(listas_terminadas_en_cero) != 0:
            nuevosCaminosAdyacentes: list[list[tuple[int, int]]] = []
            for lista in listas_terminadas_en_cero:
                caminosAdyacentes.remove(lista)
                nuevosCaminosAdyacentes += caminos_adyacentes(lista, tablero, tablero_visible, ceros_visitados)

            listas_terminadas_en_cero = ultimo_elemento_cero(nuevosCaminosAdyacentes, tablero)
            ceros_visitados_iteracion = ultimo_elemento_de_todas_listas(listas_terminadas_en_cero)
            caminosAdyacentes += nuevosCaminosAdyacentes
            ceros_visitados += ceros_visitados_iteracion
        
        caminos = caminosAdyacentes.copy()
    
    else:
        caminos.append([(f, c)])

    return (caminos, ceros_visitados)

def caminos_adyacentes(listaDePosiciones: list[tuple[int, int]], tablero: list[list[int]], tablero_visible: list[list[int]], ceros_visitados: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Obtenemos todos los caminos adyacentes a partir de una lista de posiciones.
    
    Por ejemplo, si listaDePosiciones = [(1, 1)], los caminos obtenidos serán de la forma:
    [[(1, 1), (0, 0)], [(1, 1), (0, 1)], [(1, 1), (0, 2)] ...]
    
    Pero, por ejemplo, si listaDePosiciones = [(2, 2), (1, 1)], los caminos obtenidos serán:
    [[(2, 2), (1, 1), (0, 0)], [(2, 2), (1, 1), (0, 1)], [(2, 2), (1, 1), (0, 2)] ...]"""
    
    listaPosicionesAdyacentes: list[list[tuple[int, int]]] = []
    ultimaPosicion: tuple[int, int] = listaDePosiciones[len(listaDePosiciones) - 1]
    posicionesAdyacentes: list[tuple[int, int]] = elementos_adyacentes(tablero, ultimaPosicion)

    for posicionAdyacente in posicionesAdyacentes:
        if tablero_visible[posicionAdyacente[0]][posicionAdyacente[1]] != BANDERA:
            if posicionAdyacente not in listaDePosiciones and posicionAdyacente not in ceros_visitados:
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

def ultimo_elemento_de_todas_listas(listas: list[list[tuple[int, int]]]) -> list:
    """Para hacer la función de arriba más fácil, obtenemos todos los
    últimos elementos de todas las listas dentro de una lista de listas."""
    ultimos_elementos: list[tuple[int, int]] = []

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
    valores de estado, así como sucedía en la función crear_juego. """
    estado['juego_terminado'] = False
    estado['tablero_visible'] = []
    for _ in range(estado['filas']):
        fila: list = []
        for _ in range(estado['columnas']):
            fila.append(VACIO)
        estado['tablero_visible'].append(fila)
    # Acá por las dudas chequeamos que el tablero sea diferente
    estado_tablero_previo: list[list[int]] = estado['tablero'].copy()
    estado['tablero'] = colocar_minas(estado['filas'], estado['columnas'], estado['minas'])
    calcular_numeros(estado['tablero'])

    # Hasta que el tablero no cambie, seguimos iterando en este while. En cierto momento,
    # estadísticamente, debería tocar un tablero diferente.
    
    # Aclaración: Es claro que el único caso en el que esto nunca pasaría sería si
    # la cantidad de filas, columnas y minas fuera 1, pero por el requiere de las funciones
    # crear_juego, colocar_minas y calcular_numeros, esto no sería posible. 
    # Y para que se corra la función reiniciar_juego, antes se tienen que correr esas tres
    # funciones, por lo que el while siempre será válido.
    
    while estado_tablero_previo == estado['tablero']:
        estado['tablero'] = colocar_minas(estado['filas'], estado['columnas'], estado['minas'])
        calcular_numeros(estado['tablero'])

# Ejercicio 9
def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    """Guardamos en dos archivos externos el estado del juego actual:
    
    En tablero.txt guardamos la información no visible para el usuario separada
    por comas y por filas, por ejemplo si el tablero era [[1, 1], [1, -1]] guardamos:
    1,1
    1,-1
    
    En tablero_visible.txt guardamos la información visible para el usuario separada
    por comas y por filas, con la particularidad que en donde había un casillero vacío,
    guardamos un '?' y donde había una bandera, guardamos un '*'. 
    Por ejemplo si el tablero visible era [[VACIO, 1], [1, BANDERA]] guardamos:
    ?,1
    1,*
    """
    rutaArchivoTablero: str = os.path.join(ruta_directorio, "tablero.txt")
    rutaArchivoTableroVisible: str = os.path.join(ruta_directorio, "tablero_visible.txt")

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
    """A partir de los valores guardados mediante la función guardar_estado, si se
    cumplen ciertas condiciones, volvemos a cargar esos datos dentro de estado. En caso de que
    no se cumplan esas condiciones, devolvemos False. Si se cumplen, devolvemos True.
    Condiciones:
    - En ruta_directorio no existe alguno de los archivos tablero.txt o tablero visible.txt
    - La cantidad de líneas de cada archivo guardado es igual a estado['filas'], considerando
    una linea cuando la cantidad de caracteres sea mayor a 0.
    - La cantidad de comas (',') por línea es igual a estado['columnas'] - 1.
    - En tablero.txt debe haber al menos un -1, y los valores deben ser -1 ó 
    corresponder a la cantidad de -1 que hay en las posiciones adyacentes, 
    considerando al contenido del archivo como una matriz
    - En tablero visible.txt, solo puede haber números (entre [0; 8]), '*'
    (representa BANDERA) y '?' (representa VACIO), ademas de comas (',') para separar valores. 
    En caso de haber núumeros, estos deben corresponder a los valores en la misma posición
    en el archivo tablero.txt (la iésima línea corresponde a la iésima fila de tablero)."""
    
    # Verificamos que existan ambos archivos
    if existe_archivo(ruta_directorio, "tablero.txt") == False or existe_archivo(ruta_directorio, "tablero_visible.txt") == False:
        return False
    
    # Acá leemos los archivos y después los cerramos porque no los necesitamos más
    ruta_tablero: str = os.path.join(ruta_directorio, "tablero.txt")
    ruta_tablero_visible: str = os.path.join(ruta_directorio, "tablero_visible.txt")
    
    archivo_tablero: TextIO = open(ruta_tablero, "r", encoding="utf-8")
    lineas_tablero: list[str] = archivo_tablero.readlines()
    
    archivo_tablero_visible: TextIO = open(ruta_tablero_visible, "r", encoding="utf-8")
    lineas_tablero_visible: list[str] = archivo_tablero_visible.readlines()
    
    archivo_tablero.close()
    archivo_tablero_visible.close()

    cantidad_lineas_tablero = contar_lineas(lineas_tablero)
    cantidad_lineas_tablero_visible = contar_lineas(lineas_tablero_visible)

    # Vemos que se la cantidad de filas sea la correcta 
    if cantidad_lineas_tablero != estado['filas'] or cantidad_lineas_tablero_visible != estado['filas']:
        return False
    
    # Vemos que la cantidad de comas de cada linea es correcta, contando la cantidad de columnas
    for i in range(len(lineas_tablero)):
        cant_columnas_linea: int = contar_columnas(lineas_tablero[i])
        cant_columnas_linea_visible: int = contar_columnas(lineas_tablero_visible[i])
        if cant_columnas_linea != estado['columnas'] or cant_columnas_linea_visible != estado['columnas']:
            return False
    
    tablero_cargado: list[list[int]] = []
    tablero_visible_cargado: list[list[str]] = []
    contador_minas: int = 0
    
    # Acá reconstruimos el tablero y el tablero_visible
    # También chequeamos que los valores de tablero.txt sean un número entre -1 y 8
    # Además, corroboramos que no haya valores inválidos en tablero_visible.txt y que solo
    # puedan aparecer números entre 0 y 8, y los caracteres '*' y '?' 
    for i in range(len(lineas_tablero)):
        valores_tablero: list[str] = valores_linea(lineas_tablero[i])
        
        fila_tablero: list[int] = []
        for valor_str in valores_tablero:
            valor: int = int(valor_str)
            if valor == -1:
                contador_minas += 1
            elif valor < 0 or valor > 8:
                return False
            fila_tablero.append(valor)
        
        valores_visible: list[str] = valores_linea(lineas_tablero_visible[i])
        
        fila_visible: list[str] = []
        for valor_str in valores_visible:
            if valor_str == "*":
                fila_visible.append(BANDERA)
            elif valor_str == "?":
                fila_visible.append(VACIO)
            elif '0' <= valor_str <= '8':
                fila_visible.append(valor_str)
            else:
                return False
        
        # Por las dudas chequeamos que la cantidad de columnas sea igual a la cantidad 
        # de elementos que vamos a añadir a las listas. Si esto pasara, tal vez podría 
        # romperse algo del código que continúa.
        # Por ejemplo podría ser que una linea (inválida) de tablero_txt sea 38,1
        # y luego la cantidad de columnas sería 2 pero fila_tablero sería igual a 
        # [3,8,1] y len(fila_tablero) = 3 # 2.
        
        cant_columnas_linea: int = contar_columnas(lineas_tablero[i])
        if len(fila_tablero) != cant_columnas_linea or len(fila_visible) != cant_columnas_linea:
            return False
        
        tablero_cargado.append(fila_tablero)
        tablero_visible_cargado.append(fila_visible)
    
    # Nos fijamos que haya al menos una mina, y de lo contrario devolvemos False
    if contador_minas == 0:
        return False
    
    cant_columnas_tablero: int = contar_columnas(lineas_tablero[0])
    
    # Validamos que los números en tablero correspondan a minas adyacentes, es decir,
    # que se cumpla el asegura que dice que los valores de tablero.txt deben ser o bien 
    # -1, o la cantidad de minas que hay en las posiciones adyacentes
    # Observación: Antes fue chequeado que cada valor debe ser, o bien, un -1, o un número 
    # entre 0 y 8.
    for i in range(len(lineas_tablero)):
        for j in range(cant_columnas_tablero):
            if tablero_cargado[i][j] != -1:
                minas_adyacentes_esperadas = cant_minas_adyacentes(tablero_cargado, (i, j))
                if tablero_cargado[i][j] != minas_adyacentes_esperadas:
                    return False
    
    # Y finalmente validamos que los números de tablero_visible.txt 
    # correspondan a los valores en tablero.txt
    for i in range(len(lineas_tablero)):
        for j in range(cant_columnas_tablero):
            valor_visible = tablero_visible_cargado[i][j]
            if valor_visible != BANDERA and valor_visible != VACIO and int(valor_visible) >= 0 and int(valor_visible) <= 8:
                if int(valor_visible) != tablero_cargado[i][j]:
                    return False
    
    # Actualizamos estado y devolvemos True (si es que llegamos hasta acá)
    estado['filas'] = len(lineas_tablero)
    estado['columnas'] = cant_columnas_tablero
    estado['minas'] = contador_minas
    estado['juego_terminado'] = False
    estado['tablero'] = tablero_cargado
    estado['tablero_visible'] = tablero_visible_cargado
    
    return True

def contar_columnas(linea: str) -> int:
    """Contamos cuantas columnas hay en una linea, contando cuantas comas hay"""
    contador: int = 1
    for caracter in linea:
        if caracter == ',':
            contador += 1
    return contador

def valores_linea(linea: str) -> list[str]:
    """Devolvemos todos los valores de una linea en una lista, separando a los caracteres 
    donde hay una coma, o un salto de linea siendo cada valor de la lista, aquellos que no 
    son comas o saltos de linea (Salvo el caso particular que el valor entre dos lineas
    sea -1, ahí en vez de tomar el "-" y el "1", tomamos "-1"). """
    valores: list[str] = []
    hayUnMenos: bool = False
    for caracter in linea:
        if caracter != ',' and caracter != '\n':
            if caracter == '-': hayUnMenos = True
            elif hayUnMenos: 
                valores.append('-' + caracter)
                hayUnMenos = False
            else: valores.append(caracter)
    return valores

def contar_lineas(texto: list[str]) -> int:
    """Devolvemos cuántas lineas tiene un texto. El caso que queremos evitar
    es cuando una linea es solamente un \n, ese es el único caso en que podría suceder
    que exista una linea, pero cuya cantidad de caracteres no sea 0, pues 
    un salto de linea no es un caracter"""
    cant_lineas: int = 0
    for linea in texto:
        contador: int = 0
        for caracter in linea:
            if caracter != '\n':
                contador += 1
        
        if contador > 0: 
            cant_lineas += 1

    return cant_lineas