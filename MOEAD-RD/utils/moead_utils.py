import re
import time
import random
import functools
import numpy as np
import matplotlib.pyplot as plt
from global_var import *

# 这个文件中存储了MOEAD进化过程中的辅助函数，如个体交叉变异函数，子问题分解方法等

def time_count_hooks(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        use_time = result[0]
        if func.__name__ == 'get_new_sol':
            gener_use_times.extend(use_time)
        elif func.__name__ == 'expensive_eval':
            eval_use_times.extend(use_time)
        elif func.__name__ == 'get_init_pop':
            init_use_times.extend(use_time)
        if len(result) == 2:
            return result[1]
        elif len(result) == 3:
            return result[1], result[2]
        return result[1], result[2], result[3]
    return wrapper

def convert_res_trucks_to_subsols(res_truck_list):
    real_sub_sols = []  # 装箱后得到真实的子路径
    for truck in res_truck_list:
        platform_digits = [int(re.findall(r'\d+', platform)[0]) for platform in truck['platformArray']]
        real_sub_sols.append(platform_digits)
    return real_sub_sols


class Individual:
    def __init__(self, sol, f1, f2, res_truck_list=None):
        self.sol = sol
        self.f1 = f1
        self.f2 = f2
        self.res_truck_list = res_truck_list
        # if res_truck_list is not None:
        #     self.sub_sols = convert_res_trucks_to_subsols(res_truck_list)


def cross(sol1, sol2):
    index1 = random.randint(0, len(sol1) - 1)
    index2 = random.randint(index1, len(sol1) - 1)
    tempGene = sol2[index1:index2]
    newGene = []
    p1len = 0
    for g in sol1:
        if p1len == index1:
            newGene.extend(tempGene)  # 插入基因片段
            p1len += 1
        if g not in tempGene:
            newGene.append(g)
            p1len += 1
    return newGene


def relocate(sol):
    index1 = random.randint(0, len(sol) - 1)
    index2 = random.randint(0, len(sol) - 1)
    tag = 1000
    while tag > 0 and index1 == index2:
        index2 = random.randint(0, len(sol) - 1)
        tag -= 1
    if index1 == index2:
        return sol
    index1, index2 = min(index1, index2), max(index1, index2)
    newSol = sol[:]  # 防止变异到父代

    if index2 != len(sol) - 1:
        newSol = newSol[:index1] + [newSol[index2]] + newSol[index1 + 1:index2] + [newSol[index1]] + newSol[index2 + 1:]
    else:
        newSol = newSol[:index1] + [newSol[index2]] + newSol[index1 + 1:index2] + [newSol[index1]]
    assert set(newSol) == set(sol) and len(newSol) == len(sol)
    return newSol


def relocate_to_first(sol):
    # relocate到开头
    index1 = random.randint(0, len(sol) - 1)
    newSol = sol[:]  # 防止变异到父代
    if index1 != len(sol) - 1:
        newSol = [newSol[index1]] + newSol[:index1] + newSol[index1 + 1:]
    else:
        newSol = [newSol[index1]] + newSol[:index1]
    assert set(newSol) == set(sol) and len(newSol) == len(sol)
    return newSol


def opt2(sol):
    index1 = random.randint(0, len(sol) - 2)
    index2 = random.randint(1, len(sol) - 1)
    tag = 1000
    while tag > 0 and index1 == index2:
        index2 = random.randint(0, len(sol) - 1)
        tag -= 1
    if index1 == index2:
        return sol
    index1, index2 = min(index1, index2), max(index1, index2)
    newSol = sol[:]

    A = newSol[:index1] if index1 != 0 else []
    B = newSol[index2:index1 - 1:-1] if index1 != 0 else newSol[index2::-1]
    C = newSol[index2 + 1:] if index2 != len(sol) - 1 else []
    newSol = A + B + C
    assert set(newSol) == set(sol) and len(newSol) == len(sol)
    return newSol


def single_point_inversion(sol):
    index = random.randint(0, len(sol) - 1)
    newSol = sol[:]  # 防止变异到父代
    newSol = newSol[index:] + newSol[:index]
    return newSol


def get_no_domain_pop(pop):
    if len(pop) == 0:
        return pop
    tmp_pop = sorted(pop, key=lambda x: (x.f1, x.f2))
    no_domain_pop = []
    for i, x in enumerate(tmp_pop):
        if i == 0 or x.f2 < no_domain_pop[-1].f2:
            no_domain_pop.append(x)
    return no_domain_pop


def gPBI(one, index, ref_dirs, z_min, z_max, rf_point_tag=0):

    def my_calc_distance_to_weights(F, weights, utopian_point=None, rf_point_tag=None):
        norm = np.linalg.norm(weights, axis=1)
        if rf_point_tag == 0:
            if utopian_point is not None:
                F = F - utopian_point
            d1 = (F * weights).sum(axis=1) / norm
            d2 = np.linalg.norm(F - (d1[:, None] * weights / norm[:, None]), axis=1)
        else:
            if utopian_point is not None:
                F = utopian_point - F
            d1 = (F * weights).sum(axis=1) / norm
            d2 = np.linalg.norm(F - (d1[:, None] * weights / norm[:, None]), axis=1)

        return d1, d2

    f_x = np.array(one) if isinstance(one, list) else np.array([one.f1, one.f2])
    np_z_min = np.array([z_min[0] if z_min[0] != z_max[0] else 0, z_min[1] if z_min[1] != z_max[1] else 0])
    np_z_max = np.array([z_max[0], z_max[1]])
    norm_f_x = (f_x - np_z_min) / (np_z_max - np_z_min)
    now_utopian_point = np.array([0, 0]) if rf_point_tag == 0 else np.array([1, 1])
    d1, d2 = my_calc_distance_to_weights(
        norm_f_x[None, :], np.array(ref_dirs[index])[None, :],
        utopian_point=now_utopian_point, rf_point_tag=rf_point_tag)
    return d1 + 5 * d2


def gTe(one, index, ref_dirs, z_min, z_max, rf_point_tag):  # 优化过程目标 最小化这个值
    ans = 0
    if rf_point_tag == 0:
        utopia = 0.95
        if isinstance(one, list):
            if z_max[0] != z_min[0]:
                ans = max(ans, ref_dirs[index][0] * abs(one[0] - z_min[0] * utopia) / (z_max[0] - z_min[0]))
            else:
                ans = max(ans, ref_dirs[index][0] * abs(one[0] - 0 * utopia) / (z_max[0] - 0))

            if z_max[1] != z_min[1]:
                ans = max(ans, ref_dirs[index][1] * abs(one[1] - z_min[1] * utopia) / (z_max[1] - z_min[1]))
            else:
                ans = max(ans, ref_dirs[index][1] * abs(one[1] - 0 * utopia) / (z_max[1] - 0))
        else:
            if z_max[0] != z_min[0]:
                ans = max(ans, ref_dirs[index][0] * abs(one.f1 - z_min[0] * utopia) / (z_max[0] - z_min[0]))
            else:
                ans = max(ans, ref_dirs[index][0] * abs(one.f1 - 0 * utopia) / (z_max[0] - 0))

            if z_max[1] != z_min[1]:
                ans = max(ans, ref_dirs[index][1] * abs(one.f2 - z_min[1] * utopia) / (z_max[1] - z_min[1]))
            else:
                ans = max(ans, ref_dirs[index][1] * abs(one.f2 - 0 * utopia) / (z_max[1] - 0))
    else:
        ans = float('inf')
        if isinstance(one, list):
            if z_max[0] != z_min[0]:
                ans = min(ans, ref_dirs[index][0] * abs(one[0] - z_max[0]) / (z_max[0] - z_min[0]))
            else:
                ans = min(ans, ref_dirs[index][0] * abs(one[0] - 0) / (z_max[0] - 0))

            if z_max[1] != z_min[1]:
                ans = min(ans, ref_dirs[index][1] * abs(one[1] - z_max[1]) / (z_max[1] - z_min[1]))
            else:
                ans = min(ans, ref_dirs[index][1] * abs(one[1] - 0) / (z_max[1] - 0))
        else:
            if z_max[0] != z_min[0]:
                ans = min(ans, ref_dirs[index][0] * abs(one.f1 - z_max[0]) / (z_max[0] - z_min[0]))
            else:
                ans = min(ans, ref_dirs[index][0] * abs(one.f1 - 0) / (z_max[0] - 0))

            if z_max[1] != z_min[1]:
                ans = min(ans, ref_dirs[index][1] * abs(one.f2 - z_max[1]) / (z_max[1] - z_min[1]))
            else:
                ans = min(ans, ref_dirs[index][1] * abs(one.f2 - 0) / (z_max[1] - 0))
    return ans


def gWs(one, index, ref_dirs, z_min=None, z_max=None):
    return one.f1 * ref_dirs[index][0] + (one.f2 / 4e6) * ref_dirs[index][1]


def roulette_wheel_selection(fitness, num_parents):
    probabilities = fitness / np.sum(fitness)
    cumulative_probabilities = np.cumsum(probabilities)
    selected_indices = []
    for i in range(num_parents):
        p = np.random.random()
        selected_index = np.where(cumulative_probabilities >= p)[0][0]
        selected_indices.append(selected_index)
    return selected_indices


def draw(deltas, save_path=None):
    mean = np.mean(deltas)
    median = np.median(deltas)
    max_val = np.max(deltas)
    min_val = np.min(deltas)
    plt.hist(deltas, bins=30, density=True, alpha=0.75)
    plt.xlim([0, 0.175])
    plt.ylim([0, 100])
    # 添加横轴、纵轴标签和图表标题
    plt.xlabel("Subproblem Improvement Size")
    plt.ylabel("Number of Individuals")
    plt.title("Probability Density Function")

    # 添加文本标注
    plt.text(0.95, 0.95, "Mean: {:.4f}".format(mean),
             transform=plt.gca().transAxes, ha='right', va='top')
    plt.text(0.95, 0.9, "Median: {:.4f}".format(median),
             transform=plt.gca().transAxes, ha='right', va='top')
    plt.text(0.95, 0.85, "Max value: {:.4f}".format(max_val),
             transform=plt.gca().transAxes, ha='right', va='top')
    plt.text(0.95, 0.8, "Min value: {:.4f}".format(min_val),
             transform=plt.gca().transAxes, ha='right', va='top')
    if save_path != None:
        plt.savefig(save_path)
    plt.show()


def get_random_sol(platfrom_list):
    sol = platfrom_list[:]
    random.shuffle(sol)
    return sol

@time_count_hooks
def get_init_pop(pop_size, visited_sols_dict, evaluate):
    pop = []
    platform_list = evaluate.platform_list
    use_time = []
    for _ in range(pop_size):
        start_time = time.time()
        sol = get_random_sol(platform_list)
        tag = 1000
        while tag > 0 and tuple(sol) in visited_sols_dict:
            sol = get_random_sol(platform_list)
            tag -= 1
        visited_sols_dict[tuple(sol)] = True
        use_time.append(time.time() - start_time)
        res_truck_list, f1, f2 = evaluate.expensive_eval(sol)
        new_one = Individual(sol, f1, f2, res_truck_list)
        pop.append(new_one)
    return use_time, pop
    # return pop



