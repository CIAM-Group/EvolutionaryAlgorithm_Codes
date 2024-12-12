import numpy as np




def Cal_pro_ca(num1, num2, data, v_ca, d_cn, d_ca, aph):

    q = 0.05099  # Influene of the best-quality solutions in ACOmv
    # aph = 0.0002      # parameter of UCB

    data_x = data[0][:num1]     #当前种群
    data_y = data[1][:num1]
    K = len(data_y)
    w = np.zeros(K)
    data_x_ca = data_x[:, d_cn:]

    data_x2 = data[0]           #所有评价过的解
    data_y2 = data[1]
    data_x2 = data_x2[:, d_cn:]
    K2 = len(data_y2)
    # a, b = np.shape(v_ca)
    pro_matrix = np.zeros((np.shape(v_ca)))
    UCB_matrix = np.zeros((np.shape(v_ca)))
    value = np.zeros((np.shape(v_ca)))
    var_value = np.zeros((np.shape(v_ca)))

    # for j in range(0, K):
    #     pop_rank = j
    #     # w[j] = (1 / (q * K * np.pi)) \
    #     #        * np.exp(-((pop_rank - 1) ** 2) / (2 * (q * K) ** 2))  # the original paper is sqrt(2)
    #     w[j] = (K - pop_rank)/K
    # w = range(K, 0, 1/K)
    # w = np.linspace(K, 0, 1/K)
    w = np.linspace(start = 1, stop=0, num=K)
    # print(len(w))
    for i in range(v_ca.shape[0]):
        e_value_save = []
        w_value_save = []
        for j in range(v_ca.shape[1]):
            samp_idx = list(np.argwhere(data_x2[:, i] == v_ca[i, j])[:, 0])
            num_samp = len(samp_idx)
            samp_idx2 = list(np.argwhere(data_x_ca[:, i] == v_ca[i, j])[:, 0])
            if len(samp_idx2) > 0:
                # print(w[samp_idx2])
                value[i, j] = np.max(w[samp_idx2], axis=0)
                e_value_save.append(value[i, j])
            else:
                if len(samp_idx) > 0:
                    value[i, j] = 0
                    e_value_save.append(value[i, j])
                else:
                    value[i, j] = -1
                    w_value_save.append(j)
            var_value[i, j] = np.sqrt(aph*np.log2(K2+v_ca.shape[1])/(num_samp+1))

        if len(w_value_save) > 0:
            for jj in range(len(w_value_save)):
                value[i, w_value_save[jj]] = np.mean(e_value_save)
    for i in range(v_ca.shape[0]):
        for j in range(v_ca.shape[1]):

            UCB_matrix[i, j] = value[i, j] + var_value[i, j]

    for i in range(v_ca.shape[0]):
        # temp = np.exp(UCB_matrix[i, :])
        temp = UCB_matrix[i, :]
        for j in range(v_ca.shape[1]):
            if j == 0:
                pro_matrix[i, j] = np.sum(temp[j]) / np.sum(temp)           # 轮盘赌选择
            else:
                pro_matrix[i, j] = np.sum(temp[0:(j+1)]) / np.sum(temp)     # 轮盘赌选择


    return pro_matrix




