import json
import os
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as offline
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.cluster import AgglomerativeClustering, DBSCAN, SpectralClustering

from getHV import work
from utils.data_utils import *


algorithm_list = [
    'MOEAD+DTR_gPBI',
    'MOEAD+AAWN',
    'MOEAD+AGR_all',
    # 'MOEAD+AGR_one',
    'winSilver_input250_eval2000',
    'winGold_input250_eval2000',
    'winBronze_input250_eval2000',
    # 'MOEAD_input250_final_noRSeed',
    # 'MOEAD+IGR_input250_final_noRSeed'
    # 'MOEAD',
    # 'MOEAD+GRA',
    # 'MOEAD+IGR',
    'MOEAD+IGR+GRA',
    # 'MOEAD+GRA_matchV_mean+sumT+deltaT8'
]


def get_al_name(file_name):
    algorithm = re.sub(r"_no\d+", "", file_name)
    return algorithm

def save_to_excel_2(cluster_HVs, file_name):
    latex_dict = {algorithm:[] for algorithm in algorithm_list}
    # 每一类算均值
    # 不要算均值了！
    with pd.ExcelWriter(file_name) as writer:
        for cluster_name in [1, 0, 2]:
            algorithm_Hvs = cluster_HVs[cluster_name]
            ten_run_algorithm_Hvs = {algorithm: [] for algorithm in algorithm_list}
            data = {algorithm: {'Mean': 0, 'Std': 0, 'Min': 0, 'Max': 0, 'Median': 0} for algorithm in algorithm_list}
            for algorithm, Hvs in algorithm_Hvs.items():
                if get_al_name(algorithm) in ten_run_algorithm_Hvs:
                    # ten_run_algorithm_Hvs[get_al_name(algorithm)].append(sum(Hvs) / len(Hvs))
                    ten_run_algorithm_Hvs[get_al_name(algorithm)].append(sum(Hvs))
            for algorithm, Hvs in ten_run_algorithm_Hvs.items():
                latex_dict[get_al_name(algorithm)].extend([pd.Series(Hvs).mean(), pd.Series(Hvs).median(), pd.Series(Hvs).std()])
                data[algorithm]['Mean'] = pd.Series(Hvs).mean()
                data[algorithm]['Std'] = pd.Series(Hvs).std()
                data[algorithm]['Min'] = pd.Series(Hvs).min()
                data[algorithm]['Max'] = pd.Series(Hvs).max()
                data[algorithm]['Median'] = pd.Series(Hvs).median()
            df = pd.DataFrame(data).T
            df.to_excel(writer, sheet_name=str(cluster_name))

    # 将字典值转换为矩阵
    matrix = [values for values in latex_dict.values()]

    # 计算特定列的最大值
    max_values = {col: max(row[col] for row in matrix) for col in [0, 1, 3, 4, 6, 7]}

    # 遍历并打印每个键和其对应的值
    for key, values in latex_dict.items():
        formatted_values = []
        for i, value in enumerate(values):
            # 检查当前列的值是否为最大值
            if i in max_values and value == max_values[i]:
                formatted_values.append(f"\\underline{{{value:.2f}}}")
            else:
                formatted_values.append(f"{value:.2f}")
        # 将值拼接成字符串
        formatted_string = "& " + " & ".join(formatted_values) + r" \\"
        print(f"Key: {key}, Values: {formatted_string}")
    #
    # for key, values in latex_dict.items():
    #     formatted_values = " & ".join([f"{value:.3f}" for value in values])
    #     formatted_string = f"& {formatted_values} "+r" \\"
    #     # 打印键和格式化后的字符串
    #     print(f"Key: {key}, Values: {formatted_string}")



