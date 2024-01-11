import re
import numpy as np

# ================================================================================
def read_hv_values(file_path):
    hv_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'(\d+\+\d+\+[\d.]+\+[\d.]+\+\d+)_no\d+, (\d+\.\d+)', line)
            if match:
                params = match.group(1)
                hv_value = float(match.group(2))
                if params in hv_dict:
                    hv_dict[params].append(hv_value)
                else:
                    hv_dict[params] = [hv_value]

    return hv_dict


file_path = 'HV_value.txt'  # 将此路径替换为你的文件路径
hv_values_dict = read_hv_values(file_path)


# ================================================================================
for params, hv_list in hv_values_dict.items():
    mean_value = np.mean(hv_list)
    length = len(hv_list)
    print(f'键值：{params}，mean：{mean_value:.4f}，长度：{length}')



# ================================================================================
from collections import defaultdict
import numpy as np

# 对hv_values_dict中的每个键按种群大小进行分组
grouped_hv_values = defaultdict(list)

for params, hv_list in hv_values_dict.items():
    population_size = params.split('+')[0]  # 获取种群大小
    grouped_hv_values[population_size].extend(hv_list)  # 添加HV值到对应的种群大小

# 计算每个种群大小的HV值列表的均值和长度，并打印结果
for population_size, hv_list in grouped_hv_values.items():
    mean_value = np.mean(hv_list)
    length = len(hv_list)
    print(f'种群大小：{population_size}，mean：{mean_value:.2f}，长度：{length}')

# ================================================================================
from collections import defaultdict
import numpy as np

# 假设 hv_values_dict 已经通过之前的函数填充完成
# 参数名列表
parameters = ['N', 'T', 'n', 'm', 't']

# 初始化一个字典来存储每个参数和其所有对应的HV值
grouped_hv_values = {param: defaultdict(list) for param in parameters}

for params, hv_list in hv_values_dict.items():
    # 分割参数字符串
    split_params = params.split('+')
    # 遍历参数名和它们在字符串中的位置
    for i, param_name in enumerate(parameters):
        # 分别按照参数名收集HV值
        grouped_hv_values[param_name][split_params[i]].extend(hv_list)

# 遍历参数名和它们对应的字典
for param_name, param_dict in grouped_hv_values.items():
    # 输出每个参数的均值和长度
    for param_value, hv_list in param_dict.items():
        mean_value = np.mean(hv_list)
        length = len(hv_list)
        print(f'{param_name}值：{param_value}，mean：{mean_value:.4f}，长度：{length}')








# ================================================================================
import pandas as pd


def create_excel(hv_values_dict, output_file):
    # 准备数据列表
    data = []

    # 遍历字典，计算HV均值并准备每行数据
    for params, hv_values in hv_values_dict.items():
        # 分割参数字符串，转换成列表
        param_values = params.split('+')
        # 确保所有参数都被转换成了正确的数据类型
        param_values = [int(param_values[0]), int(param_values[1]), float(param_values[2]), float(param_values[3]),
                        int(param_values[4])]
        # 计算HV值的均值
        hv_mean = sum(hv_values) / len(hv_values)
        # 添加参数值和均值到数据列表
        data.append(param_values + [hv_mean])

    # 创建DataFrame
    df = pd.DataFrame(data, columns=['N', 'T', 'n', 'm', 't', 'HV'])

    # 写入Excel文件
    df.to_excel(output_file, index=False)


# 用法示例
output_file = 'HV_averages.xlsx'  # 输出文件名
create_excel(hv_values_dict, output_file)










# ================================================================================
import pandas as pd


def save_to_excel(hv_values_dict, excel_path):
    # 准备数据列表，用于创建DataFrame
    data = []

    # 遍历字典，分解每个键并扩展HV值列表到多行
    for params, hv_values in hv_values_dict.items():
        # 分解参数值
        param_values = params.split('+')
        # 确保所有参数都被转换成了正确的数据类型
        param_values = [int(param_values[0]), int(param_values[1]), float(param_values[2]), float(param_values[3]),
                        int(param_values[4])]
        # 为每个HV值创建一行
        for hv in hv_values:
            data.append(param_values + [hv])

    # 创建DataFrame
    df = pd.DataFrame(data, columns=['N', 'T', 'n', 'm', 't', 'HV'])

    # 将DataFrame保存到Excel文件
    df.to_excel(excel_path, index=False, engine='openpyxl')


# 使用示例
excel_path = 'HV_values.xlsx'  # Excel文件保存位置
save_to_excel(hv_values_dict, excel_path)




