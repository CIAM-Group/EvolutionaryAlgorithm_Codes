import csv
import time
import numpy as np

from Application.evaluation import evaluationLeNet5, evaluationAlexNet

# LeNet5 (7CNN) cifar 10
class TPLeNet5(object):
    def __init__(self, num_epochs):
        self.r = 6
        self.dim = 12
        self.num_epochs = num_epochs

        self.N_lst = [4 , 4] + [3, 3] + [2, 2]
        self.bounds = [[6]*4 + [0.1]*2, [256]*4+[0.9]*2]

    def F(self, X):
        size = X.shape[0]
        y = np.zeros(size)
        acc = np.zeros(size)
        for i in range(size):
            acc[i], y[i] = evaluationLeNet5(X[i], num_epochs=self.num_epochs)
        return acc, y

# AlexNet (9 CNN) cifar 10
class TPAlexNet(object):
    def __init__(self, num_epochs):
        self.r = 9
        self.dim = 22
        self.num_epochs = num_epochs

        self.N_lst = [4 for _ in range(5)] + [3 for _ in range(5)] + [2 for _ in range(3)]
        self.bounds = [[32] * 7 + [0.1] * 2, [512] * 7 + [0.9] * 2]

    def F(self, X):
        size = X.shape[0]
        y = np.zeros(size)
        acc = np.zeros(size)
        for i in range(size):
            acc[i], y[i] = evaluationAlexNet(X[i], num_epochs=self.num_epochs)
        return acc, y


# 利用LHS采样得到初始数据
def generate_database(prob, init_size):
    X = np.zeros((init_size, prob.dim))
    cxmin = prob.bounds[0]
    cxmax = prob.bounds[1]

    for j in range(prob.r):
        for i in range(init_size):
            X[i, j] = cxmin[j] + np.random.uniform(i / init_size * (cxmax[j] - cxmin[j]),
                                                         (i + 1) / init_size * (cxmax[j] - cxmin[j]))
        np.random.shuffle(X[:, j])

    for j in range(prob.r, prob.dim):
        for i in range(init_size):
            X[i, j] = int(np.random.uniform(i / init_size * prob.N_lst[j - prob.r],
                                            (i + 1) / init_size * prob.N_lst[j - prob.r]))
        np.random.shuffle(X[:, j])

    return X


if __name__ == "__main__":
    init_size = 100
    #prob = TPLeNet5(num_epochs = 10)
    prob = TPAlexNet(num_epochs = 10)


    # X = generate_database(prob, init_size)

    # LeNet5, AlexNet
    # with open("results/AlexNet_initial_X.csv", "w", newline='') as csvf:
    #     w1 = csv.writer(csvf)
    #     for i in range(init_size):
    #         w1.writerow(X[i])

    X = np.loadtxt("./results/initial_data/AlexNet_initial_X.csv", delimiter=',')

    with open("results/initial_data/AlexNet_cifar10_initial_data.csv", "a+", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(init_size):

            print("Evaluating {}th solution:".format(i+1))
            s = time.time()
            y = prob.F(X[i].reshape(1,-1))
            t = time.time()
            print("Evaluating time : {} s".format(t - s))

            writer.writerow(np.append(X[i], y))













