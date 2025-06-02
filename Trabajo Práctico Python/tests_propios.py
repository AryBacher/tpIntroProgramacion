import unittest
from buscaminas import (existe_archivo, crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                               reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria, guardar_estado, cargar_estado, contar_columnas, BOMBA, BANDERA, VACIO, EstadoJuego)
from typing import TextIO

'''
Ayudamemoria: entre los métodos para testear están los siguientes:

    self.assertEqual(a, b) -> testea que a y b tengan el mismo valor
    self.assertTrue(x)     -> testea que x sea True
    self.assertFalse(x)    -> testea que x sea False
    self.assertIn(a, b)    -> testea que a esté en b (siendo b una lista o tupla)
'''
def cant_minas_en_tablero(tablero: list[list[int]]) -> bool:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas:int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas

def son_solo_ceros_y_bombas (tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True

def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True

def hay_espacios(linea: str) -> bool:
    """Chequea si hay espacios o no en una linea de texto"""
    for letra in linea:
        if letra == ' ': return True
    return False

def estado_fijo() -> EstadoJuego:
    estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [BANDERA, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
    
    return estado

class colocar_minasTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
    
    def test_mas_minas(self):
        filas = 2
        columnas = 2
        minas = 2

        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
    
    def test_mas_dimension_mas_minas(self):
        filas = 3
        columnas = 3
        minas = 3

        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
    
    def test_casi_completo_minas(self):
        filas = 3
        columnas = 3
        minas = 8

        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
    


class calcular_numerosTest(unittest.TestCase):
    def test_ejemplo(self):
        tablero = [[0,-1],
                   [0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1],
                                   [1, 1]])
    
    def test_valores_repetidos(self):
        tablero = [[-1,-1],
                   [0, 0]]
        
        calcular_numeros(tablero)
        self.assertEqual(tablero, [[-1,-1],
                                   [2, 2]])
    
    def test_valores_centro(self):
        tablero = [[0, 0, 0],
                   [0,-1, 0],
                   [0, 0, 0]]
        
        calcular_numeros(tablero)
        self.assertEqual(tablero, [[1, 1, 1],
                                   [1,-1, 1],
                                   [1, 1, 1]])
    
    def test_valores_centro_invertido(self):
        tablero = [[-1,-1,-1],
                   [-1, 0,-1],
                   [-1,-1,-1]]
        
        calcular_numeros(tablero)
        self.assertEqual(tablero, [[-1,-1,-1],
                                   [-1, 8,-1],
                                   [-1,-1,-1]])



class crear_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)
    

