from algorithms import Distance, salesman

L_X = ['Dubai','Roma','Reggio','Crotone','Vibo']
D_x = []
Start = 'Dubai'

d = Distance('Dubai','Roma',50)
D_x.append(d)
d = Distance('Dubai','Reggio',180)
D_x.append(d)
d = Distance('Dubai','Vibo',85)
D_x.append(d)
d = Distance('Dubai','Crotone',40)
D_x.append(d)
d = Distance('Roma','Reggio',140)
D_x.append(d)
d = Distance('Roma','Vibo',70)
D_x.append(d)
d = Distance('Roma','Crotone',60)
D_x.append(d)
d = Distance('Reggio','Vibo',90)
D_x.append(d)
d = Distance('Reggio','Crotone',180)
D_x.append(d)
d = Distance('Vibo','Crotone',115)
D_x.append(d)

salesman(L_X, D_x,Start) 