def visualize_clusters_plotly(statistics, k, clustering_method, max_platform_box_num_list):
    if clustering_method == 'kmeans':
        clustering = KMeans(n_clusters=k)
    elif clustering_method == 'hierarchical':
        clustering = AgglomerativeClustering(n_clusters=k)
    elif clustering_method == 'dbscan':
        clustering = DBSCAN(eps=0.5, min_samples=1)
    elif clustering_method == 'spectral':
        clustering = SpectralClustering(n_clusters=k, affinity='nearest_neighbors')
    else:
        raise ValueError("无效的聚类方法，请选择 'kmeans', 'hierarchical', 'dbscan' 或 'spectral'")

    labels = clustering.fit_predict(statistics)

    # 计算每个聚类的中心
    cluster_centers = [np.mean([statistics[j] for j in range(len(statistics)) if labels[j] == i], axis=0) for i in
                       set(labels)]

    # # 计算每个实例到其所在聚类中心的距离
    # distances = [np.linalg.norm(statistics[i] - cluster_centers[labels[i]]) for i in range(len(statistics))]
    #
    # # 在每个聚类中找到距离中心最近的实例
    # closest, _ = pairwise_distances_argmin_min(cluster_centers, statistics)
    #
    # # 打印最接近聚类中心的实例名
    # for i in set(labels):
    #     print(f'Cluster {i + 1}: {file_names[closest[i]]}')

    data = []
    cluster_files = {}  # 新增一个字典来保存每个聚类的文件名
    cluster_boundaries = {}
    cluster_max_platform_box_num = {}
    for i in set(labels):
        cluster_data = [statistics[j] for j in range(len(statistics)) if labels[j] == i]
        cluster_files[i] = [file_names[j] for j in range(len(file_names)) if labels[j] == i]  #
        cluster_max_platform_box_num[i] = [max_platform_box_num_list[j] for j in range(len(max_platform_box_num_list)) if labels[j] == i]

        print(i)
        if len(cluster_files[i]) == 68:
            print('Large')
        elif len(cluster_files[i]) == 98:
            print('Medinum')
        else:
            print('Small')

        # print(len(cluster_files[i]))
        tmp_list = sorted([max_platform_box_num_list[j] for j in range(len(max_platform_box_num_list)) if labels[j] == i], reverse=True)
        print(tmp_list)
        print('Min:', min(tmp_list))
        print('Max:', max(tmp_list))
        print('Std:', np.std(tmp_list))
        print('Max/Sum: ', f"{tmp_list[0]*100/sum(tmp_list):.2f}%")



        x = [d[0] for d in cluster_data]
        y = [d[1] for d in cluster_data]
        z = [d[2] for d in cluster_data]




    #     cluster_boundaries[i] = {
    #         '箱子数量': {
    #             '最小值': min(x),
    #             '最大值': max(x),
    #             '平均值': np.mean(x),
    #             '标准差': np.std(x)
    #         },
    #         '平台数量': {
    #             '最小值': min(y),
    #             '最大值': max(y),
    #             '平均值': np.mean(y),
    #             '标准差': np.std(y)
    #         },
    #         '车型数量': {
    #             '最小值': min(z),
    #             '最大值': max(z),
    #             '平均值': np.mean(z),
    #             '标准差': np.std(z)
    #         },
    #     }
    #
    #     trace = go.Scatter3d(
    #         x=x, y=y, z=z,
    #         mode='markers',
    #         marker=dict(size=6),
    #         name=f'Cluster {i + 1}'
    #     )
    #     data.append(trace)
    #
    # # 打印每个聚类的文件名
    # for cluster, files in cluster_files.items():
    #     print(f'Cluster {cluster + 1}: {len(files)}')

    cluster_HVs = work("./all_data/inputs250", "./all_data/outputs250", cluster_files)

    # save_to_excel_1(cluster_HVs, cluster_files, f'{clustering_method}_K{k}_clusters.xlsx')
    save_to_excel_2(cluster_HVs, f'{clustering_method}_K{k}_clusters.xlsx')

    # # 打印每个聚类的最大值和最小值
    # for cluster, boundaries in cluster_boundaries.items():
    #     print(f'Cluster {cluster + 1}: {boundaries}')

    # layout = go.Layout(
    #     scene=dict(
    #         xaxis_title='Number of Cargoes',
    #         yaxis_title='Number of Points',
    #         zaxis_title='Number of Truck Types'
    #     )
    # )
    # fig = go.Figure(data=data, layout=layout)

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    #
    # colors = ['r', 'g', 'b']  # 为每个聚类设置不同的颜色
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for i, m, l in zip(list(set(labels)), ['o', '^', 'P'], ['0EMO-2021-Small', '1-2021-Medium', '2EMO-2021-Large']):
        cluster_data = [statistics[j] for j in range(len(statistics)) if labels[j] == i]
        x = [d[0] for d in cluster_data]
        y = [d[1] for d in cluster_data]
        z = [d[2] for d in cluster_data]

        # ax.scatter(x, y, z, c=colors[i], marker='o')
        ax.scatter(x, y, z, marker=m, label=l)

    ax.set_xlabel('Number of Cargoes')
    ax.set_ylabel('Number of Points')
    ax.set_zlabel('Number of Vehicle Types')

    # # 设置三个视图的方位角和仰角
    # ax.view_init(elev=20, azim=-35)
    # plt.savefig('cluster_1.pdf')
    #
    # ax.view_init(elev=20, azim=45)
    # plt.savefig('cluster_2.pdf')

    # ax.view_init(elev=20, azim=125)
    # plt.savefig('cluster_3.pdf')

    ax.view_init(elev=20, azim=125)
    ax.legend()  # 添加图例
    plt.savefig('cluster.svg')
    plt.show()

    # 把附加信息加到图里，方便查看
    # for i, boundaries in cluster_boundaries.items():
    #     fig.add_annotation(
    #         xref='paper',
    #         yref='paper',
    #         x=0.5,
    #         y=1 - 0.1 * (i + 1),
    #         showarrow=False,
    #         text=f'Cluster {i + 1}: {boundaries}',
    #         font=dict(size=10),
    #         align='center',
    #         xanchor='center',
    #         yanchor='top',
    #         bgcolor='white'
    #     )

    # offline.plot(fig, filename=f'{clustering_method}_K{k}_clusters.html', auto_open=False)