class marcar_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)

    def test_bandera_a_vacio(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [1, 1],
                [1, -1]
            ],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO, BANDERA]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, BANDERA]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [1, 1],
            [1, -1]
        ])
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)

    def test_ni_bandera_ni_vacio(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [1, -1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, 1]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 1, 1)
        # Testeamos que no se cambio nada pues no se hizo click ni en una casilla vacía
        # ni en una bandera
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, 1]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [1, -1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)


    def test_bandera_a_vacio(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [BANDERA, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 1, 0)
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
    

    def test_celda_en_juego_terminado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [1, -1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': True 
        }
        marcar_celda(estado, 1, 1)
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [1, -1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)



class descubrir_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 2, 2)
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO],
            [VACIO, "3", "1"],
            [VACIO, "2", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])

    def test_casilla_no_cero(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 0)
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [
            ["2", VACIO, VACIO],
            [VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])

    def test_juego_estaba_terminado(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                ["2", BANDERA, "1"],
                [BANDERA, "3", "1"],
                [BANDERA, "2", "0"]
            ],
            'juego_terminado': True
        }
        descubrir_celda(estado, 0, 0)
        # Testeamos que nada haya cambiado en el tablero visible
        self.assertEqual(estado['tablero_visible'], [
            ["2", BANDERA, "1"],
            [BANDERA, "3", "1"],
            [BANDERA, "2", "0"]
        ])
        # Testeamos que el resto no se modificó salvo el juego_terminado
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertTrue(estado['juego_terminado'])

    def test_casilla_era_mina(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 1)
        # Testeamos que la celda descubierta sea visible y que se muestran todas las bombas
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, BOMBA, VACIO],
            [BOMBA, VACIO, VACIO],
            [BOMBA, VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó salvo el juego_terminado
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertTrue(estado['juego_terminado'])

    def test_acaba_de_ganar(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                ["2", BANDERA, VACIO],
                [BANDERA, "3", "1"],
                [BANDERA, "2", "0"]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 2)
        # Testeamos que cambia la casilla clickeada
        self.assertEqual(estado['tablero_visible'], [
            ["2", BANDERA, "1"],
            [BANDERA, "3", "1"],
            [BANDERA, "2", "0"]
        ])
        # Testeamos que el resto no se modificó salvo el juego_terminado
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertTrue(estado['juego_terminado'])

    def test_caminos_complejos(self):
        estado: EstadoJuego = {
            'filas': 7,
            'columnas': 7,
            'minas': 10,
            'tablero': [
                [-1, 2, 1, 1, 1, -1, 1],
                [2, 3, -1, 1, 2, 2, 2],
                [-1, 2, 1, 1, 1, -1, 1],
                [2, -1, 1, 0, 1, 2, 2],
                [2, 2, 2, 0, 0, 1, -1],
                [2, -1, 1, 0, 1, 2, 2],
                [-1, 2, 1, 0, 1, -1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO], 
                [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO], 
                [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO], 
                [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO], 
                [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO], 
                [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO], 
                [VACIO, VACIO, VACIO, BANDERA, VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 3, 3)
        # Testeamos que todas las celdas descubierta sean visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO], 
            [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO], 
            [VACIO, VACIO, "1", "1", "1", VACIO, VACIO], 
            [VACIO, VACIO, "1", "0", "1", "2", VACIO], 
            [VACIO, VACIO, "2", "0", "0", "1", VACIO], 
            [VACIO, VACIO, "1", "0", "1", "2", VACIO], 
            [VACIO, VACIO, "1", BANDERA, "1", VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 7)
        self.assertEqual(estado['columnas'], 7)
        self.assertEqual(estado['minas'], 10)
        self.assertEqual(estado['tablero'], [
            [-1, 2, 1, 1, 1, -1, 1],
            [2, 3, -1, 1, 2, 2, 2],
            [-1, 2, 1, 1, 1, -1, 1],
            [2, -1, 1, 0, 1, 2, 2],
            [2, 2, 2, 0, 0, 1, -1],
            [2, -1, 1, 0, 1, 2, 2],
            [-1, 2, 1, 0, 1, -1, 1]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 10)
        self.assertFalse(estado['juego_terminado'])


class verificar_victoriaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        # Testeamos que el juego esté terminado y que haya ganado
        self.assertTrue(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            ["1", "1"]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_no_victoria(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertFalse(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            ["1", "1"]
        ])
        self.assertFalse(estado['juego_terminado'])
        


class obtener_estado_tableroTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_otro_tablero(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, "1"]
            ],
            'juego_terminado': False
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [VACIO, "1"],
            [VACIO, "1"]
        ])
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            [VACIO, "1"]
        ])
        self.assertFalse(estado['juego_terminado'])


class reiniciar_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        reiniciar_juego(estado)
        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

    def test_juego_terminado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", "1"]
            ],
            'juego_terminado': True
        }
        reiniciar_juego(estado)
        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

