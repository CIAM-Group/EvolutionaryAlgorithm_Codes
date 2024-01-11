import os
import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt

from MOEAD_MD.my_io import join_path, read_input_file
from MOEAD_MD.process_data import get_platform_info, get_truck_type_info, get_platform_box


def get_platform_list(input_dir):
    file_names = os.listdir(input_dir)
    platform_nums = []
    for file_name in file_names:
        data = read_input_file(join_path(input_dir, file_name))
        platform_list, must_visited_dict = get_platform_info(data)
        num = 0
        for key in must_visited_dict:
            if must_visited_dict[key] is True:
                num += 1
        platform_num = len(platform_list)
        platform_nums.append(platform_num)
    platform_nums.sort()
    return platform_nums


def get_platform_num_boxplot():
    # 获得仓库数量的箱图
    input_dir = '../data/inputs'
    dataset50 = get_platform_list(input_dir)
    input_dir = '../data/inputs200'
    dataset200 = get_platform_list(input_dir)
    input_dir = '../data/inputs250'
    dataset250 = get_platform_list(input_dir)
    fig, ax = plt.subplots()
    ax.boxplot([dataset50, dataset200, dataset250], vert=True, showmeans=True, meanline=True, labels=['Dataset 50',
                                                                                                      'Dataset 200',
                                                                                                      'Dataset 250'])
    # ax.set_xlabel('number of platforms')
    ax.set_title('Number of platforms')
    plt.savefig(f'../data/imgs/Number_of_platforms.eps')
    plt.show()


# def get_distance_heatmap():
#     # 绘制节点之间距离的热力图
#     input_dir = '../data/inputs200'
#     file_names = os.listdir(input_dir)
#     for file_name in file_names:
#         data = read_input_file(join_path(input_dir, file_name))
#         platform_list, must_visited_dict = get_platform_info(data)
#         node_dict = {x: (i + 1) for i, x in enumerate(platform_list)}
#         node_dict['start_point'] = 0
#         node_dict['end_point'] = len(platform_list) + 1
#         distance_map = data["algorithmBaseParamDto"]["distanceMap"]
#         distance = np.full((len(platform_list) + 2, len(platform_list) + 2), -1)
#
#         for key in distance_map:
#             x = node_dict[key.split('+')[0]]
#             y = node_dict[key.split('+')[1]]
#             distance[x][y] = distance_map[key]
#         # if np.sum(distance==-1) != 0:
#         #     print('no') # 有的并不是全连接图
#         sns.heatmap(distance)
#         plt.savefig(f'../data/imgs/{file_name}.eps')
#         plt.show()


def get_box_list(input_dir):
    file_names = os.listdir(input_dir)
    box_num_list = []
    for file_name in file_names:
        data = read_input_file(join_path(input_dir, file_name))
        box_num_list.append(len(data['boxes']))
    return box_num_list


def get_box_num_boxplot():
    # 获得箱子的统计量，就计算一下每个订单总共的箱子数量吧
    # 统计箱子数量的图
    input_dir = '../data/inputs'
    dataset50 = get_box_list(input_dir)
    input_dir = '../data/inputs200'
    dataset200 = get_box_list(input_dir)
    input_dir = '../data/inputs250'
    dataset250 = get_box_list(input_dir)
    fig, ax = plt.subplots()
    ax.boxplot([dataset50, dataset200, dataset250], vert=True, showmeans=True, meanline=True, labels=['Dataset 50',
                                                                                                      'Dataset 200',
                                                                                                      'Dataset 250'])
    # ax.set_xlabel('Box Number')
    ax.set_title('Number of boxes')
    plt.savefig(f'../data/imgs/Number_of_boxes.eps')
    plt.show()


def get_truck_list(input_dir):
    file_names = os.listdir(input_dir)
    truck_num_list = []
    for file_name in file_names:
        data = read_input_file(join_path(input_dir, file_name))
        truck_num_list.append(len(data['algorithmBaseParamDto']['truckTypeDtoList']))
    return truck_num_list


def get_truck_num_boxplot():
    # 获得货车数量的统计量
    input_dir = '../data/inputs'
    dataset50 = get_truck_list(input_dir)
    input_dir = '../data/inputs200'
    dataset200 = get_truck_list(input_dir)
    input_dir = '../data/inputs250'
    dataset250 = get_truck_list(input_dir)
    fig, ax = plt.subplots()
    ax.boxplot([dataset50, dataset200, dataset250], vert=True, showmeans=True, meanline=True, labels=['Dataset 50',
                                                                                                      'Dataset 200',
                                                                                                      'Dataset 250'])
    # ax.set_xlabel('Number of truck types')
    ax.set_title('Number of truck types')
    plt.savefig(f'../data/imgs/Number_of_types.eps')
    plt.show()

