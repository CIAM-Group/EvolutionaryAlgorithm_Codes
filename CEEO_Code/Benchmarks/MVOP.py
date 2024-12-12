import numpy as np
from categorical_set import my_categorical_set

class MVOPT(object):
    def __init__(self, prob_name, dim_c, dim_d):

        self.r = dim_c
        self.o = dim_d
        self.dim = dim_c + dim_d
        if len(prob_name):
            f, v_dv, N_lst, _ = my_categorical_set(prob_name,  self.dim)
        else:
            raise NotImplementedError
        self.N_d = N_lst[0] #每个位置的类变量集合的数目都相等
        self.v_dv = v_dv
        self.N_lst = N_lst
        self.bounds = [-100, 100]
        self.F = f
        # self.x_shift = np.loadtxt("Benchmarks/shift_data/data_" + prob_name + '.txt')[:self.dim].reshape(1, -1)
        self.M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt')[:self.dim].reshape(10, 10)
