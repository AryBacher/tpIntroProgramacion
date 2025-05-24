#ej1

def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    matriz: list = []
    cantidad_minas: int = 0
    for i in range(filas):
        fila = []
        for j in range(columnas):
            if cantidad_minas < minas: 
                fila.append(-1)
                cantidad_minas += 1
            else: 
                fila.append(0)     
        matriz.append(fila)
    
    return matriz 


#ej2

def calcular_numeros(tablero: list[list[int]]) -> None:
    tablero_nuevo: list[list[int]] = tablero
    for fila in tablero:
        for elemento in range(len(fila)):
            if fila[elemento] == 0:
                fila[elemento] = cantidad_elementos(tablero,(-1))
    
    return tablero_nuevo
            
    

def cantidad_elementos(matriz: list[list[int]], n: int) -> int:
    cantidad: int = 0
    for fila in matriz:
        for elemento in range(len(fila)):
            if fila[elemento] == n:
                cantidad += 1
    return cantidad 