import constraint
from typing import List

class Nodo:
    label: str = ''

    def __init__(self, label):
        self.label = label

class Arco:
    sorgente: Nodo
    destinazione: Nodo
    peso: int

    def __init__(self, sorgente, destinazione, peso):
        self.sorgente = sorgente
        self.destinazione = destinazione
        self.peso = peso


def find_arco(archi: List[Arco], sorgente: Nodo, destinazione: Nodo) -> int:
    for arco in archi:
        if arco.destinazione == destinazione and arco.sorgente == sorgente:
            return arco.peso
    return None
    
    
class Graph:
    adjacenceMatrix:int = [[]]
    nodi: List[Nodo] = []
    archi: List[Arco] = []

    def __init__(self, nodi: List[Nodo], archi: List[Arco]):
        self.nodi = nodi
        self.archi = archi
        self.adjacenceMatrix = [len(nodi)][len(nodi)]
        for i in range(0, len(nodi)):
            for j in range(0, len(nodi)):
                self.adjacenceMatrix[i][j] = find_arco(archi, nodi[i], nodi[j])


def piccioneviaggiatore(G: Graph, Start: Nodo):
    problem = constraint.Problem()
    problem.addVariable('nodes', Graph.nodi)
    problem.addVariable('arcs', Graph.archi)




problem.addVariable('x', [1,2,3])
problem.addVariable('y', range(10))


def our_constraint(x, y):
    if x + y >= 5:
        return True

problem.addConstraint(our_constraint, ['x','y'])

solutions = problem.getSolutions()

# Easier way to print and see all solutions
# for solution in solutions:
#    print(solution)

# Prettier way to print and see all solutions
length = len(solutions)
print("(x,y) ∈ {", end="")
for index, solution in enumerate(solutions):
    if index == length - 1:
        print("({},{})".format(solution['x'], solution['y']), end="")
    else:
        print("({},{}),".format(solution['x'], solution['y']), end="")
print("}")