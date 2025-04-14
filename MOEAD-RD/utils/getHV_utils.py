import os
import json

import numpy as np
from pymoo.visualization.scatter import Scatter
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider


def readFile(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        message_str = f.read()
    return json.loads(message_str)


def getSum(a):
    """
    :param a:
    :return: 计算累计个数
    """
    ans = []
    for i, x in enumerate(a):
        if i == 0:
            ans.append(x)
        else:
            ans.append(ans[i - 1] + x)
    return [i * 100 / sum(a) for i in ans]


def getY(data, x):
    """
    :param data:
    :param x:
    :return: 计算data中对应x轴的个个数，画频率直方图的
    """
    y = [0 for _ in x]
    for dat in data:
        for i in range(len(x)):
            if i == 0:
                continue
            if x[i - 1] < dat <= x[i]:
                y[i] += 1
                break
    return y


def get_allInstance_f1f2(all_distanceMap, all_truckTypeMap, all_solutions):
    # 获得一个算法输出的所有文件的f1f2
    """
    :param all_distanceMap: {"orderCode":distanceMap}
    :param all_soulutions: {"orderCode": [solutionArray], ...}
    :return: all_f1f2s :{"orderCode":f1f2s}
    """

    def calculate(distanceMap, truckTypeMap, vehicles, file_name):
        def getloadingRate(vehicle):
            fenzi1 = sum([spu["length"] * spu["width"] * spu["height"] for spu in vehicle["spuArray"]])
            fenzi2 = sum([spu["weight"] for spu in vehicle["spuArray"]])
            fenmu1 = truckTypeMap[vehicle["truckTypeId"]]["length"] * \
                     truckTypeMap[vehicle["truckTypeId"]]["width"] * \
                     truckTypeMap[vehicle["truckTypeId"]]["height"]
            fenmu2 = truckTypeMap[vehicle["truckTypeId"]]["maxLoad"]
            return max(fenzi1 / fenmu1, fenzi2 / fenmu2)

        def getDistance(platformList, distanceMap, vehicle, file_name):
            # platformList_new = []
            #
            # for spu in vehicle["spuArray"]:
            #     if len(platformList_new) == 0 or spu["platformCode"] != platformList_new[-1]:
            #         platformList_new.append(spu["platformCode"])

            ans = sum([distanceMap[platformList[i], platformList[i + 1]] for i in range(len(platformList) - 1)]) + \
                  distanceMap["start_point", platformList[0]] + distanceMap[platformList[-1], "end_point"]
            return ans

        loadingRateList = [getloadingRate(vehicle) for vehicle in vehicles]
        f1 = 1 - sum(loadingRateList) / len(loadingRateList)
        f2 = sum([getDistance(v["platformArray"], distanceMap, v, file_name) for v in vehicles])
        return [f1, f2]

    all_f1f2s = {
        file_name: [calculate(all_distanceMap[file_name], all_truckTypeMap[file_name], solution, file_name) for solution
                    in
                    all_solutions[file_name]]
        for file_name in all_solutions}
    return all_f1f2s


def get_allOutputs_f1_f2(input_dir, all_outputs_dir):
    # 获得所有算法output的所有instance的f1 f2值
    filename = os.path.join('all_f1f2s', 'many_all_f1f2s2.json')
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            pre_many_all_f1f2s = json.load(f)
    else:
        pre_many_all_f1f2s = {}
    many_all_f1f2s = {}
    outputs_dirs = os.listdir(all_outputs_dir)
    for x in outputs_dirs:
        if x.startswith('.'):
            continue
        if x in pre_many_all_f1f2s:
            many_all_f1f2s[x] = pre_many_all_f1f2s[x]
            continue
        outputs_dir = os.path.join(all_outputs_dir, x)
        check_finish = set(os.listdir(input_dir)) <= set(os.listdir(outputs_dir))
        if not check_finish:
            continue
        all_solutions = {}
        all_distanceMap = {}
        all_truckTypeMap = {}
        for file_name in os.listdir(input_dir):
            if file_name.startswith('.'):
                continue
            data = readFile(os.path.join(input_dir, file_name))
            rawdistanceMap = data["algorithmBaseParamDto"]["distanceMap"]
            all_truckTypeMap[file_name] = data["algorithmBaseParamDto"]["truckTypeMap"]
            all_distanceMap[file_name] = {(key.split('+')[0], key.split('+')[1]): rawdistanceMap[key] for key in
                                          rawdistanceMap}

            data = readFile(os.path.join(outputs_dir, file_name))
            all_solutions[file_name] = data["solutionArray"]

        many_all_f1f2s[outputs_dir.split(os.sep)[-1]] = get_allInstance_f1f2(all_distanceMap,
                                                                             all_truckTypeMap,
                                                                             all_solutions)

    # with open(filename, 'w') as f:
    #     json.dump(many_all_f1f2s, f)
    return many_all_f1f2s


def get_nomalized_nondomain_f1f2_and_F1F2(many_all_f1f2s):
    # 对每个 instance 获得 归一化的F1F2
    """
    :param many_all_f1f2s:{"name": {"order":[f1f2s], "order":[f1f2s], ...}, {"order":[f1f2s]}}
    :return: F1F2s: {"order": {"f1Mn":, "f1Mx": , }, "order":{} }
    """
    F1F2s = {}
    instance_names = [x for x in many_all_f1f2s[list(many_all_f1f2s.keys())[0]]]
    algorithms_nondomain_nomalized_f1f2 = {key: {instance: [] for instance in instance_names}
                                           for key in many_all_f1f2s}  # {"name": {"instance":[], }, }
    all_nondomain_f1f2 = {instance: [] for instance in instance_names}  # debug的时候关注下这个变量
    for instance in instance_names:
        nondomain_f1f2 = []
        all_f1f2 = []
        for algorithm in many_all_f1f2s:
            all_f1f2.extend([[f1f2s[0], f1f2s[1], algorithm] for f1f2s in many_all_f1f2s[algorithm][instance]])
        all_f1f2.sort(key=lambda x: (x[0], x[1]))
        for f1, f2, algorithm in all_f1f2:
            if len(nondomain_f1f2) == 0:
                nondomain_f1f2.append([f1, f2, algorithm])
                algorithms_nondomain_nomalized_f1f2[algorithm][instance].append([f1, f2])
                continue
            if nondomain_f1f2[-1][1] > f2:
                nondomain_f1f2.append([f1, f2, algorithm])
                algorithms_nondomain_nomalized_f1f2[algorithm][instance].append([f1, f2])

        F1F2s[instance] = {}
        F1F2s[instance]["f1Mn"] = min([f1 for f1, f2, algorithm in nondomain_f1f2])
        F1F2s[instance]["f1Mx"] = max([f1 for f1, f2, algorithm in nondomain_f1f2])
        F1F2s[instance]["f2Mn"] = min([f2 for f1, f2, algorithm in nondomain_f1f2])
        F1F2s[instance]["f2Mx"] = max([f2 for f1, f2, algorithm in nondomain_f1f2])
        if F1F2s[instance]["f1Mn"] == F1F2s[instance]["f1Mx"]:
            F1F2s[instance]["f1Mn"] = 0
        if F1F2s[instance]["f2Mn"] == F1F2s[instance]["f2Mx"]:
            F1F2s[instance]["f2Mn"] = 0

        all_nondomain_f1f2[instance] = nondomain_f1f2

        f1Mn, f2Mn = F1F2s[instance]["f1Mn"], F1F2s[instance]["f2Mn"]
        f1Gap, f2Gap = F1F2s[instance]["f1Mx"] - f1Mn, F1F2s[instance]["f2Mx"] - f2Mn
        # 归一化一下
        for algorithm in algorithms_nondomain_nomalized_f1f2:
            for f1f2 in algorithms_nondomain_nomalized_f1f2[algorithm][instance]:
                f1f2[0] = (f1f2[0] - f1Mn) / f1Gap
                f1f2[1] = (f1f2[1] - f2Mn) / f2Gap
    return algorithms_nondomain_nomalized_f1f2, all_nondomain_f1f2, F1F2s


def get_allOutputs_nomalized_f1f2(many_all_f1f2s, F1F2s):
    # 对many_all_f1f2s根据F1F2s归一化 # 这里的f1f2可能被其他算法的解支配了，但只要归一化之后在[1.2, 1.2]以内就可以
    all_all_nomalized_f1f2_listlist = {}
    for output_dir_name in many_all_f1f2s:
        all_f1f2s = many_all_f1f2s[output_dir_name]
        all_nomalized_f1f2_listlist = {}
        for file_name in all_f1f2s:
            f1f2 = all_f1f2s[file_name]
            f1Mn = 0 if F1F2s[file_name]["f1Mn"] == F1F2s[file_name]["f1Mx"] else F1F2s[file_name]["f1Mn"]
            f2Mn = 0 if F1F2s[file_name]["f2Mn"] == F1F2s[file_name]["f2Mx"] else F1F2s[file_name]["f2Mn"]
            f1Gap = F1F2s[file_name]["f1Mx"] - f1Mn
            f2Gap = F1F2s[file_name]["f2Mx"] - f2Mn
            nomalized_f1f2_listlist = [[(x[0] - f1Mn) / f1Gap, (x[1] - f2Mn) / f2Gap] for x in f1f2]
            nomalized_f1f2_listlist.sort(key=lambda f1f2_list: f1f2_list[0])
            all_nomalized_f1f2_listlist[file_name] = nomalized_f1f2_listlist
        all_all_nomalized_f1f2_listlist[output_dir_name] = all_nomalized_f1f2_listlist
    return all_all_nomalized_f1f2_listlist


def get_allOutputs_Hvs(all_all_nomalized_f1f2_listlist):
    all_Hvs_sum = {}
    all_Hvs = {}
    for output_dir in all_all_nomalized_f1f2_listlist:
        all_nomalized_f1f2s = all_all_nomalized_f1f2_listlist[output_dir]
        HVs = []
        for file_name in all_nomalized_f1f2s:
            nomalized_f1f2 = all_nomalized_f1f2s[file_name]
            nomalized_f1f2 = [[f1, f2] for f1, f2 in nomalized_f1f2 if f1 < 1.2 and f2 < 1.2]
            HV = 0
            for i in range(len(nomalized_f1f2)):
                if i == 0:
                    HV += (1.2 - nomalized_f1f2[0][0]) * (1.2 - nomalized_f1f2[0][1])
                else:
                    HV += (1.2 - nomalized_f1f2[i][0]) * \
                          (nomalized_f1f2[i - 1][1] - nomalized_f1f2[i][1])
            HVs.append(HV)
        all_Hvs_sum[output_dir] = sum(HVs)
        all_Hvs[output_dir] = HVs
    return all_Hvs_sum, all_Hvs


def printHV(input_dir, all_outputs_dir, logger=None):
    # 获得所有算法的 所有文件 上的 f1f2 # 画出当前算法
    many_all_f1f2s = get_allOutputs_f1_f2(input_dir, all_outputs_dir)
    # 获得(非支配且)归一化后的f1f2
    algorithms_nondomain_nomalized_f1f2, \
    all_nondomain_f1f2, \
    F1F2s = get_nomalized_nondomain_f1f2_and_F1F2(many_all_f1f2s)
    # 获得归一化的f1 f2
    all_all_nomalized_f1f2s = get_allOutputs_nomalized_f1f2(many_all_f1f2s, F1F2s)
    # 获得HV值
    all_Hvs_sum, all_Hvs = get_allOutputs_Hvs(all_all_nomalized_f1f2s)

    all_Hvs_sum = dict(sorted(all_Hvs_sum.items()))
    for name in all_Hvs_sum:
        if logger:
            logger.info(f'{name}, {all_Hvs_sum[name]}')
        else:
            print(f'{name}, {all_Hvs_sum[name]}')
    all_Hvs = dict(sorted(all_Hvs.items()))
    return F1F2s, all_nondomain_f1f2