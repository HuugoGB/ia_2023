from ia_2022 import entorn
from practica1 import joc
from practica1.agent import Estado
from practica1.entorn import Accio, SENSOR
import time,queue


class AgentAestrella(joc.Agent):
    def __init__(self, nom):
        super(AgentAestrella, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        if self.__accions is None:
            self.cercaAestrella(Estado(percepcio[SENSOR.TAULELL], self.jugador, [], None))
        if len(self.__accions) != 0:
            print(self.__accions)
            return Accio.POSAR, self.__accions.pop()
        return Accio.ESPERAR

    def cercaAestrella(self,estatInicial):
        self.__oberts = queue.PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((estatInicial.calculoCosteTotalAestrella(), estatInicial))

        actual = None
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()
            if actual in self.__tancats:
                continue

            if actual.es_terminal():
                #self.__accions = actual.accionesPrevias
                break

            estats_fills = actual.generar_estados_hijos()

            for estat_f in estats_fills:
                self.__oberts.put((estat_f.calculoCosteTotalAestrella(), estat_f))

            self.__tancats.add(actual)

        if actual.es_terminal():
            accions = []
            iterador = actual
            while iterador.padre is not None:
                padre, accio = iterador.padre #(self,(x,y)) padre = self, accio = (x,y)

                accions.append(accio)
                iterador = padre
            self.__accions = accions
