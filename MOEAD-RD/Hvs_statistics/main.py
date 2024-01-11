import re

import numpy as np

def calculate_statistics(lst):
    mean = np.mean(lst)
    std = np.std(lst)
    min_value = np.min(lst)
    max_value = np.max(lst)
    median = np.median(lst)
    lower_quartile = np.percentile(lst, 25)
    upper_quartile = np.percentile(lst, 75)

    print(f"Mean: {mean:.2f}")
    print(f"Std: {std:.2f}")
    # print(f"Min: {min_value:.2f}")
    # print(f"Upper Quartile: {upper_quartile:.2f}")
    # print(f"Median: {median:.2f}")
    # print(f"Lower Quartile: {lower_quartile:.2f}")
    # print(f"Max: {max_value:.2f}")

    return mean, std, min_value, upper_quartile, median, lower_quartile, max_value

moead_final = []
moead_dra_final = []
moead_gra_final = []
moead_igr_dra_final = []
moead_igr_final = []
win_bronze = []
win_gold = []
win_silver = []


moead_igr_dra_final_case1 = []
moead_igr_dra_final_case2 = []
moead_igr_dra_final_case3 = []


moead_igr_gra_case1_T5 = []
moead_igr_gra_case1_T20 = []
moead_igr_gra_case2_T5 = []
moead_igr_gra_case2_T20 = []




with open("HV_value.txt", "r") as file:
    for line in file:
        if "MOEAD_input250_no" in line and "_final_noRSeed" in line:
            moead_final.append(float(re.findall("\d+\.\d+", line)[0]))
        elif "MOEAD+DRA_input250_no" in line and "_final_noRSeed" in line:
            moead_dra_final.append(float(re.findall("\d+\.\d+", line)[0]))
        elif "MOEAD+IGR+DRA_input250_no" in line and "_final_noRSeed" in line:
            moead_igr_dra_final.append(float(re.findall("\d+\.\d+", line)[0]))
        elif "MOEAD+IGR_input250_no" in line and "_final_noRSeed" in line:
            moead_igr_final.append(float(re.findall("\d+\.\d+", line)[0]))
        elif "winBronze_input250_eval2000_no" in line:
            win_bronze.append(float(re.findall("\d+\.\d+", line)[0]))
        elif "winGold_input250_eval2000_no" in line:
            win_gold.append(float(re.findall("\d+\.\d+", line)[0]))
        elif "winSilver_input250_eval2000_no" in line:
            win_silver.append(float(re.findall("\d+\.\d+", line)[0]))

        elif "MOEAD+IGR+DRA_input250" in line and "case1_DRATest_noRSeed_no" in line:
            moead_igr_dra_final_case1.append(float(re.findall("\d+\.\d+", line)[0]))

        elif "MOEAD+IGR+DRA_input250" in line and "case2_DRATest_noRSeed_no" in line:
            moead_igr_dra_final_case2.append(float(re.findall("\d+\.\d+", line)[0]))

        elif "MOEAD+IGR+DRA_input250" in line and "case3_DRATest_noRSeed_no" in line:
            moead_igr_dra_final_case3.append(float(re.findall("\d+\.\d+", line)[0]))

        elif "MOEAD+IGR+GRA_input250_case1_T5_GRATest" in line:
            moead_igr_gra_case1_T5.append(float(re.findall("\d+\.\d+", line)[0]))
        elif "MOEAD+IGR+GRA_input250_case1_T20_GRATest" in line:
            moead_igr_gra_case1_T20.append(float(re.findall("\d+\.\d+", line)[0]))
        elif "MOEAD+IGR+GRA_input250_case2_T5_GRATest" in line:
            moead_igr_gra_case2_T5.append(float(re.findall("\d+\.\d+", line)[0]))
        elif "MOEAD+IGR+GRA_input250_case2_T20_GRATest" in line:
            moead_igr_gra_case2_T20.append(float(re.findall("\d+\.\d+", line)[0]))
        elif "MOEAD+GRA_input250_DRAT5_no" in line:
            moead_gra_final.append(float(re.findall("\d+\.\d+", line)[0]))



# print("MOEAD_final:", moead_final)
# print("MOEAD+DRA_final:", moead_dra_final)
# print("MOEAD+IGR+DRA_final:", moead_igr_dra_final)
# print("MOEAD+IGR_final:", moead_igr_final)
# print("winBronze:", win_bronze)
# print("winGold:", win_gold)
# print("winSilver:", win_silver)
#
# print("MOEAD+IGR+DRA_case1:", moead_igr_dra_final_case1)
# print("MOEAD+IGR+DRA_case2:", moead_igr_dra_final_case2)
# print("MOEAD+IGR+DRA_case3:", moead_igr_dra_final_case3)
#
#
# print("MOEAD+IGR+GRA_input250_case1_T5:", moead_igr_gra_case1_T5)
# print("MOEAD+IGR+DRA_final_case2:", moead_igr_dra_final_case2)
# print("MOEAD+IGR+DRA_final_case3:", moead_igr_dra_final_case3)
#
# print("MOEAD+GRA_final:", moead_gra_final)


# import matplotlib.pyplot as plt
#
# # 列表数据
# data = [
#     moead_final,
#     moead_dra_final,
#     moead_igr_final,
#     moead_igr_dra_final
# ]

# # 算法标签
# labels = ['MOEAD', 'MOEAD-D', 'MOEAD-R', 'MOEAD-RD']
#
# # 绘制盒型图
# plt.figure(figsize=(10, 6))
# plt.boxplot(data, labels=labels)
# plt.title('Boxplot of Algorithms')
# plt.xlabel('Algorithms')
# plt.ylabel('Values')
#
# # 显示图形
# plt.show()


alg_dict = {
    'moead_final': moead_final,
    'moead_dra_final': moead_dra_final,
    'moead_gra_final': moead_gra_final,
    'moead_igr_final': moead_igr_final,
    'moead_igr_dra_final': moead_igr_dra_final,
    'moead_igr_gra_case1_T5': moead_igr_gra_case1_T5,
    'win_bronze': win_bronze,
    'win_gold': win_gold,
    'win_silver': win_silver,
    'moead_igr_dra_final_case1': moead_igr_dra_final_case1,
    'moead_igr_dra_final_case2': moead_igr_dra_final_case2,
    'moead_igr_dra_final_case3': moead_igr_dra_final_case3,
    'moead_igr_gra_case1_T20': moead_igr_gra_case1_T20,
    'moead_igr_gra_case2_T5': moead_igr_gra_case2_T5,
    'moead_igr_gra_case2_T20': moead_igr_gra_case2_T20
}

for name, value in alg_dict.items():
    print("==================================================================")
    print(name)
    print(len(value))
    calculate_statistics(value)






