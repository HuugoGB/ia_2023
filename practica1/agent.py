"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, SENSOR,TipusCasella

class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        pass

    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        if self.__accions is None:
            estatInicial = Estat(percepcio[SENSOR.TAULELL], self.jugador,accions_previes=None)
            self.__accions = self.cercaProfunditat(estatInicial)
        else:
            return Accio.POSAR, self.__accions.pop()

    def cercaProfunditat(self, estatInicial):
        self.__oberts = []
        self.__accions = []
        self.__tancats = set()
        self.__oberts.append(estatInicial)
        while len(self.__oberts) != 0:
            x = self.__oberts.pop()
            if Estat.es_terminal(x):
                return x.accions_previes
            else:
                if (x in self.__tancats) is False:
                    self.__tancats.add(x)
                    self.__oberts = Estat.generar_estats_fill(x) + self.__oberts
    def cercaAestrella(self):
        pass

    def cercaMinMax(self):
        pass

class Estat:
    def __init__(self, tablero, jugador_actual, accions_previes):
        self.tablero = tablero  # La configuración actual del tablero del juego (matriz)
        self.jugador_actual = jugador_actual  # El jugador que tiene el turno actual
        self.accions_previes = accions_previes
    def es_terminal(self):
        # Verifica si el estado es terminal (alguien ganó o es un empate)

        n = len(self.tablero)  # Obté la mida del taulell (N)

        # Comprova les combinacions horitzontals
        for fila in self.tablero:
            for x in range(n - 3):  # Utilitza la mida N aquí
                combinacio = fila[x:x + 4]
                if all(casella == self.jugador_actual for casella in combinacio):
                    return True

        # Comprova les combinacions verticals
        for x in range(n):
            for y in range(n - 3):  # Utilitza la mida N aquí
                combinacio = [self.tablero[x][y + i] for i in range(4)]
                if all(casella == self.jugador_actual for casella in combinacio):
                    return True

        # Comprova les combinacions diagonals (des d'esquerra a dreta)
        for x in range(n - 3):  # Utilitza la mida N aquí
            for y in range(n - 3):  # Utilitza la mida N aquí
                combinacio = [self.tablero[x + i][y + i] for i in range(4)]
                if all(casella == self.jugador_actual for casella in combinacio): #Si totes les caselles pertenexien al matexi jugador retorna True
                    return True

        # Comprova les combinacions diagonals (des de dreta a esquerra)
        for x in range(3, n):  # Utilitza la mida N aquí
            for y in range(n - 3):  # Utilitza la mida N aquí
                combinacio = [self.tablero[x - i][y + i] for i in range(4)]
                if all(casella == self.jugador_actual for casella in combinacio): #Si totes les caselles pertenexien al matexi jugador retorna True
                    return True

        return False  # Si no es compleix cap combinació de 4, el joc no està en un estat terminal





    def generar_estats_fill(self) -> list:
        estats_fill = []
        for x in range(len(self.tablero)):
            for y in range(len(self.tablero[0])):
                if self.tablero[x][y] == TipusCasella.LLIURE:
                    # La casella està buida, per tant, podem fer un moviment aquí
                    nou_tablero = [fila[:] for fila in self.tablero]  # Crea una còpia del taulell
                    nou_tablero[x][y] = self.jugador_actual  # Realitza el moviment, indicant en la casella el jugador qui ha colocat.
                    accions = self.accions_previes + [x,y]

                    nou_estat = Estat(nou_tablero, self.jugador_actual,accions)
                    estats_fill.append(nou_estat)

        return estats_fill

    def evaluar(self):
        # Evalúa la calidad de este estado (valor heurístico)
        pass
