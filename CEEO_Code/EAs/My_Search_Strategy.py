import numpy as np
from EAs.De_operator_2 import DE_2


def RW_Select(p_set):
    lvalue = np.random.rand(1)
    probability = 0
    for i in range(np.size(p_set, 0)):
        probability += p_set[i]
        if probability >= lvalue:
                idx2 = i
                break
    return idx2



def Roulette(len_c, v_dv, pro_matrix):

    x_c = np.zeros([1, len_c])
    for j in range(0, len_c):
        jtemp = np.argwhere(np.random.random() <= pro_matrix[j, :])

        Select_ca = jtemp[0]


        x_c[0, j] = v_dv[j, Select_ca]
    x_c = x_c.astype(float)
    return x_c


#################################
def DEUCB(K , M , database, len_r, len_c, dn_r, up_r, N_lst, v_dv, pro_matrix):

    pop_x = database[0][:K]


    x_c_generate = np.zeros((M,len_c))


    x_r_generate = DE_2(pop_x[:, :len_r], 0.5, 0.8, up_r, dn_r)
    for i in range(0, M):

        x_c_generate[i, :] = Roulette(len_c, v_dv, pro_matrix)

    return x_r_generate, x_c_generate
#################################