def get_same_size_box_ratio(boxes, platform_list):
    platform_boxex_dict = {x: [y for y in boxes if y['platformCode'] == x] for x in platform_list}
    # 返回每个仓库同大小的箱子占总箱子数目的比例？
    # 这个用盒图表示吧，数据集里所有instance的所有platform都放一起
    platform_same_size_box_ratio = []
    for platform in platform_boxex_dict:
        platform_boxes = platform_boxex_dict[platform]
        size_dict = {}
        for box in platform_boxes:
            size = (min(box['width'], box["length"]), max(box['width'], box["length"]), box['height'])
            if size not in size_dict:
                size_dict[size] = 0
            size_dict[size] += 1
        size_num_list = [size_dict[key] for key in size_dict]
        platform_same_size_box_ratio.append(max(size_num_list)/len(platform_boxes))
    return platform_same_size_box_ratio

def get_same_size_box_ratio_boxplot(input_dir):
    file_names = os.listdir(input_dir)
    all_platform_same_size_box_ratio = []
    for file_name in file_names:
        data = read_input_file(join_path(input_dir, file_name))
        platform_list, must_visited_dict = get_platform_info(data)
        boxes = data['boxes']
        platform_same_size_box_ratio = get_same_size_box_ratio(boxes, platform_list)
        all_platform_same_size_box_ratio.extend(platform_same_size_box_ratio)

    fig, ax = plt.subplots(figsize=(20, 6))
    ax.hist(all_platform_same_size_box_ratio, density=True, alpha=0.5)
    ax.set_title('Proportion of homogeneous boxes in platforms')
    # plt.savefig(f'../data/imgs/Number_of_types.eps')
    plt.show()


def get_platform_num_box_num_plot(input_dir):
    file_names = os.listdir(input_dir)
    platform_num_list = []
    boxes_num_per_platform = []
    for file_name in file_names:
        data = read_input_file(join_path(input_dir, file_name))
        platform_list, must_visited_dict = get_platform_info(data)
        platform_num = len(platform_list)
        platform_num_list.append(platform_num)
        boxes = data['boxes']
        boxes_num_dict = {x: 0 for x in platform_list}
        for one in boxes:
            boxes_num_dict[one['platformCode']] += 1
        boxes_num_list = [boxes_num_dict[key] for key in boxes_num_dict]
        boxes_num_per_platform.extend(boxes_num_list)

    num_instance = len(platform_num_list)
    # 绘制图形
    fig, ax1 = plt.subplots(figsize=(10, 8))
    # 设置左轴
    color = '#7aa6c2'
    ax1.set_xlabel('Data Index')
    ax1.set_ylabel('Number of Warehouses', color=color)
    ax1.bar(range(num_instance), platform_num_list, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # 设置右轴
    ax2 = ax1.twinx()
    # color = 'tab:blue'
    color = '#ffb347'
    ax2.set_ylabel('Number of Boxes per Warehouse', color=color)
    # ax2.plot(range(num_warehouses), [avg_boxes_per_warehouse] * num_warehouses, '--', color=color)
    num_box = []
    for i, x in enumerate(platform_num_list):
        num_box.extend([i]*x)
    # print(num_box)
    # print(boxes_num_per_platform)
    ax2.scatter(num_box, boxes_num_per_platform, s=15, marker='o', c='none', edgecolors=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # 设置图例
    ax1.legend(['Number of Warehouses'], loc='upper left')
    ax2.legend(['Average Boxes per Warehouse', 'Boxes per Warehouse'], loc='upper right')

    # 显示图形
    plt.show()

# get_platform_num_boxplot()
# get_distance_heatmap()
# get_box_num_boxplot()
# get_platform_num_box_num_plot('../data/inputs')
# get_same_size_box_ratio_boxplot('../data/inputs')

def print_list(num_list):
    # 将列表转换为numpy数组
    num_list = np.array(num_list)
    # 计算最大值
    max_value = np.max(num_list)
    print("最大值:", max_value)
    # 计算最小值
    min_value = np.min(num_list)
    print("最小值:", min_value)
    # 计算平均值
    average_value = np.mean(num_list)
    print("平均值:", average_value)
    # 计算方差
    std = np.std(num_list)
    print("std:", std)

    #
    sum = np.sum(num_list)
    print("总:", sum)

num_list = np.array(get_box_list('../data/inputs250'))

print_list(num_list)
