

import numpy as np

# =============================================================================
# Rosenbrock Function (f_min = 0)
# https://www.sfu.ca/~ssurjano/rosen.html
# =============================================================================


def F1(X):
    # X 是连续变量与类变量的组合
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)
    x0 = [7.7624, -51.0984, -95.5110, -68.7425, 8.7344, 0.0577, -36.7734, 44.3837, 99.8131, -12.1793]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z = z2 ** 2
    y = z.sum()

    return y.astype(float)

def F2(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)
    # ht is a categorical index
    # X is a continuous variable
    x0 = [0.5876, -84.9703, -97.8543, 39.7223, 28.3686, 61.1286, 38.9558, -77.1346, 50.6776, 14.4813]
    z1 = X-x0
    z2 = np.dot(z1, M)
    z2 = z2/20
    cos_z2 = np.cos(2*np.pi*z2)
    z = z2**2
    y = np.sum(z-10*cos_z2+10)
    return y.astype(float)

def F3(X):
    # ht is a categorical index
    # X is a continuous variable
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)
    x0 = [5.3830, 0.1560, 47.8659, -17.0994, -32.5756, -29.2208, -32.7262, -43.5349, 1.9141, -36.7252]
    z1 = X-x0
    z2 = np.dot(z1, M)
    z2 = z2/3
    D = 10
    e = np.exp(1)
    z = z2**2
    # y = (20+e-20*np.exp(-0.2*np.sqrt((1/D)*np.sum(z, axis=1)))-np.exp((1/D)*np.sum(np.cos(2*np.pi*z2),axis=1)))
    y = (20 + e - 20 * np.exp(-0.2 * np.sqrt((1 / D) * np.sum(z))) - np.exp(
        (1 / D) * np.sum(np.cos(2 * np.pi * z2))))
    return y.astype(float)

def F4(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)
    x0 = [6.5706, -4.7415, 99.8101, -69.8675, 46.3398, -94.7804, -14.1227, -22.2035, 63.0211, -96.1546]

    z1 = X-x0
    z2 = np.dot(z1, M)
    z2 = z2/20
    D = 10
    fit = 0
    z2=np.reshape(z2, (1, D))
    for i in range(1, D+1):
        fit = fit + i * (z2[0, i-1]**2)

    y = fit
    # e = np.exp(1)
    # z = z2**2
    # y = (20+e-20*np.exp(-0.2*np.sqrt((1/D)*np.sum(z,axis=1)))-np.exp((1/D)*np.sum(np.cos(2*np.pi*z2),axis=1)))/20
    return y.astype(float)

