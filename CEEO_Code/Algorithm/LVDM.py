import numpy as np
from scipy.spatial.distance import cdist
from sklearn import preprocessing
from sklearn.cluster import KMeans
def LVDM(data_x, data_y, samp_dict, d_cn, d_ca, v_ca, Csize):

    no_points = data_x.shape[0]
    # Csize = int(no_points / 25)  # 向下取整
    # Csize = int(-18 / 500 * no_points + 118 / 5)  # 向下取整
    # Csize = int(np.ceil(-76/500 * no_points + 576/5))

    data_cnx = data_x[:, :d_cn]
    data_cax = data_x[:, d_cn:]
    norm_data_cnx = data_pro_min_max(data_cnx)
    index = np.argsort(data_y) + 1
    norm_data_Y = data_pro_min_max(index)
    # = ODD(norm_data_cnx, norm_data_cnx[0], norm_data_Y, norm_data_Y[0])  # 通过连续变量与目标值的排序值来计算
    # sort_index = np.argsort(distMat, axis=0).reshape(-1)
    sort_index = np.argsort(data_y)
    pop_layer = np.array([np.ceil((int((np.argwhere(sort_index == i)[0])) + 1) / no_points * Csize) for i in range(no_points)])
    # pop_cax = pop_x[:, d_cn:]

    km = KMeans(n_clusters=Csize).fit(data_y.reshape(-1, 1))
    pop_layer = km.labels_
    # km = KMeans(n_clusters=Csize).fit(data_y.reshape(-1, 1))
    for j in range(d_ca):
        samp_dict[j] = {}
        X_C = v_ca[j]
        for X_idx in range(len(X_C)):
            samp_idx = list(np.argwhere(X_C[X_idx] == data_cax[:, j])[:, 0])  #
            samp_lay = pop_layer[samp_idx]
            samp_dict[j][X_C[X_idx]] = {}
            samp_dict[j][X_C[X_idx]]['all_lay'] = len(samp_idx)
            if len(samp_idx) != 0:
                samp_dict[j][X_C[X_idx]]['each_lay'] = np.array(
                                 [np.sum(samp_lay == lay_num + 1) for lay_num in range(Csize)])
            else:
                samp_dict[j][X_C[X_idx]]['each_lay'] = np.zeros(Csize)
            if len(samp_idx) == 0:
                samp_dict[j][X_C[X_idx]]['prob'] = np.zeros(Csize)
            else:
                samp_dict[j][X_C[X_idx]]['prob'] = samp_dict[j][X_C[X_idx]]['each_lay'] / \
                                                            samp_dict[j][X_C[X_idx]]['all_lay']
    return samp_dict

def ODD(norm_data_X, norm_data_x_best, norm_data_Y, norm_data_Y_best):


    distMat = cdist(norm_data_X, norm_data_x_best.reshape(1, -1), metric='euclidean') + cdist(norm_data_Y.reshape(-1, 1), norm_data_Y_best.reshape(-1, 1),
                                                                              metric='euclidean')  # metric='euclidean'/ mahalanobis

    return distMat

def data_pro_min_max(input_data):
    norm_data = preprocessing.minmax_scale(input_data)

    return norm_data