if __name__ == '__main__':
    statistics, file_names, max_platform_box_num_list = get_all_statistics()  # 获取统计信息和文件名 # 可以存成文件的
    # elbow_method(statistics)

    k = 3
    # visualize_clusters_plotly(statistics, k, clustering_method='kmeans')
    # visualize_clusters_plotly(statistics, k, clustering_method='hierarchical')
    visualize_clusters_plotly(statistics, k, 'spectral', max_platform_box_num_list)

    # k = 4
    # visualize_clusters_plotly(statistics, k, clustering_method='kmeans')
    # visualize_clusters_plotly(statistics, k, clustering_method='hierarchical')
    # visualize_clusters_plotly(statistics, k, clustering_method='spectral')

    # eps = 0.5
    # visualize_clusters_plotly(statistics, k=None, clustering_method='dbscan')

# ==========================================================================================
# 其他聚类方法
# 1. 层次聚类（Hierarchical Clustering）
# 层次聚类是一种基于树形结构的聚类方法，可以分为凝聚型（Agglomerative）和分裂型（Divisive）两种。凝聚型层次聚类从每个数据点作为一个单独的簇开始，然后逐步合并最接近的簇，直到达到指定的簇数量。以下是使用scikit-learn库中的AgglomerativeClustering类实现凝聚型层次聚类的示例代码：

# 2. DBSCAN（Density-Based Spatial Clustering of Applications with Noise）
# DBSCAN是一种基于密度的聚类算法，它将具有足够密度的区域划分为簇，并将较低密度的区域视为噪声。DBSCAN的主要优点是它可以发现任意形状的簇，并且对噪声具有较好的鲁棒性。以下是使用scikit-learn库中的DBSCAN类实现DBSCAN聚类的示例代码：

# 3. 谱聚类（Spectral Clustering）
# 谱聚类是一种基于图论的聚类方法，它将数据点表示为图中的节点，并根据数据点之间的相似性分配边的权重。谱聚类的主要思想是将图划分为具有最小切割代价的子图，从而形成簇。以下是使用scikit-learn库中的SpectralClustering类实现谱聚类的示例代码：