def F5(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [84.9982, 65.1519, -12.0721, -10.4880, 2.4412, -86.8010, -32.6663, -39.7689, 39.6034, 52.0954]

    z1 = X-x0
    z2 = np.dot(z1, M)
    z2 = z2*6

    D = 10
    z2 = np.reshape(z2, (1, D))
    # term1 = np.sum(z2**2,axis=1)/4000
    term1 = np.sum(z2 ** 2) / 4000
    term2 = 1
    for i in range(1, D+1):
        term2 = term2 * np.cos(z2[0, i-1]/np.sqrt(i))
    y = (term1 - term2 + 1)
    return y.astype(float)

def F6(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [7.7624, -51.0984, -95.5110, -68.7425, 8.7344, 0.0577, -36.7734, 44.3837, 99.8131, -12.1793]

    z1 = X-x0
    z2 = np.dot(z1, M)

    z = z2**2
    y = z.sum()
    return y.astype(float)

def F7(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [0.5876, -84.9703, -97.8543, 39.7223, 28.3686, 61.1286, 38.9558, -77.1346, 50.6776, 14.4813]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 20
    cos_z2 = np.cos(2 * np.pi * z2)
    z = z2 ** 2
    # y = np.sum(z - 10 * cos_z2 + 10, axis=1)
    y = np.sum(z - 10 * cos_z2 + 10)
    return y.astype(float)

def F8(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [5.3830, 0.1560, 47.8659, -17.0994, -32.5756, -29.2208, -32.7262, -43.5349, 1.9141, -36.7252]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 3
    D = 10
    e = np.exp(1)
    z = z2 ** 2
    z2 = np.reshape(z2, (1, D))
    y = (20 + e - 20 * np.exp(-0.2 * np.sqrt((1 / D) * np.sum(z))) - np.exp((1 / D) * np.sum(np.cos(2 * np.pi * z2))))
    return y.astype(float)

def F9(X):

    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [6.5706, -4.7415, 99.8101, -69.8675, 46.3398, -94.7804, -14.1227, -22.2035, 63.0211, -96.1546]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 20
    D = 10
    fit = 0
    z2 = np.reshape(z2, (1, D))
    for i in range(1, D + 1):
        fit = fit + i * (z2[0, i - 1] ** 2)

    y = fit / 2500
    return y.astype(float)

def F10(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [84.9982, 65.1519, -12.0721, -10.4880, 2.4412, -86.8010, -32.6663, -39.7689, 39.6034, 52.0954]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 * 6
    D = 10
    z2 = np.reshape(z2, (1, D))
    term1 = np.sum(z2 ** 2) / 4000
    term2 = 1
    for i in range(1, D + 1):
        term2 = term2 * np.cos(z2[0, i - 1] / np.sqrt(i))
    y = (term1 - term2 + 1)
    return y.astype(float)

def F11(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [7.7624, -51.0984, -95.5110, -68.7425, 8.7344, 0.0577, -36.7734, 44.3837, 99.8131, -12.1793]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z = z2 ** 2
    y = z.sum()
    return y.astype(float)

def F12(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [0.5876, -84.9703, -97.8543, 39.7223, 28.3686, 61.1286, 38.9558, -77.1346, 50.6776, 14.4813]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 20
    cos_z2 = np.cos(2 * np.pi * z2)
    z = z2 ** 2

    y = np.sum(z - 10 * cos_z2 + 10)
    return y.astype(float)

def F13(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [5.3830, 0.1560, 47.8659, -17.0994, -32.5756, -29.2208, -32.7262, -43.5349, 1.9141, -36.7252]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 3
    D = 10
    e = np.exp(1)
    z = z2 ** 2
    y = (20 + e - 20 * np.exp(-0.2 * np.sqrt((1 / D) * np.sum(z))) - np.exp(
        (1 / D) * np.sum(np.cos(2 * np.pi * z2))))
    return y.astype(float)

def F14(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [6.5706, -4.7415, 99.8101, -69.8675, 46.3398, -94.7804, -14.1227, -22.2035, 63.0211, -96.1546]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 20
    D = 10
    fit = 0
    z2 = np.reshape(z2, (1, D))
    for i in range(1, D + 1):
        fit = fit + i * (z2[0, i - 1] ** 2)

    y = fit
    return y.astype(float)

def F15(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [84.9982, 65.1519, -12.0721, -10.4880, 2.4412, -86.8010, -32.6663, -39.7689, 39.6034, 52.0954]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 * 6
    D = 10
    z2 = np.reshape(z2, (1, D))
    term1 = np.sum(z2 ** 2) / 4000
    term2 = 1
    for i in range(1, D + 1):
        term2 = term2 * np.cos(z2[0, i - 1] / np.sqrt(i))
    y = (term1 - term2 + 1)
    return y.astype(float)

def F16(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [7.7624, -51.0984, -95.5110, -68.7425, 8.7344, 0.0577, -36.7734, 44.3837, 99.8131, -12.1793]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z = z2 ** 2
    y = z.sum()
    return y.astype(float)

def F17(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [0.5876, -84.9703, -97.8543, 39.7223, 28.3686, 61.1286, 38.9558, -77.1346, 50.6776, 14.4813]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 20
    cos_z2 = np.cos(2 * np.pi * z2)
    z = z2 ** 2
    y = np.sum(z - 10 * cos_z2 + 10)
    return y.astype(float)

def F18(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [5.3830, 0.1560, 47.8659, -17.0994, -32.5756, -29.2208, -32.7262, -43.5349, 1.9141, -36.7252]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 3
    D = 10
    e = np.exp(1)
    z = z2 ** 2
    y = (20 + e - 20 * np.exp(-0.2 * np.sqrt((1 / D) * np.sum(z))) - np.exp(
        (1 / D) * np.sum(np.cos(2 * np.pi * z2))))
    return y.astype(float)

def F19(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [6.5706, -4.7415, 99.8101, -69.8675, 46.3398, -94.7804, -14.1227, -22.2035, 63.0211, -96.1546]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 20
    D = 10
    fit = 0
    z2 = np.reshape(z2, (1, D))
    for i in range(1, D + 1):
        fit = fit + i * (z2[0, i - 1] ** 2)

    y = fit
    return y.astype(float)

def F20(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [84.9982, 65.1519, -12.0721, -10.4880, 2.4412, -86.8010, -32.6663, -39.7689, 39.6034, 52.0954]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 * 6
    D = 10
    z2 = np.reshape(z2, (1, D))
    term1 = np.sum(z2 ** 2) / 4000
    term2 = 1
    for i in range(1, D + 1):
        term2 = term2 * np.cos(z2[0, i - 1] / np.sqrt(i))
    y = (term1 - term2 + 1)
    return y.astype(float)

def F21(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [7.7624, -51.0984, -95.5110, -68.7425, 8.7344, 0.0577, -36.7734, 44.3837, 99.8131, -12.1793]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z = z2 ** 2
    y = z.sum()
    return y.astype(float)

def F22(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [0.5876, -84.9703, -97.8543, 39.7223, 28.3686, 61.1286, 38.9558, -77.1346, 50.6776, 14.4813]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 20
    cos_z2 = np.cos(2 * np.pi * z2)
    z = z2 ** 2
    y = np.sum(z - 10 * cos_z2 + 10)
    return y.astype(float)

def F23(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)
    x0 = [5.3830, 0.1560, 47.8659, -17.0994, -32.5756, -29.2208, -32.7262, -43.5349, 1.9141, -36.7252]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 3
    D = 10
    e = np.exp(1)
    z = z2 ** 2
    y = (20 + e - 20 * np.exp(-0.2 * np.sqrt((1 / D) * np.sum(z))) - np.exp(
        (1 / D) * np.sum(np.cos(2 * np.pi * z2))))
    return y.astype(float)

def F24(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [6.5706, -4.7415, 99.8101, -69.8675, 46.3398, -94.7804, -14.1227, -22.2035, 63.0211, -96.1546]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 20
    D = 10
    z2 = np.reshape(z2, (1, D))
    fit = 0
    for i in range(1, D + 1):
        fit = fit + i * (z2[0, i - 1] ** 2)

    y = fit
    return y.astype(float)

def F25(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [84.9982, 65.1519, -12.0721, -10.4880, 2.4412, -86.8010, -32.6663, -39.7689, 39.6034, 52.0954]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 * 6
    D = 10
    z2 = np.reshape(z2, (1, D))
    term1 = np.sum(z2 ** 2) / 4000
    term2 = 1
    for i in range(1, D + 1):
        term2 = term2 * np.cos(z2[0, i - 1] / np.sqrt(i))
    y = (term1 - term2 + 1)
    return y.astype(float)

def F26(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [7.7624, -51.0984, -95.5110, -68.7425, 8.7344, 0.0577, -36.7734, 44.3837, 99.8131, -12.1793]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z = z2 ** 2
    y = z.sum()
    return y.astype(float)

def F27(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [0.5876, -84.9703, -97.8543, 39.7223, 28.3686, 61.1286, 38.9558, -77.1346, 50.6776, 14.4813]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 20
    cos_z2 = np.cos(2 * np.pi * z2)
    z = z2 ** 2
    y = np.sum(z - 10 * cos_z2 + 10)
    return y.astype(float)

def F28(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [5.3830, 0.1560, 47.8659, -17.0994, -32.5756, -29.2208, -32.7262, -43.5349, 1.9141, -36.7252]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 3
    D = 10
    e = np.exp(1)
    z = z2 ** 2
    y = (20 + e - 20 * np.exp(-0.2 * np.sqrt((1 / D) * np.sum(z))) - np.exp(
        (1 / D) * np.sum(np.cos(2 * np.pi * z2))))
    return y.astype(float)

def F29(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [6.5706, -4.7415, 99.8101, -69.8675, 46.3398, -94.7804, -14.1227, -22.2035, 63.0211, -96.1546]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 / 20
    D = 10
    fit = 0
    z2 = np.reshape(z2, (1, D))
    for i in range(1, D + 1):
        fit = fit + i * (z2[0, i - 1] ** 2)

    y = fit
    return y.astype(float)

def F30(X):
    M = np.loadtxt("Benchmarks/shift_data/data_elliptic_M_D10" '.txt').reshape(10, 10)

    x0 = [84.9982, 65.1519, -12.0721, -10.4880, 2.4412, -86.8010, -32.6663, -39.7689, 39.6034, 52.0954]

    z1 = X - x0
    z2 = np.dot(z1, M)
    z2 = z2 * 6
    D = 10
    z2 = np.reshape(z2, (1, D))
    term1 = np.sum(z2 ** 2) / 4000
    term2 = 1
    for i in range(1, D + 1):
        term2 = term2 * np.cos(z2[0, i - 1] / np.sqrt(i))
    y = (term1 - term2 + 1)
    return y.astype(float)