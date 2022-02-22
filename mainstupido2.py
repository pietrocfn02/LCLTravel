from typing import List
from src.algorithms import Player, normalize_preferences, Distance, constraint_check, salesman, best_travel, lcl_travel

locations: List[str] = ['Cosenza', 'Catanzaro', 'Vibo', 'Crotone', 'Reggio']
u1: dict = {}
u1['Cosenza'] = 15
u1['Catanzaro'] = 10
u1['Vibo'] = 25
u1['Crotone'] = 0
u1['Reggio'] = 2
u2: dict = {}
u2['Cosenza'] = 7
u2['Catanzaro'] = 0
u2['Vibo'] = 0
u2['Crotone'] = 0
u2['Reggio'] = 10
u3: dict = {}
u3['Cosenza'] = 5
u3['Catanzaro'] = 4
u3['Vibo'] = 3
u3['Crotone'] = 2
u3['Reggio'] = 1

p1 = Player(name="Santino", utility=u1, cost_bound=3000)
p2 = Player(name="Pietro", utility=u2, cost_bound=3000)
p3 = Player(name="Claudio", utility=u3, cost_bound=3000)


X = [p1, p2, p3]


#normalize_preferences(X, locations)

#p1_bar = p1.get_utilities()
#p2_bar = p2.get_utilities()
#p3_bar = p3.get_utilities()

# print(p1_bar)
# print(p2_bar)
# print(p3_bar)

#L_X = ['Dubai','Roma','Reggio','Crotone','Vibo']

D_x = []
Start = 'Cosenza'

d = Distance('Cosenza', 'Catanzaro', 50)
D_x.append(d)
d = Distance('Cosenza', 'Vibo', 180)
D_x.append(d)
d = Distance('Cosenza', 'Crotone', 85)
D_x.append(d)
d = Distance('Cosenza', 'Reggio', 40)
D_x.append(d)
d = Distance('Catanzaro', 'Vibo', 140)
D_x.append(d)
d = Distance('Catanzaro', 'Crotone', 70)
D_x.append(d)
d = Distance('Catanzaro', 'Reggio', 60)
D_x.append(d)
d = Distance('Vibo', 'Crotone', 90)
D_x.append(d)
d = Distance('Vibo', 'Reggio', 180)
D_x.append(d)
d = Distance('Crotone', 'Reggio', 115)
D_x.append(d)

#t = salesman(L_X, D_x,Start)


lcl_travel(X, locations, Start, D_x, 2, 300)
