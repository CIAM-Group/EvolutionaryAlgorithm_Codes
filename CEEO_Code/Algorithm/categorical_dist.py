import numpy as np



def ca_dist(samp_dict, v_dv, samp_dist):
    l1 = len(v_dv)
    l2 = np.shape(v_dv)[1]
    max_value = np.zeros(l1)
    save_ca_value = np.zeros((l1, l2))
    for i in range(l1):
        n = len(v_dv[i])
        samp_dist[i] = {}
        # samp_dist[i]['max_value']
        for i2 in range(n):
            for i3 in range(i2, n):
                ca_value = abs(v_dv[i, i2] - v_dv[i, i3])
                save_ca_value[i, i3] = ca_value
                samp_dist[i][ca_value] = {}
                if i2 == i3:
                    samp_dist[i][ca_value] = 0
                else:
                    error = np.sum(np.abs(samp_dict[i][v_dv[i, i2]]['prob'] - samp_dict[i][v_dv[i, i3]]['prob']), axis=0)
                    samp_dist[i][ca_value] = error

        samp_dist[i]['max_value'] = max(samp_dist[i].values())
        if samp_dist[i]['max_value'] == 0:
            print(samp_dist[i].values())
# ## 归一化
    return samp_dist