class guardar_estadoTest(unittest.TestCase):
    def test_guardado_correcto(self):
        estado: EstadoJuego = estado_fijo()

        guardar_estado(estado, "")
        
        # Chequeamos que existan los archivos
        self.assertTrue(existe_archivo("", "tablero.txt"))
        self.assertTrue(existe_archivo("", "tablero_visible.txt"))
        
        # Los abrimos y analizamos si el contenido es igual al esperado
        archivo_tablero: TextIO = open("tablero.txt", "r", encoding="utf-8")
        archivo_tablero_visible: TextIO = open("tablero_visible.txt", "r", encoding="utf-8")
        
        self.assertEqual(archivo_tablero.readline(), "-1,1\n")
        self.assertEqual(archivo_tablero.readline(), "1,1")

        self.assertEqual(archivo_tablero_visible.readline(), "*,1\n")
        self.assertEqual(archivo_tablero_visible.readline(), "?,?")

        archivo_tablero.close()
        archivo_tablero_visible.close()
        
        # Testeamos que nada haya cambiado
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, "1"],
            [VACIO, VACIO]
        ])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

    def test_cantidad_filas(self):
        estado: EstadoJuego = estado_fijo()

        guardar_estado(estado, "")
        
        # Chequeamos que existan los archivos
        self.assertTrue(existe_archivo("", "tablero.txt"))
        self.assertTrue(existe_archivo("", "tablero_visible.txt"))
        
        # Los abrimos y analizamos si la cantidad de filas es correcta
        archivo_tablero: TextIO = open("tablero.txt", "r", encoding="utf-8")
        archivo_tablero_visible: TextIO = open("tablero_visible.txt", "r", encoding="utf-8")
        
        self.assertEqual(len(archivo_tablero.readlines()), 2)
        self.assertEqual(len(archivo_tablero_visible.readlines()), 2)

        archivo_tablero.close()
        archivo_tablero_visible.close()
        
        # Testeamos que nada haya cambiado
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, "1"],
            [VACIO, VACIO]
        ])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

    def test_cantidad_comas(self):
        estado: EstadoJuego = estado_fijo()

        guardar_estado(estado, "")
        
        # Chequeamos que existan los archivos
        self.assertTrue(existe_archivo("", "tablero.txt"))
        self.assertTrue(existe_archivo("", "tablero_visible.txt"))
        
        # Los abrimos y analizamos si la cantidad de comas es correcta
        archivo_tablero: TextIO = open("tablero.txt", "r", encoding="utf-8")
        archivo_tablero_visible: TextIO = open("tablero_visible.txt", "r", encoding="utf-8")
        
        self.assertEqual(contar_columnas(archivo_tablero.readline()) - 1, 1)
        self.assertEqual(contar_columnas(archivo_tablero.readline()) - 1, 1)
        
        self.assertEqual(contar_columnas(archivo_tablero_visible.readline()) - 1, 1)
        self.assertEqual(contar_columnas(archivo_tablero_visible.readline()) - 1, 1)

        archivo_tablero.close()
        archivo_tablero_visible.close()
        
        # Testeamos que nada haya cambiado
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, "1"],
            [VACIO, VACIO]
        ])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

    def test_hay_espacios(self):
        estado: EstadoJuego = estado_fijo()

        guardar_estado(estado, "")
        
        # Chequeamos que existan los archivos
        self.assertTrue(existe_archivo("", "tablero.txt"))
        self.assertTrue(existe_archivo("", "tablero_visible.txt"))
        
        # Los abrimos y analizamos si la cantidad de comas es correcta
        archivo_tablero: TextIO = open("tablero.txt", "r", encoding="utf-8")
        archivo_tablero_visible: TextIO = open("tablero_visible.txt", "r", encoding="utf-8")
        
        self.assertFalse(hay_espacios(archivo_tablero.readline()))
        self.assertFalse(hay_espacios(archivo_tablero.readline()))
        
        self.assertFalse(hay_espacios(archivo_tablero_visible.readline()))
        self.assertFalse(hay_espacios(archivo_tablero_visible.readline()))

        archivo_tablero.close()
        archivo_tablero_visible.close()
        
        # Testeamos que nada haya cambiado
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, "1"],
            [VACIO, VACIO]
        ])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

