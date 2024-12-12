import numpy as np
from EAs.DE import DE
from Surrogate.RBFNmv import RBFNmv
from smt.surrogate_models import KRG
from Algorithm.LVDM import LVDM
from Algorithm.categorical_dist import ca_dist
from EAs.My_Search_Strategy import DEUCB
from Cal_pro_ca import Cal_pro_ca
from scipy.spatial.distance import pdist, cdist

class Pop:
    def __init__(self, X, F):
        self.X = X
        self.F = F    # evaluation function
        self.realObjV = None
        self.predObjV = None

    def pred_fit(self, sm):
        self.predObjV = sm.predict(self.X)

    # function evaluation
    def cal_fitness(self, X):
        return self.F(X)

# Algorithm class
class CEEO(object):
    def __init__(self, maxFEs, popsize, dim, clb, cub, N_lst, v_dv, prob, r, database=None):


        self.maxFEs = maxFEs
        self.popsize = popsize

        self.dim = dim
        self.cxmin = np.array(clb)
        self.cxmax = np.array(cub)
        self.N_lst = N_lst
        self.v_dv = v_dv

        self.prob = prob
        self.r = r
        self.o = self.dim - self.r
        self.c_result = []
        # surrogate models
        self.global_sm = None
        self.local_sm1 = None
        self.local_sm2 = None
        self.sm3 = None

        self.pop = None
        self.database = None
        self.init_size = 100  # the size of initial samples
        self.gen = None

        self.xbest = None
        self.ybest = None
        self.ybest_lst = []

        self.data = None
        self.melst = []
        self.samp_dict = {}
        self.samp_dist = {}
        self.Layer = self.init_size
        self.apha = 0
        ####################参数

        self.aph = 0.0001
        self.phi = 0.5
        self.tau = 3
        ####################
    # build or update the global surrogate model using all data
    def updateGSM(self):

        xtrain = self.database[0]
        ytrain = self.database[1]


        sm = RBFNmv(self.dim, self.N_lst, self.cxmin, self.cxmax, self.samp_dist, self.Layer)

        sm.fit(xtrain, ytrain)

        self.global_sm = sm




    def updateLSM2(self):


        xtrain = self.database[0][:int(self.phi*self.popsize)]
        ytrain = self.database[1][:int(self.phi*self.popsize)]

        sm = RBFNmv(self.dim, self.N_lst, self.cxmin, self.cxmax, self.samp_dist, self.Layer)


        sm.fit(xtrain, ytrain)
        self.local_sm2 = sm

    # Inilization
    def initPop(self):

        X = np.zeros((self.init_size, self.dim))
        inity = np.zeros((self.init_size))
        area = self.cxmax - self.cxmin
        # continuous part
        for j in range(self.r):
            for i in range(self.init_size):
                X[i, j] = self.cxmin[j] + np.random.uniform(i / self.popsize * area[j],
                                                            (i + 1) / self.popsize * area[j])
            np.random.shuffle(X[:, j])
        #
        for j in range(self.r, self.dim):
            for i in range(self.init_size):
                v_ca = self.v_dv[j - self.r]
                X[i, j] = v_ca[np.random.randint(self.N_lst[j - self.r])]

                # discrete part
        for j in range(self.init_size):
            inity[j] = self.prob(X[j, :])
        for j in range(self.init_size):
            if j == 0:
                self.c_result.append(np.min(inity[j]))
            else:
                self.c_result.append(np.min(inity[0:j]))
        self.gen = self.init_size
        inds = np.argsort(inity)
        self.database = [X[inds], inity[inds]]
        self.data = [X[inds], inity[inds]]

        popInds = inds[:self.popsize]
        self.pop = Pop(X[popInds], self.prob)
        self.pop.realObjV = inity[popInds]

        self.xbest = self.database[0][0]
        self.ybest = self.database[1][0]

        if self.gen >= int(self.apha *self.maxFEs):
            self.samp_dict = LVDM(self.pop.X, self.pop.realObjV, self.samp_dict,
                                  self.r, self.o, self.v_dv, self.Layer)
            self.samp_dist = ca_dist(self.samp_dict, self.v_dv, self.samp_dist)

    # Check for duplicate samples
    def check(self, x):
        num = self.database[1].shape[0]
        datx_x = self.database[0]
        x = x.reshape(1, -1)
        xx = x[:, :self.r]
        distance = cdist(xx, datx_x[:, :self.r]).reshape(-1)
        for i in range(num):
            if distance[i] == 0:
                return False
        return True


    # update the database and current population
    def update_database(self, X, y):
        self.data[0] = np.r_[self.data[0], X]
        self.data[1] = np.append(self.data[1], y)

        size = len(self.database[1])
        for i in range(size):
            if (self.database[1][i] > y):
                self.database[0] = np.insert(self.database[0], i, X, axis=0)
                self.database[1] = np.insert(self.database[1], i, y)
                break

        self.pop.X = self.database[0][:self.popsize]
        self.pop.realObjV = self.database[1][:self.popsize]
        self.xbest = self.database[0][0]
        self.ybest = self.database[1][0]

        if self.gen >= int(self.apha * self.maxFEs):
            self.samp_dict = LVDM(self.database[0], self.database[1], self.samp_dict,
                                  self.r, self.o, self.v_dv, self.Layer)
            self.samp_dist = ca_dist(self.samp_dict, self.v_dv, self.samp_dist)

    # Select samples with the same value as the current optimal discrete values for continuous refining
    def data_selection2(self):
        best_c = self.xbest[self.r:]
        inds = []
        for i in range(len(self.database[1])):
            if (np.all(self.database[0][i, self.r:] == best_c)):
                inds.append(i)

        X_r = self.database[0][inds, :self.r]
        y_r = self.database[1][inds]
        size = len(y_r)

        if (size > self.tau * self.r):
            ssinds = np.argsort(y_r)
            effsamples = []
            effsamples.append(ssinds[0])
            for i in range(1, size):
                if ((y_r[ssinds[i]] - y_r[ssinds[i - 1]]) / y_r[ssinds[i - 1]] > 1e-3):
                    effsamples.append(ssinds[i])

            if len(effsamples) > 11 * self.r:
                X_r = X_r[effsamples[:11 * self.r]]
                y_r = y_r[effsamples[:11 * self.r]]
            else:
                X_r = X_r[effsamples]
                y_r = y_r[effsamples]

            size = len(y_r)

        return size, X_r, y_r

    # Continuous refining
    def SAR_local(self, X_r, y_r):
        self.sm3 = KRG(print_global=False, n_start = 1)
        self.sm3.set_training_values(X_r, y_r)
        self.sm3.train()

        ga = DE(max_iter=50, func=self.sm3.predict_values, dim=self.r, lb=self.cxmin, ub=self.cxmax,
                initX=X_r)
        X_l = ga.run()

        return np.append(X_l, self.xbest[self.r:]).reshape(1, -1)

    def run(self):

        if self.database is None:
            self.initPop()
        else:

            initX = self.database[0]
            inity = self.database[1]
            inds = np.argsort(inity)

            self.data = [initX[inds], inity[inds], self.database[2][inds]]
            self.database = [initX[inds], inity[inds]]

            self.pop = Pop(initX, self.prob)
            self.pop.realObjV = inity
            self.xbest = self.database[0][0]
            self.ybest = self.database[1][0]
            self.gen = len(self.database[1])


        flag = "l1"
        while (self.gen < self.maxFEs and self.ybest != 0):


            if flag == "l1":
                self.updateGSM()
                K1 = 100
                M1 = 100

                self.Pro_matrix = Cal_pro_ca(K1, M1, self.database, self.v_dv, self.r, self.o, self.aph)
                x_r_generate, x_c_generate = DEUCB(K1, M1, self.database, self.r, self.o, self.cxmin[1],
                                                              self.cxmax[1],
                                                              self.N_lst, self.v_dv, self.Pro_matrix)
                X = np.concatenate((x_r_generate, x_c_generate), axis=1)
                predObjV = self.global_sm.predict(X)
                index = np.argmin(predObjV)
                x1 = X[index, :]
                if self.check(x1) and self.gen < self.maxFEs:
                    y1 = self.pop.cal_fitness(x1)

                    print("{}/{} gen x1: {}{}".format(self.gen, self.maxFEs, y1,' Global model'))

                    if y1 < self.ybest:
                        flag = "l1"
                    else:
                        flag = "l2"
                    self.update_database(x1.reshape(1, -1), y1)
                    self.melst.append(1)
                    self.ybest_lst.append(self.ybest)
                    self.c_result.append(self.ybest)
                    self.gen += 1
                else:
                    flag = "l2"
            else:

                self.updateLSM2()
                K2 = int(self.phi * self.popsize)
                M2 = K2

                self.Pro_matrix = Cal_pro_ca(M2, K2, self.database, self.v_dv, self.r, self.o, self.aph)
                x_r_generate2, x_c_generate2 = DEUCB(K2, M2, self.database, self.r, self.o, self.cxmin[1],
                                                                self.cxmax[1], self.N_lst, self.v_dv, self.Pro_matrix)
                X2 = np.concatenate((x_r_generate2, x_c_generate2), axis=1)
                predObjV = self.local_sm2.predict(X2)
                index = np.argmin(predObjV)
                x2 = X2[index, :]
                if self.check(x2) and self.gen < self.maxFEs:
                    y2 = self.pop.cal_fitness(x2)
                    print("{}/{} gen x2: {}{}".format(self.gen, self.maxFEs, y2, ' Local model'))
                    if y2 < self.ybest:
                        flag = "l2"
                    else:
                        flag = "l1"

                    self.update_database(x2.reshape(1, -1), y2)
                    self.melst.append(2)
                    self.ybest_lst.append(self.ybest)
                    self.c_result.append(self.ybest)
                    self.gen += 1
                else:

                    flag = "l1"

            # Local continuous search
            size, X_r, y_r = self.data_selection2()
            if (size >= self.tau * self.r):
                x4 = self.SAR_local(X_r, y_r)
                if (self.check(x4) and self.gen < self.maxFEs):
                    y4 = self.pop.cal_fitness(x4)
                    print("{}/600 gen x4: {}{}".format(self.gen, y4, ' GP assisted local search'))
                    self.update_database(x4, y4)
                    self.melst.append(4)
                    self.ybest_lst.append(self.ybest)
                    self.c_result.append(self.ybest)
                    self.gen += 1



        return self.xbest, self.ybest, self.ybest_lst, self.data, self.melst,  self.c_result


