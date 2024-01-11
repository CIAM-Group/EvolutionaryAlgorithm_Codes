import re
import statistics
import numpy as np
import pandas as pd

# 读取文件
with open('Hvs_statistics/HV_value.txt', 'r') as f:
    lines = f.readlines()

# 解析文件
results = {}
for line in lines:
    match = re.search(r': (.*?), (\d+\.\d+)', line)
    if match:
        algorithm = match.group(1)
        if '_no' not in algorithm:  # 如果算法名称中不存在"_no"，跳过
            continue
        algorithm = re.sub(r'_no\d+', '', algorithm)  # 去掉_noi部分
        hv = float(match.group(2))
        if algorithm not in results:
            results[algorithm] = []
        results[algorithm].append(hv)


# 初始化DataFrame
df = pd.DataFrame(index=results.keys())
tricks = ['bias', 'relative', 'real', 'mean+', 'matchJ', 'sumT', 'meanT', 'meanS', 'deltaT']
# 初始化trick列
for trick in tricks:
    df[trick] = ''

# 检查并标记trick
for name in df.index:
    for trick in tricks:
        if trick in name:
            if trick == 'bias':
                pattern = r'\+\d+\.\d+$'
                match = re.search(pattern, name)
                # match = re.search(r"\d+\.\d+", name)
                if match:
                    df.loc[name, trick] = match.group()
            elif trick == 'deltaT':
                df.loc[name, trick] = re.search(r'deltaT(\d+)', name).group(1)
            else:
                df.loc[name, trick] = '√'

# 计算mean, std, min, max并添加到DataFrame
for name, values in results.items():
    df.loc[name, 'Mean'] = np.mean(values)
    df.loc[name, 'Std'] = np.std(values)
    df.loc[name, 'Min'] = np.min(values)
    df.loc[name, 'Max'] = np.max(values)
    df.loc[name, 'Len'] = len(values)
    df.loc[name, 'Median'] = np.median(values)

# 保存到excel
df.to_excel('results.xlsx')