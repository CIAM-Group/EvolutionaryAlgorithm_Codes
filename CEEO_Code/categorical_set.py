
import numpy as np
import Benchmarks.syntheticFunctions
from Application.ParamOP import TPAlexNet

def my_categorical_set(obj_func, dim):
    bounds = []
    categories =[]
    if obj_func == 'F1':
        f = Benchmarks.syntheticFunctions.F1
        v1 = np.array((99.8131, 38.7794, 97.4385, 66.3214, 83.6572))
        v2 = np.array((-12.1793, -81.4490, 94.5925, -20.7460, -23.4447))
        v = np.array((v1, v2))
        lj = [len(v1), len(v2)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (v[i])})
        for i in range(len(v), dim):
            bounds.append({'name': f"x{i-len(v)+1}", 'type': 'continuous', 'domain': (-100, 100)})


    elif obj_func == 'F2':
        f = Benchmarks.syntheticFunctions.F2
        v1 = np.array((50.6776, -39.6234, -61.7100, 97.7223, 63.1775))
        v2 = np.array((14.4813, -97.4609, 92.2885, -3.8172, 83.2134))
        v = np.array((v1, v2))
        lj = [len(v1), len(v2)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (v[i])})
        for i in range(len(v), dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})


    elif obj_func == 'F3':
        f = Benchmarks.syntheticFunctions.F3
        v1 = [1.9141, -12.6618, -3.5678, -18.1508, -7.8900]
        v2 = [-36.7252, 27.8390, -53.1350, -21.6579, -27.2089]
        v = np.array((v1, v2))
        lj = [len(v1), len(v2)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (v[i])})
        for i in range(len(v), dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F4':
        f = Benchmarks.syntheticFunctions.F4
        v1 = [63.0211, 15.4585, -0.9510, 90.1246, 18.4635]
        v2 = [-96.1546, -3.5673, -59.5396, 13.2944, -21.4157]
        v = np.array((v1, v2))
        lj = [len(v1), len(v2)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (v[i])})
        for i in range(len(v), dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F5':
        f = Benchmarks.syntheticFunctions.F5
        v1 = [39.6034, -98.0900, 66.9081, 5.6974, -52.6892]
        v2 = [52.0954, -95.0943, 60.2757, -59.7487, -89.1344]
        v = np.array((v1, v2))
        lj = [len(v1), len(v2)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (v[i])})
        for i in range(len(v), dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F6':
        f = Benchmarks.syntheticFunctions.F6
        v1 = [99.8131, 38.7794, 97.4385, 66.3214, 83.6572, 64.3900, 6.2714, 4.7893, 42.9978, -46.2021]
        v2 = [-12.1793, -81.4490, 94.5925, -20.7460, -23.4447, -37.0443, -33.7724, -78.8025, 69.8750, 70.8563]
        v = np.array((v1, v2))
        lj = [len(v1), len(v2)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (v[i])})
        for i in range(len(v), dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F7':
        f = Benchmarks.syntheticFunctions.F7
        v1 = [50.6776, -39.6234, -61.7100, 97.7223, 63.1775, -12.0348, -21.6271, -12.3744, 67.1491, -19.0775]
        v2 = [14.4813, -97.4609, 92.2885, -3.8172, 83.2134, -89.4358, 10.1637, -86.6364, -64.1289, 6.0189]
        v = np.array((v1, v2))
        lj = [len(v1), len(v2)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (v[i])})
        for i in range(len(v), dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F8':
        f = Benchmarks.syntheticFunctions.F8
        v1 = [1.9141, -12.6618, -3.5678, -18.1508, -7.8900, 1.7955, -45.1022, -14.7915, -47.5095, 57.2121]
        v2 = [-36.7252, 27.8390, -53.1350, -21.6579, -27.2089, -58.0376, 19.1243, 2.8412, -17.4512, -58.3012]
        v = np.array((v1, v2))
        lj = [len(v1), len(v2)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (v[i])})
        for i in range(len(v), dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F9':
        f = Benchmarks.syntheticFunctions.F9
        v1 = [63.0211, 15.4585, -0.9510, 90.1246, 18.4635, -17.3490, 96.5306, -14.2523, -37.9036, 58.6272]
        v2 = [-96.1546, -3.5673, -59.5396, 13.2944, -21.4157, 25.7777, 0.5632, 73.3501, -29.0539, -79.8143]
        v = np.array((v1, v2))
        lj = [len(v1), len(v2)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (v[i])})
        for i in range(len(v), dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F10':
        f = Benchmarks.syntheticFunctions.F10
        v1 = [39.6034, -98.0900, 66.9081, 5.6974, -52.6892, -22.8678, -21.4237, -70.5337, 8.6142, -89.3348]
        v2 = [52.0954, -95.0943, 60.2757, -59.7487, -89.1344, 70.3986, -55.3637, 17.6185, -72.3865, -10.6520]
        v = np.array((v1, v2))
        lj = [len(v1), len(v2)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (v[i])})
        for i in range(len(v), dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F11':
        f = Benchmarks.syntheticFunctions.F11
        v1 = [-95.5110, 10.9166, -86.3500, 6.3552, -52.8390]
        v2 = [-68.7425, 2.4009, -26.8628, 52.9171, -94.4758]
        v3 = [8.7344, 2.0220, 1.2974, -37.0691, -79.2651]
        v4 = [0.0577, -66.8891, -24.5506, -96.2061, 45.4579]
        v5 = [-36.7734, 11.1348, 40.9187, -32.3377, 62.3757]
        v6 = [44.3837, -84.2635, -31.8857, -99.0299, 23.2041]
        v7 = [99.8131, 38.7794, 97.4385, 66.3214, 83.6572]
        v8 = [-12.1793, -81.4490, 94.5925, -20.7460, -23.4447]
        v = np.array((v1, v2, v3, v4,
                      v5, v6, v7, v8))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5), len(v6), len(v7), len(v8)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F12':
        f = Benchmarks.syntheticFunctions.F12
        v1 = [-97.8543, -98.8581, -93.8085, -78.8370, 81.9188]
        v2 = [39.7223, -99.8416, -4.6454, 74.7200, -80.8983]
        v3 = [28.3686, -19.5009, -96.7178, 9.0181, 58.1322]
        v4 = [61.1286, 4.1286, -3.9445, -15.1705, -7.9428]
        v5 = [38.9558, 37.3101, 83.0975, -98.6905, -75.3426]
        v6 = [-77.1346, -2.0340, 70.8802, 51.3176, -24.3460]
        v7 = [50.6776, -39.6234, -61.7100, 97.7223, 63.1775]
        v8 = [14.4813, -97.4609, 92.2885, -3.8172, 83.2134]
        v = np.array((v1, v2, v3, v4,
                      v5, v6, v7, v8))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5), len(v6), len(v7), len(v8)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F13':
        f = Benchmarks.syntheticFunctions.F13
        v1 = [47.8659, -50.2789, -51.4218, -5.7807, 59.7290]
        v2 = [-17.0994, 17.6311, -52.2380, -37.5205, -50.8626]
        v3 = [-32.5756, 27.7492, -33.1525, 55.2097, -38.2367]
        v4 = [-29.2208, -14.6371, 31.1216, -14.0404, 23.6011]
        v5 = [-32.7262, 53.3853, -56.2406, 51.0570, 21.1575]
        v6 = [-43.5349, -59.4140, -49.4245, -9.3890, -56.9489]
        v7 = [1.9141, -12.6618, -3.5678, -18.1508, -7.8900]
        v8 = [-36.7252, 27.8390, -53.1350, -21.6579, -27.2089]
        v = np.array((v1, v2, v3, v4,
                      v5, v6, v7, v8))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5), len(v6), len(v7), len(v8)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F14':
        f = Benchmarks.syntheticFunctions.F14
        v1 = [99.8101, -31.6099, 89.6818, 56.8515, -88.4346]
        v2 = [-69.8675, 40.6365, -76.1113, 65.0137, -93.6473]
        v3 = [46.3398, 57.3869, -59.6658, 54.2175, -66.4293]
        v4 = [-94.7804, 90.0091, -12.3052, 27.1707, 89.5608]
        v5 = [-14.1227, 70.3685, -3.5821, -57.3306, -21.0553]
        v6 = [-22.2035, -94.6947, -28.3114, 79.0958, -32.9711]
        v7 = [63.0211, 15.4585, -0.9510, 90.1246, 18.4635]
        v8 = [-96.1546, -3.5673, -59.5396, 13.2944, -21.4157]
        v = np.array((v1, v2, v3, v4,
                      v5, v6, v7, v8))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5), len(v6), len(v7), len(v8)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F15':
        f = Benchmarks.syntheticFunctions.F15
        v1 = [-12.0721, 2.9979, -19.0989, -67.9707, -5.3256]
        v2 = [-10.4880, 49.2424, 64.1867, 5.7290, -95.5992]
        v3 = [2.4412, 63.1647, -11.6669, -31.9233, -87.5237]
        v4 = [-86.8010, 58.9903, -71.2887, 55.7150, 59.1220]
        v5 = [-32.6664, 14.3942, 19.6051, 23.8658, 92.7302]
        v6 = [-39.7689, 51.2260, 95.1572, -52.9366, 81.0941]
        v7 = [39.6034, -98.0900, 66.9081, 5.6974, -52.6892]
        v8 = [52.0954, -95.0943, 60.2757, -59.7487, -89.1344]
        v = np.array((v1, v2, v3, v4,
                      v5, v6, v7, v8))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5), len(v6), len(v7), len(v8)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F16':
        f = Benchmarks.syntheticFunctions.F16
        v1 = [-95.5110, 10.9166, -86.3500, 6.3552, -52.8390, 30.5276, 77.9978, -14.5499, -53.7453, 93.4961]
        v2 = [-68.7425, 2.4009, -26.8628, 52.9171, -94.4758, -19.8521, 18.5924, 16.7370, -83.7091, -33.1471]
        v3 = [8.7344, 2.0220, 1.2974, -37.0691, -79.2651, -13.4857, 91.8744, 41.5887, 54.6449, -53.6206]
        v4 = [0.0577, -66.8891, -24.5506, -96.2061, 45.4579, 18.1319, 58.3241, 71.9285, -75.8105, -22.9862]
        v5 = [-36.7734, 11.1348, 40.9187, -32.3377, 62.3757, 24.4644, 86.2232, 90.6468, -99.4558, 89.3221]
        v6 = [44.3837, -84.2635, -31.8857, -99.0299, 23.2041, 13.1996, -43.5760, 26.1334, -6.6750, -22.8134]
        v7 = [99.8131, 38.7794, 97.4385, 66.3214, 83.6572, 64.3900, 6.2714, 4.7893, 42.9978, -46.2021]
        v8 = [-12.1793, -81.4490, 94.5925, -20.7460, -23.4447, -37.0443, -33.7724, -78.8025, 69.8750, 70.8563]
        v = np.array((v1, v2, v3, v4,
                      v5, v6, v7, v8))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5), len(v6), len(v7), len(v8)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F17':
        f = Benchmarks.syntheticFunctions.F17
        v1 = [-97.8543, -98.8581, -93.8085, -78.8370, 81.9188, -2.9181, -50.9363, 31.9732, 69.0271, 85.5965]
        v2 = [39.7223, -99.8416, -4.6454, 74.7200, -80.8983, -54.2256, 73.2056, -29.1147, -11.7113, 16.2659]
        v3 = [28.3686, -19.5009, -96.7178, 9.0181, 58.1322, -8.9950, 99.3704, 28.2749, 60.8476, -53.6360]
        v4 = [61.1286, 4.1286, -3.9445, -15.1705, -7.9428, -51.8438, 76.1710, -37.0110, -34.0411, -61.8862]
        v5 = [38.9558, 37.3101, 83.0975, -98.6905, -75.3426, 93.3490, 52.6871, -77.6949, 3.4488, -14.2671]
        v6 = [-77.1346, -2.0340, 70.8802, 51.3176, -24.3460, 63.8007, 93.8858, 11.8351, 57.5630, -0.9117]
        v7 = [50.6776, -39.6234, -61.7100, 97.7223, 63.1775, -12.0348, -21.6271, -12.3744, 67.1491, -19.0775]
        v8 = [14.4813, -97.4609, 92.2885, -3.8172, 83.2134, -89.4358, 10.1637, -86.6364, -64.1289, 6.0189]
        v = np.array((v1, v2, v3, v4,
                      v5, v6, v7, v8))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5), len(v6), len(v7), len(v8)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F18':
        f = Benchmarks.syntheticFunctions.F18
        v1 = [47.8659, -50.2789, -51.4218, -5.7807, 59.7290, -16.4921, 4.6304, -51.4052, -56.5858, -1.4768]
        v2 = [-17.0994, 17.6311, -52.2380, -37.5205, -50.8626, -18.6013, -3.3562, -46.1564, 23.0041, -24.2366]
        v3 = [-32.5756, 27.7492, -33.1525, 55.2097, -38.2367, -34.8929, 54.6377, -45.0192, 26.5879, -53.1159]
        v4 = [-29.2208, -14.6371, 31.1216, -14.0404, 23.6011, -27.5998, 50.6179, 26.2418, 43.5885, 15.1259]
        v5 = [-32.7262, 53.3853, -56.2406, 51.0570, 21.1575, 20.4656, -28.2398, -13.7042, -18.0062, 10.0906]
        v6 = [-43.5349, -59.4140, -49.4245, -9.3890, -56.9489, -50.0486, -53.9074, -58.2566, 17.3949, -27.1704]
        v7 = [1.9141, -12.6618, -3.5678, -18.1508, -7.8900, 1.7955, -45.1022, -14.7915, -47.5095, -57.2121]
        v8 = [-36.7252, 27.8390, -53.1350, -21.6579, -27.2089, -58.0376, 19.1243, 2.8412, -17.4512, -58.3012]
        v = np.array((v1, v2, v3, v4,
                      v5, v6, v7, v8))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5), len(v6), len(v7), len(v8)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F19':
        f = Benchmarks.syntheticFunctions.F19
        v1 = [99.8101, -31.6099, 89.6818, 56.8515, -88.4346, -57.0659, -31.5381, -49.4641, 25.9274, 9.5564]
        v2 = [-69.8675, 40.6365, -76.1113, 65.0137, -93.6473, 92.6166, 80.1439, 76.2718, 26.7529, 37.0511]
        v3 = [46.3398, 57.3869, -59.6658, 54.2175, -66.4293, 23.2850, 8.9172, 5.8984, -81.7778, -29.9939]
        v4 = [-94.7804, 90.0091, -12.3052, 27.1707, 89.5608, 23.1004, -82.2399, 22.3617, 87.6216, -60.2491]
        v5 = [-14.1227, 70.3685, -3.5821, -57.3306, -21.0553, 22.6570, -8.0322, 66.9846, 22.4542, -21.2894]
        v6 = [-22.2035, -94.6947, -28.3114, 79.0958, -32.9711, -68.5177, -37.1964, 49.1284, -50.3006, 31.9762]
        v7 = [63.0211, 15.4585, -0.9510, 90.1246, 18.4635, -17.3490, 96.5306, -14.2523, -37.9036, 58.6272]
        v8 = [-96.1546, -3.5673, -59.5396, 13.2944, -21.4157, 25.7777, 0.5632, 73.3501, -29.0539, -79.8143]
        v = np.array((v1, v2, v3, v4,
                      v5, v6, v7, v8))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5), len(v6), len(v7), len(v8)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F20':
        f = Benchmarks.syntheticFunctions.F20
        v1 = [-12.0721, 2.9979, -19.0989, -67.9707, -5.3256, 41.2393, 88.4943, -89.4662, 12.4275, 53.2186]
        v2 = [-10.4880, 49.2424, 64.1867, 5.7290, -95.5992, 66.8645, 56.9595, -27.3189, 77.8113, -53.0569]
        v3 = [2.4412, 63.1647, -11.6669, -31.9233, -87.5237, 48.4239, -75.0023, 49.5995, -83.9520, -81.1888]
        v4 = [-86.8010, 58.9903, -71.2887, 55.7150, 59.1220, 37.2548, 75.7530, -10.7222, -1.7561, 97.9166]
        v5 = [-32.6664, 14.3942, 19.6051, 23.8658, 92.7302, 0.4261, 19.6791, 60.4852, -39.3893, -35.6968]
        v6 = [-39.7689, 51.2260, 95.1572, -52.9366, 81.0941, -67.8047, -13.8984, 74.2628, 41.1879, 53.5652]
        v7 = [39.6034, -98.0900, 66.9081, 5.6974, -52.6892, -22.8678, -21.4237, -70.5337, 8.6142, -89.3348]
        v8 = [52.0954, -95.0943, 60.2757, -59.7487, -89.1344, 70.3986, -55.3637, 17.6185, -72.3865, -10.6520]
        v = np.array((v1, v2, v3, v4,
                      v5, v6, v7, v8))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5), len(v6), len(v7), len(v8)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F21':
        f = Benchmarks.syntheticFunctions.F21
        v1 = [0.0577, -66.8891, -24.5506, -96.2061, 45.4579]
        v2 = [-36.7734, 11.1348, 40.9187, -32.3377, 62.3757]
        v3 = [44.3837, -84.2635, -31.8857, -99.0299, 23.2041]
        v4 = [99.8131, 38.7794, 97.4385, 66.3214, 83.6572]
        v5 = [-12.1793, -81.4490, 94.5925, -20.7460, -23.4447]
        v = np.array((v1, v2, v3, v4, v5))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F22':
        f = Benchmarks.syntheticFunctions.F22
        v1 = [61.1286, 4.1286, -3.9445, -15.1705, -7.9428]
        v2 = [38.9558, 37.3101, 83.0975, -98.6905, -75.3426]
        v3 = [-77.1346, -2.0340, 70.8802, 51.3176, -24.3460]
        v4 = [50.6776, -39.6234, -61.7100, 97.7223, 63.1775]
        v5 = [14.4813, -97.4609, 92.2885, -3.8172, 83.2134]
        v = np.array((v1, v2, v3, v4, v5))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F23':
        f = Benchmarks.syntheticFunctions.F23
        v1 = [-29.2208, -14.6371, 31.1216, -14.0404, 23.6011]
        v2 = [-32.7262, 53.3853, -56.2406, 51.0570, 21.1575]
        v3 = [-43.5349, -59.4140, -49.4245, -9.3890, -56.9489]
        v4 = [1.9141, -12.6618, -3.5678, -18.1508, -7.8900]
        v5 = [-36.7252, 27.8390, -53.1350, -21.6579, -27.2089]
        v = np.array((v1, v2, v3, v4, v5))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F24':
        f = Benchmarks.syntheticFunctions.F24
        v1 = [-94.7804, 90.0091, -12.3052, 27.1707, 89.5608]
        v2 = [-14.1227, 70.3685, -3.5821, -57.3306, -21.0553]
        v3 = [-22.2035, -94.6947, -28.3114, 79.0958, -32.9711]
        v4 = [63.0211, 15.4585, -0.9510, 90.1246, 18.4635]
        v5 = [-96.1546, -3.5673, -59.5396, 13.2944, -21.4157]
        v = np.array((v1, v2, v3, v4, v5))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F25':
        f = Benchmarks.syntheticFunctions.F25
        v1 = [-86.8010, 58.9903, -71.2887, 55.7150, 59.1220]
        v2 = [-32.6664, 14.3942, 19.6051, 23.8658, 92.7302]
        v3 = [-39.7689, 51.2260, 95.1572, -52.9366, 81.0941]
        v4 = [39.6034, -98.0900, 66.9081, 5.6974, -52.6892]
        v5 = [52.0954, -95.0943, 60.2757, -59.7487, -89.1344]
        v = np.array((v1, v2, v3, v4, v5))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F26':
        f = Benchmarks.syntheticFunctions.F26
        v1 = [0.0577, -66.8891, -24.5506, -96.2061, 45.4579, 18.1319, 58.3241, 71.9285, -75.8105, -22.9862]
        v2 = [-36.7734, 11.1348, 40.9187, -32.3377, 62.3757, 24.4644, 86.2232, 90.6468, -99.4558, 89.3221]
        v3 = [44.3837, -84.2635, -31.8857, -99.0299, 23.2041, 13.1996, -43.5760, 26.1334, -6.6750, -22.8134]
        v4 = [99.8131, 38.7794, 97.4385, 66.3214, 83.6572, 64.3900, 6.2714, 4.7893, 42.9978, -46.2021]
        v5 = [-12.1793, -81.4490, 94.5925, -20.7460, -23.4447, -37.0443, -33.7724, -78.8025, 69.8750, 70.8563]
        v = np.array((v1, v2, v3, v4, v5))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F27':
        f = Benchmarks.syntheticFunctions.F27
        v1 = [61.1286, 4.1286, -3.9445, -15.1705, -7.9428, -51.8438, 76.1710, -37.0110, -34.0411, -61.8862]
        v2 = [38.9558, 37.3101, 83.0975, -98.6905, -75.3426, 93.3490, 52.6871, -77.6949, 3.4488, -14.2671]
        v3 = [-77.1346, -2.0340, 70.8802, 51.3176, -24.3460, 63.8007, 93.8858, 11.8351, 57.5630, -0.9117]
        v4 = [50.6776, -39.6234, -61.7100, 97.7223, 63.1775, -12.0348, -21.6271, -12.3744, 67.1491, -19.0775]
        v5 = [14.4813, -97.4609, 92.2885, -3.8172, 83.2134, -89.4358, 10.1637, -86.6364, -64.1289, 6.0189]
        v = np.array((v1, v2, v3, v4, v5))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F28':
        f = Benchmarks.syntheticFunctions.F28
        v1 = [-29.2208, -14.6371, 31.1216, -14.0404, 23.6011, -27.5998, 50.6179, 26.2418, 43.5885, 15.1259]
        v2 = [-32.7262, 53.3853, -56.2406, 51.0570, 21.1575, 20.4656, -28.2398, -13.7042, -18.0062, 10.0906]
        v3 = [-43.5349, -59.4140, -49.4245, -9.3890, -56.9489, -50.0486, -53.9074, -58.2566, 17.3949, -27.1704]
        v4 = [1.9141, -12.6618, -3.5678, -18.1508, -7.8900, 1.7955, -45.1022, -14.7915, -47.5095, -57.2121]
        v5 = [-36.7252, 27.8390, -53.1350, -21.6579, -27.2089, -58.0376, 19.1243, 2.8412, -17.4512, -58.3012]
        v = np.array((v1, v2, v3, v4, v5))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F29':
        f = Benchmarks.syntheticFunctions.F29
        v1 = [-94.7804, 90.0091, -12.3052, 27.1707, 89.5608, 23.1004, -82.2399, 22.3617, 87.6216, -60.2491]
        v2 = [-14.1227, 70.3685, -3.5821, -57.3306, -21.0553, 22.6570, -8.0322, 66.9846, 22.4542, -21.2894]
        v3 = [-22.2035, -94.6947, -28.3114, 79.0958, -32.9711, -68.5177, -37.1964, 49.1284, -50.3006, 31.9762]
        v4 = [63.0211, 15.4585, -0.9510, 90.1246, 18.4635, -17.3490, 96.5306, -14.2523, -37.9036, 58.6272]
        v5 = [-96.1546, -3.5673, -59.5396, 13.2944, -21.4157, 25.7777, 0.5632, 73.3501, -29.0539, -79.8143]
        v = np.array((v1, v2, v3, v4, v5))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'F30':
        f = Benchmarks.syntheticFunctions.F30
        v1 = [-86.8010, 58.9903, -71.2887, 55.7150, 59.1220, 37.2548, 75.7530, -10.7222, -1.7561, 97.9166]
        v2 = [-32.6664, 14.3942, 19.6051, 23.8658, 92.7302, 0.4261, 19.6791, 60.4852, -39.3893, -35.6968]
        v3 = [-39.7689, 51.2260, 95.1572, -52.9366, 81.0941, -67.8047, -13.8984, 74.2628, 41.1879, 53.5652]
        v4 = [39.6034, -98.0900, 66.9081, 5.6974, -52.6892, -22.8678, -21.4237, -70.5337, 8.6142, -89.3348]
        v5 = [52.0954, -95.0943, 60.2757, -59.7487, -89.1344, 70.3986, -55.3637, 17.6185, -72.3865, -10.6520]
        v = np.array((v1, v2, v3, v4, v5))
        lj = [len(v1), len(v2), len(v3), len(v4), len(v5)]
        for i in range(len(v)):
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (range(lj[i]))})
        for i in range(len(v), 1, dim):
            bounds.append({'name': f"x{i - len(v) + 1}", 'type': 'continuous', 'domain': (-100, 100)})

    elif obj_func == 'TPAlexNet':
        dim = 22
        problem = TPAlexNet(10)
        f = problem.F
        N_lst = problem.N_lst
        lj = N_lst
        v = N_lst
        for i in range(len(N_lst)):
            a = np.arange(0, N_lst[i], 1)
            bounds.append({'name': f"h{i}", 'type': 'categorical', 'domain': (a)})
        for i in range(len(N_lst), dim):
            if i <= (len(N_lst) + 6):
                bounds.append({'name': f"x{i - len(N_lst) + 1}", 'type': 'continuous', 'domain': (32, 512)})
            else:
                bounds.append({'name': f"x{i - len(N_lst) + 1}", 'type': 'continuous', 'domain': (0.1, 0.9)})

    return f, v, lj, bounds