class cargar_estadoTest(unittest.TestCase):
    def test_guardado_y_cargado(self):
        estado: EstadoJuego = estado_fijo()

        guardar_estado(estado, "")
        cargar_estado(estado, "")
        
        # Testeamos que nada haya cambiado
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, "1"],
            [VACIO, VACIO]
        ])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

    def test_guardado_reiniciado_y_cargado(self):
        estado: EstadoJuego = estado_fijo()

        guardar_estado(estado, "")
        reiniciar_juego(estado)
        cargar_estado(estado, "")
        
        # Testeamos que nada haya cambiado
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, "1"],
            [VACIO, VACIO]
        ])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

    def test_cargado_a_medio_del_juego(self):
        estado: EstadoJuego = estado_fijo()

        guardar_estado(estado, "")
        
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [1, -1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [BANDERA, VACIO]
            ],
            'juego_terminado': False
        }

        cargar_estado(estado, "")
        
        # Testeamos que nada haya cambiado
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, "1"],
            [VACIO, VACIO]
        ])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

    def test_no_existen_archivos(self):
        estado: EstadoJuego = estado_fijo()

        guardar_estado(estado, "")
        self.assertFalse(cargar_estado(estado, "/archivos_guardados"))
        
        # Testeamos que nada haya cambiado
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, "1"],
            [VACIO, VACIO]
        ])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

    def test_levanta_bien_banderas_y_vacios(self):
        estado: EstadoJuego = estado_fijo()
        
        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("1,-1\n")
        archivo_prueba.write("1,1")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        cargar_estado(estado, "")
        
        # Testeamos que haya levantado bien todos los datos
        self.assertEqual(estado['tablero_visible'], [
            ["1", BANDERA],
            [VACIO, VACIO]
        ])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero'], [
            [1, -1],
            [1, 1]
        ])

    def test_archivo_con_linea_vacia(self):
        estado: EstadoJuego = estado_fijo()
        
        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("\n")
        archivo_prueba.write("1,1")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertFalse(cargar_estado(estado, ""))
        
        # Observación: Aquí no tiene que cambiar estado, pues no se cumple 
        # una de las condiciones

    def test_archivo_vacio(self):
        estado: EstadoJuego = estado_fijo()

        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("\n")
        archivo_prueba.write("\n")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertFalse(cargar_estado(estado, ""))
        
        # Observación: Aquí no tiene que cambiar estado, pues no se cumple 
        # una de las condiciones

    def test_cantidad_de_lineas_incorrecta(self):
        estado: EstadoJuego = estado_fijo()

        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("1,-1\n")
        archivo_prueba.write("1,1\n")
        archivo_prueba.write("0,0")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertFalse(cargar_estado(estado, ""))
        
        # Observación: Aquí no tiene que cambiar estado, pues no se cumple 
        # una de las condiciones

    def test_cantidad_de_comas_incorrecta(self):
        estado: EstadoJuego = estado_fijo()

        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("1,-1\n")
        archivo_prueba.write("1,,1")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertFalse(cargar_estado(estado, ""))
        
        # Observación: Aquí no tiene que cambiar estado, pues no se cumple 
        # una de las condiciones

    def test_sin_minas_en_tablero(self):
        estado: EstadoJuego = estado_fijo()

        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("1,1\n")
        archivo_prueba.write("1,1")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertFalse(cargar_estado(estado, ""))
        
        # Observación: Aquí no tiene que cambiar estado, pues no se cumple 
        # una de las condiciones

    def test_valor_mayor_a_8(self):
        estado: EstadoJuego = estado_fijo()

        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("9,-1\n")
        archivo_prueba.write("1,1")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertFalse(cargar_estado(estado, ""))
        
        # Observación: Aquí no tiene que cambiar estado, pues no se cumple 
        # una de las condiciones

    def test_valores_invalidos_visibles(self):
        estado: EstadoJuego = estado_fijo()

        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("1,-1\n")
        archivo_prueba.write("1,1")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("a,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertFalse(cargar_estado(estado, ""))
        
        # Observación: Aquí no tiene que cambiar estado, pues no se cumple 
        # una de las condiciones

    def test_valores_de_dos_cifras_en_tablero(self):
        estado: EstadoJuego = estado_fijo()

        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("38,-1\n")
        archivo_prueba.write("1,1")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertFalse(cargar_estado(estado, ""))
        
        # Observación: Aquí no tiene que cambiar estado, pues no se cumple 
        # una de las condiciones

    def test_minas_adyacentes_incorrectas(self):
        estado: EstadoJuego = estado_fijo()

        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("1,-1\n")
        archivo_prueba.write("1,2")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertFalse(cargar_estado(estado, ""))
        
        # Observación: Aquí no tiene que cambiar estado, pues no se cumple 
        # una de las condiciones

    def test_valores_incorrectos_visibles(self):
        estado: EstadoJuego = estado_fijo()

        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("1,-1\n")
        archivo_prueba.write("1,1")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("2,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertFalse(cargar_estado(estado, ""))
        
        # Observación: Aquí no tiene que cambiar estado, pues no se cumple 
        # una de las condiciones

    def test_valores_correctos(self):
        estado: EstadoJuego = estado_fijo()

        archivo_prueba: TextIO = open("tablero.txt", "w", encoding="utf-8")
        archivo_prueba.write("1,-1\n")
        archivo_prueba.write("1,1")
        
        archivo_prueba_visible: TextIO = open("tablero_visible.txt", "w", encoding="utf-8")
        archivo_prueba_visible.write("1,*\n")
        archivo_prueba_visible.write("?,?")

        archivo_prueba.close()
        archivo_prueba_visible.close()

        self.assertTrue(cargar_estado(estado, ""))
        
        # Testeamos que nada haya cambiado
        self.assertEqual(estado['tablero_visible'], [
            ["1", BANDERA],
            [VACIO, VACIO]
        ])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero'], [
            [1, -1],
            [1,  1]
        ])

# Tarea: Agregar tests para guardar_estado y cargar_estado
"""
- Agregar varios casos de prueba para cada función.
- Se debe cubrir al menos el 95% de las líneas de cada función.
- Se debe cubrir al menos el 95% de ramas de cada función.
"""

if __name__ == '__main__':
    unittest.main(verbosity=2)
