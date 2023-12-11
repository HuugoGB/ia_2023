from ia_2022 import entorn
from practica1 import joc
from practica1.agent import Estado
from practica1.entorn import Accio, SENSOR
import time

class AgentMinMax(joc.Agent):
    def __init__(self, nom):
        super(AgentMinMax, self).__init__(nom)
    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        #Cada llamada a actua, debe hacer una nueva busqueda minmax, para el nuevo estado del tablero y solamente hacer la primera accion
        _, _, accion = self.cercaMinMax(Estado(percepcio[SENSOR.TAULELL], self.jugador, [], None), True, float('-inf'),float('inf'),2)
        if accion is not None:
            return Accio.POSAR, accion
        return Accio.ESPERAR

    def cercaMinMax(self, estado, turnoMax: bool, alpha, beta, profundidad) -> (Estado,int,(int,int)):
        score = estado.evaluar()
        if profundidad == 0:
            estado, accion = estado.padre
            return estado, score, accion

        puntuacionHijos = []
        for estadoHijo in estado.generar_estados_hijos():
            puntuacionHijos.append(self.cercaMinMax(estadoHijo, not turnoMax, alpha, beta, profundidad -1))
            if turnoMax:
                alpha = self.maximAlpha(puntuacionHijos, alpha)
            else:
                beta = self.minimBeta(puntuacionHijos, beta)
            if alpha >= beta:
                break
        if turnoMax:
            return self.maxim(puntuacionHijos)
        else:
            return self.minim(puntuacionHijos)

    def minimBeta(self, puntuacionHijos: [], beta):
        for (_, score,_) in puntuacionHijos:
            if score < beta:
                beta = score
        return beta

    def maximAlpha(self,puntuacionHijos: [], alpha):
        for (_, score,_) in puntuacionHijos:
            if score > alpha:
                alpha = score
        return alpha

    def minim(self, puntuacionHijos: []):
        valorMinimo = float('inf')
        estadoMinimo = accionMinima = None
        for (estado, score,accion) in puntuacionHijos:
            if score < valorMinimo:
                estadoMinimo,valorMinimo,accionMinima = estado,score,accion
        if estadoMinimo is None or accionMinima is None:
            return estado,score,accion
        return estadoMinimo, valorMinimo,accionMinima

    def maxim(self,puntuacionHijos: []):
        valorMaximo = -float('inf')
        estadoMaximo = accionMaximo = None
        for (estado, score,accion) in puntuacionHijos:
            if score > valorMaximo:
                estadoMaximo,valorMaximo,accionMaximo = estado,score,accion
        if estadoMaximo is None or accionMaximo is None:
            return estado,score,accion
        return estadoMaximo, valorMaximo ,accionMaximo