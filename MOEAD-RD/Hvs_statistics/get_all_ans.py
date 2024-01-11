import re
from collections import defaultdict

def extract_data_from_file(file_path):
    pattern = re.compile(r":\s+([a-zA-Z0-9+_]+(?:_no\d+)?[\w]*),\s+([\d.]+)")
    results = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                # 提取整个算法名称和数值
                full_algorithm, value = match.groups()
                # 移除 "_no数字" 部分
                algorithm = re.sub(r"_no\d+", "", full_algorithm)
                # 将数值转换为浮点数并添加到对应的列表中
                results[algorithm].append(float(value))
    return dict(results)

def extract_data_from_file2(file_path):
    results = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            full_algorithm, value = line.split(', ')
            # 移除 "_no数字" 部分
            algorithm = re.sub(r"_no\d+", "", full_algorithm)
            # 将数值转换为浮点数并添加到对应的列表中
            results[algorithm].append(float(value))
    return dict(results)


# Example usage
filepath = 'HV_value.txt'  # Replace with your actual file path
results = extract_data_from_file2(filepath)
# print(results)

# =====================
# 输出特定键值的 mean，median，min, max, std

# key_list = [
#     'MOEAD+DTR_gPBI',
#     'MOEAD+AAWN',
#     'MOEAD+AGR_all',
#     # 'MOEAD+AGR_one',
#     'winSilver_input250_eval2000',
#     'winGold_input250_eval2000',
#     'winBronze_input250_eval2000',
#     # 'MOEAD_input250_final_noRSeed',
#     # 'MOEAD+IGR_input250_final_noRSeed'
#     'MOEAD',
#     'MOEAD+GRA',
#     'MOEAD+IGR',
#     'MOEAD+IGR+GRA',
#     # 'MOEAD+GRA_matchV_mean+sumT+deltaT8'
# ]


key_list = [
    'MOEAD_IGRCount',
    'MOEAD+IGR_IGRCount',
]

import statistics

def print_stats(results, key_list):
    for key in key_list:
        ns_list = [10,20,30,40,50]
        for ns in ns_list:
            key2 = key+f'_ns{ns}'
            if key2 in results:
                data = results[key2]
                mean = statistics.mean(data)
                median = statistics.median(data)
                std = statistics.stdev(data)
                min_val = min(data)
                max_val = max(data)
                # &   &   &   &   &   \\
                print(f"{key2} & {mean:.2f} & {median:.2f} & {std:.2f} & {min_val:.2f} & {max_val:.2f}" + r"\\")
            else:
                print(f"{key2}: No data available")

# 用法示例：
print_stats(results, key_list)















