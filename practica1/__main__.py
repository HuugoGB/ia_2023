from practica1 import agent,agentAestrella,agentProfunditat,agentMinMax, joc


def main():
    #quatre = joc.Taulell([agentProfunditat.AgentProfunditat("Hugo")])
    #quatre = joc.Taulell([agentAestrella.AgentAestrella("Hugo")])
    quatre = joc.Taulell([agentMinMax.AgentMinMax("Hugo"),agentMinMax.AgentMinMax("Pere")])
    quatre.comencar()


if __name__ == "__main__":
    main()
