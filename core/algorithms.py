import itertools
from typing import List
from minizinc_executor import salesman


class Player:
    name : str
    utility : dict 
    normalized_utility: dict 
    cost_bound : int
    
    def __init__(self, name, utility, cost_bound):
        self.name = name
        self.utility = utility
        self.cost_bound = cost_bound

    def normalize_utility(self,bound:int, L:List[str]):
        for k in L:
            self.normalized_utility[k] = bound * (self.utility[k]/max(self.utility))

    def get_utility(self, location: str):
        return self.normalized_utility[location]


class Tour:
    tour_itin: List[str]
    itin_length: int

    def __init__(self, tour_itin, itin_length):
        self.tour_itin = tour_itin
        self.itin_length = itin_length

    def __str__(self):
        retvalue = ''
        for i in range(0, len(self.tour_itin)):
            retvalue += self.tour_itin[i]
            if i < len(self.tour_itin) - 1:
                retvalue += ', '
        retvalue+='\n'
        retvalue+='Length: '+str(self.itin_length)
        return retvalue

class Outcome:
    X : List['Player']
    V : List[str]
    w : int
    f : dict
    p : dict
    t : Tour

    def __init__(self, X, V, w, f, p, t):
        self.X = X
        self.V = V
        self.w = w
        self.f = f
        self.p = p
        self.t = t


class Distance:
    sorgente: str
    destinazione: str
    distanza: int

    def __init__(self, sorgente, destinazione, distanza):
        self.sorgente = sorgente
        self.destinazione = destinazione
        self.distanza = distanza

    @staticmethod
    def find_distance(distances: List['Distance'], l1: str, l2: str) -> int:
        for distance in distances:
            if (distance.destinazione == l1 and distance.sorgente == l2) or \
                (distance.destinazione == l2 and distance.sorgente == l1):
                return distance.distanza
        return 0


def normalize_preferences(N: List['Player'], L: List[str]):
    m = 0
    for player in N:
        tmp = 0
        for location in L:
            if player.get_utility(location) > 0:
                tmp=tmp+1
        if tmp > m:
            m = tmp
    for player in N:
       player.normalize_utility(bound=m, L=L)



def minimum_spanning_tree(self, a, g, r):
    pass

def constraint_check(self, X: List['Player'], L_x: List[str], t: 'Tour', MaxLen: int, f: dict, p: dict) -> bool:
    q = t.itin_length
    if MaxLen > q:
        return False
    for player in X:
        tmp = 0
        # COSTI FISSI -- RIVEDERE 
        #for j in range (0, len(L_x)):
        #    d_j = 0
        #    for k in range (0, len(X)):
        #        d_j += u_bar[k][j]
        #    tmp = (50 * u_bar[j])/d_j
        #    f[i] += tmp
        p[player] = (10*q)/len(X)
        if f[player] + p[player] > player.cost_bound:
            return False
    
    return True


def extract_distance_subset(distances: List['Distance'], subset: List[str]) -> List['Distance']:
    returnvalue: List['Distance'] = []
    for i in distances:
        if belongs_to_subset(i, subset):
            returnvalue.append(i)
    return returnvalue



def belongs_to_subset(distance: 'Distance', subset: List[str]) -> bool:
    start = distance.sorgente
    end = distance.destinazione
    start_in_subset = False
    end_in_subset = False
    for i in subset:
        if i == start:
            start_in_subset = True
        if i == end:
            end_in_subset = True
        if start_in_subset and end_in_subset:
            return True
    
    return False


def best_travel(X: List['Player'], L_x: List[str], MaxLen: int, D: List['Distance'], Start: str, R: List['Outcome']) -> 'Outcome':
    found = False
    while (len(R) == 0):
        f: dict = ()
        p: dict = ()
        #G = [[0 for i in range(0, len(L_x))] for j in range(0, len(L_x))]
        #End = ""
        D_X = extract_distance_subset(D, L_x)
        t: 'Tour' = salesman(L_x, D_X, Start)
        found = constraint_check(X, L_x, t, MaxLen, f, p)
        if found:
            w = 0
            for player in X:
                w = w + sum(player.normalized_utility)
            o = Outcome(X,L_x,w,f,p,t)
            R.append(o)
        else:
            if len(L_x) == 1:
                return None
            subsets = list(itertools.combinations(L_x, len(L_x)-1))
            for subset in subsets:
                tmp = best_travel(X,subset,MaxLen,D,Start,R)
                if tmp != None:
                    R.append(tmp)
    
    o_max: 'Outcome'
    w_max:int = 0
    for o in R:
        if o.w > w_max:
            w_max = o.w
            o_max = o

    return o_max

def lcl_travel(self, N: List['Player'], L: List[str], Start: str, D: List[Distance], k: int, MaxLen: int):
    normalize_preferences(N,L)
    N_part: List[List['Player']] = list(itertools.combinations(N,k))
    O = []
    for player_subset in N_part:
        L_x = []
        for player in player_subset:
            for location in L:
                if player.get_utility(location) > 0:
                    L_x.append(location)
        o = best_travel(player_subset, L_x, MaxLen, D, Start, [])
        O.append(o)
    
    o_max: 'Outcome'
    w_max:int = 0
    for o in O:
        if o.w > w_max:
            w_max = o.w
            o_max = o

    LV = o_max.V
    UT = o_max.X
    CTF = o_max.f
    CTP = o_max.p
    T = o_max.t

    


