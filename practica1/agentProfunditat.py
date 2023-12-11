from ia_2022 import entorn
from practica1 import joc
from practica1.agent import Estado
from practica1.entorn import Accio, SENSOR
import time

class AgentProfunditat(joc.Agent):
    def __init__(self, nom):
        super(AgentProfunditat, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        if self.__accions is None:
            self.cercaProfunditat(Estado(percepcio[SENSOR.TAULELL], self.jugador, [], None))
        if len(self.__accions) != 0:
            print(self.__accions)
            return Accio.POSAR, self.__accions.pop()
        return Accio.ESPERAR

    def cercaProfunditat(self, estatInicial) -> list:
        self.__oberts = []
        self.__tancats = set()
        self.__oberts.append(estatInicial)
        while len(self.__oberts) != 0:
            estatActual = self.__oberts.pop(0)
            if Estado.es_terminal(estatActual):
                self.__accions = estatActual.accionesPrevias
                break
            else:
                if estatActual not in self.__tancats :
                    self.__tancats.add(estatActual)
                    estadosHijos = Estado.generar_estados_hijos(estatActual)
                    self.__oberts = estadosHijos + self.__oberts
