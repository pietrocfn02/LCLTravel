import itertools
from typing import List

from minizinc import Instance, Model, Result, Solver

from src.file_handler import setup_config_file


class Player:
    name: str
    utility: dict
    normalized_utility: dict
    cost_bound: int

    def __init__(self, name, utility, cost_bound):
        self.name = name
        self.utility = utility
        self.cost_bound = cost_bound
        self.normalized_utility = {}

    def normalize_utility(self, bound: int, L: List[str]):
        for k in L:
            max_utility = max(self.utility.values())
            self.normalized_utility[k] = bound * (self.utility.get(k) / max_utility)

    def sum_normalized_utility(self, L_x: List[str]):
        sum: int = 0
        for i in L_x:
            sum += self.normalized_utility.get(i)

        return sum

    def __str__(self):
        retvalue = self.name + ", ["
        for i in self.normalized_utility.values():
            retvalue += str(i) + ", "
        retvalue += "]\nUtilities:\n"
        for i, j in self.utility.items():
          retvalue += f'{i} - {j}\n'

        return retvalue

    def get_utility(self, location: str):
        return self.utility[location]

    def get_norm_utility(self, location: str):
        return self.normalized_utility.get(location)

    def get_utilities(self):
        return self.normalized_utility

    def get_max_utility(self):
        max = 0
        for i in self.normalized_utility.values():
            if i > max:
                max = i

        return max

    def get_utility_minus_i(self, players: List['Player'], location: str) -> int:
        tmp_sum: int = 0
        for player in players:
            if player.name != self.name:
                tmp_sum += player.get_norm_utility(location=location)

        return tmp_sum


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
        retvalue += '\n'
        retvalue += 'Length: ' + str(self.itin_length)
        return retvalue


class Outcome:
    X: List['Player']
    V: List[str]
    w: int
    f: dict
    p: dict
    t: Tour

    def __init__(self, X, V, w, f, p, t):
        self.X = X
        self.V = V
        self.w = w
        self.f = f
        self.p = p
        self.t = t

    def __str__(self):
        retvalue = '{ players: ['
        for i in self.X:
            retvalue += str(i) + ","
        retvalue += "],\n locations: ["
        for i in self.V:
            retvalue += i + ","
        retvalue += "],\n welfare:"
        retvalue += str(self.w) + ",\n fixed_costs: ["
        for i in self.f.values():
            retvalue += str(i) + ", "
        retvalue += "],\n proportional_costs: ["
        for i in self.p.values():
            retvalue += str(i) + ", "
        retvalue += "],\n tour: " + str(self.t)
        return retvalue


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


# CALL MINIZINC STUFF #########################################################
MINIZINC_MODEL_PATH = 'salesman.mzn'
MINIZINC_DATA_PATH = 'salesman.dzn'


def calc_distance_matrix(L_x: List[str], D_x: List['Distance']) -> List[List[int]]:
    matrix = [[0 for i in range(0, len(L_x))] for j in range(0, len(L_x))]
    for location_row in range(0, len(L_x)):
        for location_column in range(0, len(L_x)):
            if location_row == location_column:
                matrix[location_row][location_column] = 0
            else:
                matrix[location_row][location_column] = Distance.find_distance(D_x, L_x[location_row],
                                                                               L_x[location_column])
    return matrix


def determine_start_index(Start: str, Locations: List[str]) -> int:
    for i in range(0, len(Locations)):
        if Locations[i] == Start:
            return i + 1


def salesman(L_x: List[str], D_x: List['Distance'], Start: str) -> 'Tour':
    distance_matrix = calc_distance_matrix(L_x, D_x)
    start: int = determine_start_index(Start, L_x)
    setup_config_file(dist=distance_matrix, n=len(L_x),
                      start_city=start, city_names=L_x)
    salesman_model = Model(MINIZINC_MODEL_PATH)
    salesman_model.add_file(MINIZINC_DATA_PATH)
    gecode = Solver.lookup('gecode')
    instance = Instance(gecode, salesman_model)
    result: Result = instance.solve()
    str_result = str(result)
    reslist = str_result.split('\n')
    itin = []
    for i in range(0, len(reslist) - 1):
        itin.append(reslist[i])
    t: Tour = Tour(tour_itin=itin, itin_length=reslist[len(reslist) - 1])
    return t


