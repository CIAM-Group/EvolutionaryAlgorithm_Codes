import numpy as np


def DE_1(P, F, CR, UB, LB):

    NP, Dim = np.shape(P)
    U = np.zeros((NP, Dim))
    V = np.zeros((NP, Dim))
    for i in range(0, NP):
        # mutation
        k0 = np.random.randint(0, NP - 1)
        while k0 == i:
            k0 = np.random.randint(1, NP)
            #P1 = P[k0, :]
        k1 = np.random.randint(1, NP - 1)
        while k1 == i | k1 == k0:
            k1 = np.random.randint(1, NP - 1)
            #P2 = P[k1, :]
        k2 = np.random.randint(1, NP - 1)
        while k2 == i | k2 == k1 | k2 == k0:
            k2 = np.random.randint(1, NP - 1)
            #P3 = P[k2, :]
        #V_1 = P1 + F * (P2-P3)
        V[i, :] = P[k0, :] + F * (P[k1, :] - P[k2, :])
        # bound
        for j in range(Dim):
            if LB <= V[i, j] <= UB:
                V[i, j] = V[i, j]
            else:
                V[i, j] = LB + np.random.random() * (UB - LB)
        # crossover
        jrand = np.random.randint(0, Dim)
        for j in range(Dim):
            k3 = np.random.random()
            if k3 > CR and j != jrand:
                U[i, j] = P[i, j]
            else:
                U[i, j] = V[i, j]
    return U
    #print(U)
def DE_2(P, F, CR, UB, LB):
#DE/best/1

    NP, Dim = np.shape(P)
    X_best = P[0, :]
    U = np.zeros((NP, Dim))
    V = np.zeros((NP, Dim))
    UB = 100
    LB = -100
    for i in range(0, NP):
        # mutation
        k0 = np.random.randint(0, NP - 1)
        while k0 == i:
            k0 = np.random.randint(1, NP)
            #P1 = P[k0, :]
        k1 = np.random.randint(1, NP - 1)
        while k1 == i | k1 == k0:
            k1 = np.random.randint(1, NP - 1)
            #P2 = P[k1, :]
            #P3 = P[k2, :]
        #V_1 = P1 + F * (P2-P3)
        V[i, :] = X_best + F * (P[k0, :] - P[k1, :])
        # bound
        for j in range(Dim):
            if LB <= V[i, j] <= UB:
                V[i, j] = V[i, j]
            else:
                V[i, j] = LB + np.random.random() * (UB - LB)

        jrand = np.random.randint(0, Dim-1)
        for j in range(Dim):
            k3 = np.random.random()
            if k3 > CR and j != jrand:
                U[i, j] = P[i, j]
            else:
                U[i, j] = V[i, j]
    return U
    #print(U)
def DE_3(P, F, CR, UB, LB):

    NP, Dim = np.shape(P)
    U = np.zeros((NP, Dim))
    V = np.zeros((NP, Dim))
    for i in range(0, NP):
        # mutation
        k0 = np.random.randint(0, NP - 1)
        while k0 == i:
            k0 = np.random.randint(1, NP)
            #P1 = P[k0, :]
        k1 = np.random.randint(1, NP - 1)
        while k1 == i | k1 == k0:
            k1 = np.random.randint(1, NP - 1)
            #P2 = P[k1, :]
        k2 = np.random.randint(1, NP - 1)
        while k2 == i | k2 == k1 | k2 == k0:
            k2 = np.random.randint(1, NP - 1)
            #P3 = P[k2, :]
        #V_1 = P1 + F * (P2-P3)
        k3 = np.random.randint(1, NP - 1)
        while k3 == i | k3 == k2 | k2 == k1 | k1 == k0:
            k3 = np.random.randint(1, NP - 1)
        k4 = np.random.randint(1, NP - 1)
        while k4 == i | k4 == k3 | k3 == k2 | k2 == k1 | k1 == k0:
            k4 = np.random.randint(1, NP - 1)
        V[i, :] = P[k0, :] + F * (P[k1, :] - P[k2, :]) + F * (P[k3, :] - P[k4, :])
        # bound
        for j in range(Dim):
            if LB <= V[i, j] <= UB:
                V[i, j] = V[i, j]
            else:
                V[i, j] = LB + np.random.random() * (UB - LB)
        # crossover
        jrand = np.random.randint(0, Dim)
        for j in range(Dim):
            k3 = np.random.random()
            if k3 > CR and j != jrand:
                U[i, j] = P[i, j]
            else:
                U[i, j] = V[i, j]
    return U

def DE_4(P, F, CR, UB, LB):
#DE/current-rand/

    NP, Dim = np.shape(P)
    U = np.zeros((NP, Dim))
    V = np.zeros((NP, Dim))
    for i in range(0, NP):
        # mutation
        k0 = np.random.randint(0, NP - 1)
        while k0 == i:
            k0 = np.random.randint(1, NP)
            #P1 = P[k0, :]
        k1 = np.random.randint(1, NP - 1)
        while k1 == i | k1 == k0:
            k1 = np.random.randint(1, NP - 1)
            #P2 = P[k1, :]
        k2 = np.random.randint(1, NP - 1)
        while k2 == i | k2 == k1 | k2 == k0:
            k2 = np.random.randint(1, NP - 1)
            #P3 = P[k2, :]
        #V_1 = P1 + F * (P2-P3)
        V[i, :] = P[k0, :] + F * (P[k1, :] - P[k0, :]) + F * (P[k1, :] - P[k2, :])
        # bound
        for j in range(Dim):
            if LB <= V[i, j] <= UB:
                V[i, j] = V[i, j]
            else:
                V[i, j] = LB + np.random.random() * (UB - LB)
        # crossover
        jrand = np.random.randint(0, Dim)
        for j in range(Dim):
            k3 = np.random.random()
            if k3 > CR and j != jrand:
                U[i, j] = P[i, j]
            else:
                U[i, j] = V[i, j]
    return U





















