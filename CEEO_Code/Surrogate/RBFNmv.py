
import numpy as np
from scipy import stats
from sklearn.base import BaseEstimator
from scipy.spatial.distance import cdist

class RBFNmv(BaseEstimator):
    def __init__(self, dim, N_lst, cxmin, cxmax, samp_dist, layer):
        '''
        :param dim: the dimension of decision variables
        :param N_lst: the number of values for discrete variables
        :param cxmin: the lower bounds of continuous decision variables
        :param cxmax: the upper bounds of continuous decision variables
        '''
        self.dim = dim
        self.num_neurons = None
        self.sigma = None
        self.centers = None
        self.cxmin = cxmin
        self.cxmax = cxmax

        self.weights = None
        self.bias = None

        self.N_lst = N_lst
        self.o = len(N_lst)
        self.r = self.dim - self.o
        self.samp_dist = samp_dist
        self.Layer = layer

    def VDM(self, X_C):
        VDM_X_C = np.zeros((self.o, self.Layer))
        gen_num = max(self.samp_dict.keys())
        for j in range(self.o):
            if X_C[j] in self.samp_dict[gen_num][j].keys():
                VDM_X_C[j, :] = self.samp_dict[gen_num][j][X_C[j]]['prob']
            else:
                VDM_X_C[j, :] = np.array([0, 0, 0, 0])
                print('No results!')
        return VDM_X_C.transpose()

    # Gower distance based Gaussian kernel
    def kernel_(self, data_point):
        n1 = data_point.shape[0]
        n2 = self.centers.shape[0]
        D = data_point.shape[1]

        # 连续变量（街区距离）
        rdistMat = np.zeros((n1, n2))
        xr1 = data_point[:, :self.r]
        xr2 = self.centers[:, :self.r]
        xr1_ca = data_point[:, self.r:]
        xr2_ca = self.centers[:, self.r:]
        x12 = np.concatenate((xr1, xr2), axis=0)
        cmax = np.max(x12, axis=0)
        cmin = np.min(x12, axis=0)
        norm_data = np.append(xr1, xr2, axis=0)

        cdisMat = np.zeros((n1, n2))

        for i in range(n1):
            rdistMat[i, :] = np.sum(np.abs(xr1[i] - xr2) / (self.cxmax - self.cxmin), axis=1)   ############################修改在这里######################################

            for i2 in range(n2):
                distance = 0
                for i3 in range(self.o):
                    ca_value = abs(xr1_ca[i, i3] - xr2_ca[i2, i3])
                    if self.samp_dist[i3]['max_value'] != 0:

                        distance = distance + self.samp_dist[i3][ca_value] / self.samp_dist[i3]['max_value']
                cdisMat[i, i2] = distance


        distMat = (rdistMat + cdisMat) / D

        return np.exp(-0.5 * distMat / self.sigma ** 2)

        # return np.exp(distMat)

    def calsigma(self):
        max = 0.0
        num = 0
        total = 0.0
        for i in range(self.num_neurons - 1):
            for j in range(i + 1, self.num_neurons):

                d1 = np.sum(np.abs(self.centers[i, :self.r] - self.centers[j, :self.r]).reshape(1, -1) / (self.cxmax - self.cxmin), axis=1)
                d2 = 0
                for i3 in range(self.o):
                    ca_value = abs(self.centers[i, self.r + i3] - self.centers[j, self.r + i3])
                    d2 = d2 + self.samp_dist[i3][ca_value] / self.samp_dist[i3]['max_value']

                d = d1 + d2
                dis = d
                total = total + dis
                num += 1
                if dis > max:
                    max = dis
        self.sigma = 2 * total / num


    # kmeans聚类
    def kmeans(self, X, n_clusters):

        nums, dim = X.shape

        # 选取初始聚类中心
        c_s = np.random.choice(np.arange(nums), n_clusters, replace=False)
        centers = X[c_s, :]

        clusters_lst = [[] for i in range(n_clusters)]

        delta = np.inf
        c = 0

        while (delta > 1e-4 and c < 500):
            c_f = centers.copy()
            ####################
            nums2, dim2 = centers.shape
            dist_c = np.zeros((nums2))


            X_ca = X[:, self.r:]
            centers_ca = centers[:, self.r:]
            for i in range(nums):
                dist_r = np.sum(np.abs(X[i, :self.r] - centers[:, :self.r])/(self.cxmax - self.cxmin), axis=1)

                for i2 in range(nums2):
                    distance = 0
                    for i3 in range(self.o):
                        ca_value = abs(X_ca[i, i3] - centers_ca[i2, i3])
                        if self.samp_dist[i3]['max_value'] != 0:
                            distance = distance + self.samp_dist[i3][ca_value] / self.samp_dist[i3]['max_value']
                    dist_c = distance

                dist = dist_c + dist_r
                ######################
                ind = np.argmin(dist)
                clusters_lst[ind].append(i)

            for k in range(n_clusters):
                centers[k, :self.r] = np.mean(X[clusters_lst[k], :self.r], axis=0)
                t = stats.mode(X[clusters_lst[k], self.r:])[0]
                centers[k, self.r:] = t[0] if len(t != 0) else centers[np.random.randint(0, n_clusters), self.r:]

            clusters_lst = [[] for i in range(n_clusters)]
            c_b = centers[:]
            delta = np.sum((c_f - c_b) ** 2)
            c += 1

        return c_f

    # 求违逆(对最初数据计算不含增量的违逆)
    def pinv(self, A, reg):
        return np.linalg.inv(reg * np.eye(A.shape[1]) + A.T.dot(A)).dot(A.T)

    def fit(self, X, Y):

        self.num_neurons = int(X.shape[0] / 2)
        self.centers = self.kmeans(X, n_clusters=self.num_neurons)

        self.calsigma()
        G = self.kernel_(X)
        temp = np.column_stack((G, np.ones((X.shape[0]))))
        temp = np.dot(np.linalg.pinv(temp), Y)
        self.weights = temp[:self.num_neurons]
        self.bias = temp[self.num_neurons]

    def predict(self, X):

        G = self.kernel_(X)
        predictions = np.dot(G, self.weights) + self.bias
        return predictions




