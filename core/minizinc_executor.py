from posixpath import split
from minizinc import Solver, Model, Instance, Result
from typing import List
from algorithms import Distance, Tour
from file_handler import setup_config_file
MINIZINC_MODEL_PATH = 'minizinc_model/salesman'

def calc_distance_matrix(L_x: List[str], D_x: List['Distance']) -> List[List[int]]:
    matrix = [[0 for i in range(0, len(L_x))] for j in range(0, len(L_x))]
    for location_row in range(0, len(L_x)):
        for location_column in range(0, len(L_x)):
            if location_row == location_column:
                matrix[location_row][location_column] = 0
            else: 
                matrix[location_row][location_column] = Distance.find_distance(D_x,L_x[location_row], L_x[location_column])
    return matrix    

def determine_start_index(Start: str, Locations: List[str]) -> int:
    for i in range(0, len(Locations)):
        if Locations[i] == Start:
            return i+1

def salesman(L_x : List[str], D_x: List['Distance'], Start: str) -> 'Tour':
    distance_matrix = calc_distance_matrix(L_x, D_x)
    start: int = determine_start_index(Start, L_x)
    setup_config_file(dist=distance_matrix, n=len(L_x), start_city=start, city_names=L_x)
    salesman_model = Model(MINIZINC_MODEL_PATH+'.mzn')
    salesman_model.add_file(MINIZINC_MODEL_PATH+'.dzn')
    gecode = Solver.lookup('gecode')
    instance = Instance(gecode, salesman_model)
    result: Result = instance.solve()
    str_result = str(result)
    reslist = str_result.split('\n')
    itin = []
    for i in range(0, len(reslist)-1):
        itin.append(reslist[i])
    t: Tour = Tour(tour_itin=itin, itin_length=reslist[len(reslist)-1])
    print(t)