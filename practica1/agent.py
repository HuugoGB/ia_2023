"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
import copy

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, TipusCasella


class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass

class Estado:
    def __init__(self, tablero : [[]], jugadorActual :TipusCasella, accionesPrevias=None, padre=None):
        self.tablero = tablero  # La configuración actual del tablero del juego (matriz)
        self.jugadorActual = jugadorActual  # El jugador que tiene el turno actual, contiene el tipo de casilla que pone en el tablero (Cara o Cruz)
        self.padre = padre
        if accionesPrevias is None:
            self.accionesPrevias = []
        else:
            self.accionesPrevias = accionesPrevias


    def __lt__(self, other):
        return False

    def es_terminal(self):
        # Verifica si el estado es terminal (alguien ganó o es un empate)

        n = len(self.tablero)  # Obtiene el tamaño del tablero (N)

        # Comprueba las combinaciones horizontales
        for fila in self.tablero:
            for x in range(n - 3):
                combinacion = fila[x:x + 4]  # Crea una lista a partir de la lista fila, que toma las 4 casillas siguientes
                if all(casilla == self.jugadorActual for casilla in combinacion):  # Si todas las casillas pertenecen al mismo jugador, devuelve True
                    return True

        # Comprueba las combinaciones verticales
        for x in range(n):
            for y in range(n - 3):
                combinacion = [self.tablero[x][y + i] for i in range(4)]
                if all(casilla == self.jugadorActual for casilla in combinacion):  # Si todas las casillas pertenecen al mismo jugador, devuelve True
                    return True

        # Comprueba las combinaciones diagonales (de izquierda a derecha)
        for x in range(n - 3):
            for y in range(n - 3):
                combinacion = [self.tablero[x + i][y + i] for i in range(4)]
                if all(casilla == self.jugadorActual for casilla in combinacion):  # Si todas las casillas pertenecen al mismo jugador, devuelve True
                    return True

        # Comprueba las combinaciones diagonales (de derecha a izquierda)
        for x in range(3, n):
            for y in range(n - 3):
                combinacion = [self.tablero[x - i][y + i] for i in range(4)]
                if all(casilla == self.jugadorActual for casilla in combinacion):  # Si todas las casillas pertenecen al mismo jugador, devuelve True
                    return True

        return False  # Si no se cumple ninguna combinación de 4, el juego no está en un estado terminal

    def generar_estados_hijos(self) -> list:
        estados_hijos = []
        for x in range(len(self.tablero)):
            for y in range(len(self.tablero[0])):
                if self.tablero[x][y] == TipusCasella.LLIURE:
                    nuevo_estado = copy.deepcopy(self) #Hacemos una copia del estado padre
                    # Modificamos los valores del nuevo estado:
                    nuevo_estado.tablero[x][y] = self.jugadorActual#Asignamos a la casillas posicion (x,y) el tipo de casilla del jugador (Cara o Cruz)
                    nuevo_estado.accionesPrevias.append((x, y))
                    nuevo_estado.padre = (self, (x,y))
                    estados_hijos.append(nuevo_estado)
        return estados_hijos


    def calculoCosteTotalAestrella(self) -> int:

        # Variable para saber el valor de la huerística
        heuristicaActual = 4

        n = len(self.tablero)  # Obtiene el tamaño del tablero (N)

        # Comprueba las combinaciones horizontales
        for fila in self.tablero:
            for x in range(n - 3):
                combinacion = fila[x:x + 4]  # Crea una lista que toma las 4 casillas siguientes
                # Obtención de la heurística
                if 4 - self.__longitudCombinacion__(combinacion) < heuristicaActual:
                    heuristicaActual = 4 - self.__longitudCombinacion__(combinacion)


        # Comprueba las combinaciones verticales
        for x in range(n):
            for y in range(n - 3):
                combinacion = [self.tablero[x][y + i] for i in range(4)]
                #Obtención de la heurística
                if 4 - self.__longitudCombinacion__(combinacion) < heuristicaActual:
                    heuristicaActual = 4 - self.__longitudCombinacion__(combinacion)


        # Comprueba las combinaciones diagonales (de izquierda a derecha)
        for x in range(n - 3):
            for y in range(n - 3):
                combinacion = [self.tablero[x + i][y + i] for i in range(4)]
                # Obtención de la heurística
                if 4 - self.__longitudCombinacion__(combinacion) < heuristicaActual:
                        heuristicaActual = 4 - self.__longitudCombinacion__(combinacion)

        # Comprueba las combinaciones diagonales (de derecha a izquierda)
        for x in range(3, n):
            for y in range(n - 3):
                combinacion = [self.tablero[x - i][y + i] for i in range(4)]
                # Obtención de la heurística
                if 4 - self.__longitudCombinacion__(combinacion) < heuristicaActual:
                    heuristicaActual = 4 - self.__longitudCombinacion__(combinacion)
        return heuristicaActual

    def __longitudCombinacion__(self, combinacion: list) -> int:
        aux = 0
        for i in combinacion:
            if i == self.jugadorActual:
                aux += 1
        return aux

    def calculoCosteTotalMiniMax(self) -> int:

        # Variable para saber el valor de la huerística
        heuristicaActual = 0

        n = len(self.tablero)  # Obtiene el tamaño del tablero (N)

        # Comprueba las combinaciones horizontales
        for fila in self.tablero:
            for x in range(n - 3):  # Utiliza el tamaño N aquí
                combinacion = fila[x:x + 4]  # Crea una lista que toma las 4 casillas siguientes
                # Obtención de la heurística
                heuristicaActual += self.__heuristicaCombinacion__(combinacion, self.jugadorActual)
                if self.jugadorActual == TipusCasella.CARA: #Jugadas posibles jugador rival
                    heuristicaActual -= self.__heuristicaCombinacion__(combinacion, TipusCasella.CREU)
                else:
                    heuristicaActual -= self.__heuristicaCombinacion__(combinacion, TipusCasella.CARA)

        # Comprueba las combinaciones verticales
        for x in range(n):
            for y in range(n - 3):  # Utiliza el tamaño N aquí
                combinacion = [self.tablero[x][y + i] for i in range(4)]
                # Obtención de la heurística
                heuristicaActual += self.__heuristicaCombinacion__(combinacion, self.jugadorActual)
                if self.jugadorActual == TipusCasella.CARA:#Jugadas posibles jugador rival
                    heuristicaActual -= self.__heuristicaCombinacion__(combinacion, TipusCasella.CREU)
                else:
                    heuristicaActual -= self.__heuristicaCombinacion__(combinacion, TipusCasella.CARA)

        # Comprueba las combinaciones diagonales (de izquierda a derecha)
        for x in range(n - 3):  # Utiliza el tamaño N aquí
            for y in range(n - 3):  # Utiliza el tamaño N aquí
                combinacion = [self.tablero[x + i][y + i] for i in range(4)]
                # Obtención de la heurística
                heuristicaActual += self.__heuristicaCombinacion__(combinacion, self.jugadorActual)
                if self.jugadorActual == TipusCasella.CARA:#Jugadas posibles jugador rival
                    heuristicaActual -= self.__heuristicaCombinacion__(combinacion, TipusCasella.CREU)
                else:
                    heuristicaActual -= self.__heuristicaCombinacion__(combinacion, TipusCasella.CARA)

        # Comprueba las combinaciones diagonales (de derecha a izquierda)
        for x in range(3, n):  # Utiliza el tamaño N aquí
            for y in range(n - 3):  # Utiliza el tamaño N aquí
                combinacion = [self.tablero[x - i][y + i] for i in range(4)]
                # Obtención de la heurística
                heuristicaActual += self.__heuristicaCombinacion__(combinacion, self.jugadorActual)
                if self.jugadorActual == TipusCasella.CARA:#Jugadas posibles jugador rival
                    heuristicaActual -= self.__heuristicaCombinacion__(combinacion, TipusCasella.CREU)
                else:
                    heuristicaActual -= self.__heuristicaCombinacion__(combinacion, TipusCasella.CARA)


        return heuristicaActual

    def __heuristicaCombinacion__(self, combinacion: list, jugador: TipusCasella) -> int:
        heur = 0
        longitudCombinacion = 0
        # Si la combinacion es del jugador pasado por parámetro evaluamos la heurística
        if combinacion[0] == jugador:
            # Premiamos más según la lonjitud la linea formada por la misma ficha
            for i in combinacion:
                if i == self.jugadorActual:
                    longitudCombinacion += 1

            if longitudCombinacion == 4:
                heur = 10000


            elif longitudCombinacion == 3:
                heur = 100


            elif longitudCombinacion == 2:
                heur = 3


            elif longitudCombinacion == 1:
                heur = 1
        return heur

    def evaluar(self):
        # Evalúa la calidad de este estado (valor heurístico)
        return self.calculoCosteTotalMiniMax()