################################################################################


def normalize_preferences(N: List['Player'], L: List[str]):
    m: int = 0
    for player in N:
        tmp = 0
        for location in L:
            if player.get_utility(location) != None and player.get_utility(location) > 0:
                tmp = tmp + 1
        if tmp > m:
            m = tmp
    for player in N:
        player.normalize_utility(bound=m, L=L)


def get_chi(N: List['Player'], L_x: List[str]):
    max = 0
    returnvalue: str = L_x[0]
    for c in L_x:
        tmp = 0
        for i in N:
            tmp += i.normalized_utility[c]
        if (tmp > max):
            max = tmp
            returnvalue = c
    return returnvalue


def constraint_check(X: List['Player'], L_x: List[str], t: 'Tour', MaxLen: int, f: dict, p: dict) -> bool:
    q = t.itin_length
    if MaxLen < int(q):
        return False
    constant: float = len(X) / len(X) - 1
    chi = get_chi(X, L_x)
    payments_of_players: dict = {}

    for player in X:
        summa = 0
        summa2 = 0

        u_bar_minus_player = []
        for pl in X:
            u_bar_minus_player.append(pl)

        u_bar_minus_player.remove(player)
        chi_without_player = get_chi(u_bar_minus_player, L_x)
        
        for agent in u_bar_minus_player:

            summa += agent.normalized_utility[chi_without_player]
            summa2 += agent.normalized_utility[chi]

        payments_of_players[player] = constant * summa - summa2

    denom = sum(payments_of_players.values())
    for player in X:
        f[player] = (payments_of_players[player] / denom) * 50 * len(L_x)
        p[player] = (10 * int(q)) / len(X)
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

    D_X = extract_distance_subset(D, L_x)
    found_one = False
    available_travels = []
    length_of_travel = len(L_x)
    available_travels.append(L_x)
    while (length_of_travel > 1):
        f: dict = {}
        p: dict = {}
        for travel in available_travels:
            found = False
            t: 'Tour' = salesman(travel, D_X, Start)
            found = constraint_check(X, travel, t, MaxLen, f, p)
            if found:
                w: int = 0
                for player in X:
                    w = w + player.sum_normalized_utility(L_x)
                o = Outcome(X, travel, w, f, p, t)
                R.append(o)
                found_one = True
        if not found_one:
            available_travels = []
            length_of_travel = length_of_travel - 1
            tmp_travels = list(itertools.combinations(L_x, length_of_travel))
            for subset in tmp_travels:
                valid = False
                for s in subset:
                    if s == Start:
                        valid = True
                        break
                if valid:
                    available_travels.append(subset)
        else:
            length_of_travel = -1

    if len(R) > 0:
        o_max: 'Outcome'
        w_max: int = 0
        for o in R:
            if o.w > w_max:
                w_max = o.w
                o_max = o
        return o_max
    return None


def can_insert(location: str, L_x: List[str]) -> bool:
    if (L_x is None or location is None):
        return False

    for x in L_x:
        if x == location:
            return False

    return True


def lcl_travel(N: List['Player'], L: List[str], Start: str, D: List[Distance], k: int, MaxLen: int):
    normalize_preferences(N, L)
    N_part: List[List['Player']] = list(list(itertools.combinations(N, k)))
    O = []
    for player_subset in N_part:
        L_x = []
        for player in player_subset:
            for location in L:
                if player.get_utility(location) > 0 and can_insert(location, L_x):
                    L_x.append(location)
        o = best_travel(player_subset, L_x, MaxLen, D, Start, [])
        if o != None:
            O.append(o)

    o_max: 'Outcome'
    w_max: int = 0
    if len(O) > 0:
        for o in O:
            if o.w > w_max:
                w_max = o.w
                o_max = o

        LV = o_max.V
        UT = o_max.X
        CTF = o_max.f
        CTP = o_max.p
        T = o_max.t
        print("**************BEST OUTCOME*******************")
        print(str(o_max))
        print("**************BEST OUTCOME*******************")
        return o_max
    else:
        print("Impossibile determinare il viaggio")
        return None
