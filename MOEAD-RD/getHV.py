import json
import os
import numpy as np
from utils import getHV_utils as Utils


def work(input_dir, all_outputs_dir, cluster_files=None):
    # 获得所有算法的 所有文件 上的 f1f2
    many_all_f1f2s = Utils.get_allOutputs_f1_f2(input_dir, all_outputs_dir)
    # 获得(非支配且)归一化后的f1f2
    algorithms_nondomain_nomalized_f1f2, \
    all_nondomain_f1f2, \
    F1F2s = Utils.get_nomalized_nondomain_f1f2_and_F1F2(many_all_f1f2s)
    # # 获得归一化的f1 f2
    all_all_nomalized_f1f2s = Utils.get_allOutputs_nomalized_f1f2(many_all_f1f2s, F1F2s)
    # 获得HV值
    all_Hvs_sum, all_Hvs = Utils.get_allOutputs_Hvs(all_all_nomalized_f1f2s)

    if cluster_files is not None:
        file_names = list(all_all_nomalized_f1f2s[list(all_all_nomalized_f1f2s.keys())[0]].keys())
        cluster_HVs = {cluster_name: {} for cluster_name in cluster_files}
        for cluster_name, instances in cluster_files.items():
            print(cluster_name, len(instances))
            for algorithm, hvs in all_Hvs.items():
                # mean
                # total_hv = np.mean([hvs[file_names.index(instance)] for instance in instances])
                total_hv = [hvs[file_names.index(instance)] for instance in instances]
                cluster_HVs[cluster_name][algorithm] = total_hv
        return cluster_HVs

    all_Hvs_sum = dict(sorted(all_Hvs_sum.items()))
    for name in all_Hvs_sum:
        print(name, all_Hvs_sum[name])

    # all_Hvs = dict(sorted(all_Hvs.items()))
    # for name in all_Hvs:
    #     print(name, all_Hvs[name])


if __name__ == '__main__':
    work("./all_data/inputs250", "./all_data/outputs250")
