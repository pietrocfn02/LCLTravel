# IMPORTANT!: file input of minizinc: 'piccione_viaggiatore.dzn'
from os import chdir
from typing import List


FILE_CONFIG_NAME = 'piccione_viaggiatore.dzn'


def setup_config_file(n: int, dist: List[List[int]], start_city: int, city_names: List[str]):
    chdir('core/minizinc_model/')
    with open(FILE_CONFIG_NAME, 'w') as o:
        o.write(f'n = {n};\n')
        o.write('dist = [|\n')
        for i in range(n):
            for j in range(n):
                if j == n - 1:
                    o.write(f'{dist[i][j]}|\n')
                else:
                    o.write(f'{dist[i][j]},')
        o.write('];')
        o.write(f'\nstart_city = {start_city};')
        o.write('\ncity_names = [')
        for i in range(n):
            if i == n - 1:
                o.write(f'{city_names[i]}')
            else:
                o.write(f'{city_names[i]},')
        o.write('];')


def read_output_tsp():
    # TODO: read the output of minizinc with the help of the python plugin for minizinc
    pass
