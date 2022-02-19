from typing import List
from algorithms import Player, normalize_preferences
locations: List[str] = ['Cosenza', 'Catanzaro', 'Roma','Crotone','Dubai']
u1: dict = {}
u1['Cosenza'] = 15
u1['Catanzaro'] = 10
u1['Roma'] = 25
u1['Crotone'] = 0
u1['Dubai'] = 0
u2 = dict = {}
u2['Cosenza'] = 7
u2['Catanzaro'] = 0
u2['Roma'] = 0
u2['Crotone'] = 0
u2['Dubai'] = 0
u3 = dict = {}
u3['Cosenza'] = 5
u3['Catanzaro'] = 4
u3['Roma'] = 3
u3['Crotone'] = 2
u3['Dubai'] = 1

p1 = Player(name = "Santino", utility = u1,cost_bound=1000)
p2 = Player(name = "Pietro", utility = u2, cost_bound=1400)
p3 = Player(name = "Claudio", utility = u3, cost_bound=1500) 


X = [p1,p2,p3]


normalize_preferences(X, locations)

p1_bar = p1.get_utilities()
p2_bar = p2.get_utilities()
p3_bar = p3.get_utilities()


print(p1_bar)
print(p2_bar)
print(p3_bar)