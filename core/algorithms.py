import itertools

def normalize_preferences(u, N, L):
    m = 0
    u_bar = [ [0 for i in range(0, len(N))] for j in range(0, len(L))]
    for i in range(0, len(N)):
        tmp = 0
        for j in range(0, len(L)):
            if u[i][j] > 0:
                tmp += u[i][j]
        if tmp > m:
            m = tmp
    for j in range (0, len(N)):
        max_j = max(u[j])
        for k in range (0, len(L)):
            u_bar[j][k] = m * (u[j][k]/max_j)

    return u_bar


def minimum_spanning_tree(self, a, g, r):
    pass


def constraint_check(self, X, L_x, q, c, MaxLen, u_bar, f, p):
    if MaxLen > q:
        return False

    for i in range (0, len(X)):
        tmp = 0
        f[i] = 0
        p[i] = 0
        for j in range (0, len(L_x)):
            d = 0
            for k in range (0, len(X)):
                d += u_bar[k][j]
            tmp = (50 * u_bar[j])/d
            f[i] += tmp
        p[i] = (10*q)/len(X)
        if f[i] + p[i] > c[i]:
            return False
    
    return True

def D(l1, l2):
    return 0


def best_travel(X, L_x, u_bar, c, MaxLen, D, Start):
    found = False
    R = []
    while (len(R) == 0):
        f,p = [0 for i in range(0, len(X))]
        G = [[0 for i in range(0, len(L_x))] for j in range(0, len(L_x))]
        End = ""

        q = minimum_spanning_tree(G, Start, End)





def lcl_travel(self, N, L, Start, D, u, k, c, MaxLen):
    u_bar = normalize_preferences(u,N,L)
    N_part = list(itertools.combinations(N,k))
    O = []
    for x in range(0, len(N_part)):
        L_x = []
        for i in range(0, len(x)):
            for l in range(0, len(L)):
                if(u_bar[i][l]>0):
                    L_x.append(L[l])
        o = best_travel(x, L_x, u_bar, c, MaxLen, D, Start)
        O.append(o)
    
    o_hat = None
    w_max = 0
    '''for o in range(0, len(O)):
        if()'''
    #Da finire


    


