import copy
import math
from scipy.spatial.distance import cdist

from MOEAD_MD.moead_base import MOEAD_MD_BASE
from MOEAD_MD.my_io import *
from MOEAD_MD.evaluate import Evaluate

from utils.utils import *
from utils.moead_utils import *
from utils.getHV_utils import *
from utils.gene_sols_utils import *

class MOEAD_MD(MOEAD_MD_BASE):
    def __init__(self, method_params, data_params):
        super().__init__(method_params, data_params)

    @time_count_hooks
    def get_new_sol(self, i: int, select_rate, mutate_rate):
        start_time = time.time()
        p1, p2 = self.get_p1_p2(i, select_rate)
        new_sol, _ = CrossForNNCoding.pmx_crossover(p1.sol, p2.sol)
        if random.random() < mutate_rate or new_sol == p1.sol or new_sol == p2.sol:
            new_sol = MutateForNNCoding.relocate(new_sol)
        use_time = [time.time()-start_time]
        return use_time, new_sol

    def one_replace(self, index, new_one):
        pop_size = len(self.pop)
        # GR
        tag = index
        # gr log
        for j in range(pop_size):
            if self.fun(new_one, j) < self.fun(new_one, tag):
                tag = j
        if tag not in self.neighbors[index]:
            self.gr_log += 1
        tag = index

        # GR / IGR
        if any(x in self.method_params['trick'] for x in ['IGR', 'GR']):
            for j in range(pop_size):
                if self.fun(new_one, j) < self.fun(new_one, tag):
                    tag = j
        self.unMatchedSub[tag] = 1  

        discard_ones = []

        matchJ_delta_fun = 0

        if 'test_trick' in self.method_params and 'relative' in self.method_params['test_trick']:
            matchJ_delta_fun += 1 - self.fun(new_one, tag) / self.fun(self.pop[tag], tag)
        else:
            matchJ_delta_fun += self.fun(self.pop[tag], tag) - self.fun(new_one, tag)

        all_delta_fun = [] 
        now_neighbors = self.neighbors[tag]
        for j in now_neighbors:
            delta_fun = self.fun(self.pop[j], j) - self.fun(new_one, j)
            if delta_fun > 0:
                all_delta_fun.append(delta_fun)
                if j != index:
                    if j not in self.subproblemi_BeimprovedBy_subproblemj:
                        self.subproblemi_BeimprovedBy_subproblemj[j] = {index: 1}
                    else:
                        if index not in self.subproblemi_BeimprovedBy_subproblemj[j]:
                            self.subproblemi_BeimprovedBy_subproblemj[j][index] = 1
                        else:
                            self.subproblemi_BeimprovedBy_subproblemj[j][index] += 1

                discard_ones.append([j, delta_fun])

        sum_delta_fun = sum(all_delta_fun) if len(all_delta_fun) > 0 else 0
        mean_delta_fun = sum(all_delta_fun) / len(all_delta_fun) if len(all_delta_fun) > 0 else 0
        max_delta_fun = max(all_delta_fun) if len(all_delta_fun) > 0 else 0
        real_delta_fun = 0

        if len(discard_ones) > 0:
            if 'MFI' in self.method_params['trick']:  #
                discard_ones.sort(reverse=True, key=lambda x: x[1])
            else:
                random.shuffle(discard_ones)
            index = discard_ones[0][0]
            if 'test_trick' in self.method_params and 'relative' in self.method_params['test_trick']:
                real_delta_fun += 1 - self.fun(new_one, index) / self.fun(self.pop[index], index)
            else:
                real_delta_fun += self.fun(self.pop[index], index) - self.fun(new_one, index)
            self.pop[index] = new_one
            self.pop_f1f2[index][0] = new_one.f1
            self.pop_f1f2[index][1] = new_one.f2

        if 'IGR' in self.method_params['trick']:
            discard_ones = []
            for j in range(pop_size):
                if self.unMatchedSub[j] == 0 and self.fun(new_one, j) < self.fun(self.pop[j], j):
                    discard_ones.append(j)
            random.shuffle(discard_ones)  #
            if len(discard_ones) > 0:
                index = discard_ones[0]
                if 'test_trick' in self.method_params and 'relative' in self.method_params['test_trick']:
                    real_delta_fun += 1 - self.fun(new_one, index) / self.fun(self.pop[index], index)
                else:
                    real_delta_fun += self.fun(self.pop[index], index) - self.fun(new_one, index)
                self.pop[index] = new_one
                self.pop_f1f2[index][0] = new_one.f1
                self.pop_f1f2[index][1] = new_one.f2

        # DRA/GRA
        if 'DRA' in self.method_params['trick'] or 'GRA' in self.method_params['trick']:
            tmp_delta = real_delta_fun
            if 'test_trick' in self.method_params:
                if 'mean' in self.method_params["test_trick"]:
                    tmp_delta = mean_delta_fun
                elif 'matchJ' in self.method_params["test_trick"]:
                    tmp_delta = matchJ_delta_fun
                elif 'sum' in self.method_params["test_trick"]:
                    tmp_delta = sum_delta_fun

            if index not in self.subproblemj_improve_others_delta:
                self.subproblemj_improve_others_delta[index] = [tmp_delta]
            elif len(self.subproblemj_improve_others_delta[index]) < self.method_params['delta_T']:
                self.subproblemj_improve_others_delta[index].append(tmp_delta)
            else:
                self.subproblemj_improve_others_delta[index].pop(0)
                self.subproblemj_improve_others_delta[index].append(tmp_delta)

    def run_one_moead(self, gen, selected_indices, select_rate, mutate_rate, mx_eval_num):
        keepN = []
        if 'GRA' in self.method_params['trick']:
            if len(self.choose_i) >= self.method_params['delta_T']:
                self.choose_i.pop(0)
            self.choose_i.append(selected_indices)
        self.gr_log = 0
        for i in selected_indices:
            if self.eval_num >= mx_eval_num:
                break
            new_sol = self.get_new_sol(i, select_rate, mutate_rate)
            res_truck_list, f1, f2 = self.evaluate.expensive_eval(new_sol)
            self.eval_num += 1
            self.subproblem_FEs[i] += 1
            if self.file_name in self.all_subproblem_FEs and self.eval_num in self.all_subproblem_FEs[
                self.file_name]:
                self.all_subproblem_FEs[self.file_name][self.eval_num] = copy.copy(self.subproblem_FEs)
            new_one = Individual(new_sol, f1, f2, res_truck_list)

            self.z_min = [min(new_one.f1, self.z_min[0]), min(new_one.f2, self.z_min[1])]
            self.z_max = [max(new_one.f1, self.z_max[0]), max(new_one.f2, self.z_max[1])]

            keepN.append([i, new_one])
            if 'N+N' in self.method_params['trick']:
                continue
            self.one_replace(i, new_one)
        if 'N+N' in self.method_params['trick']:
            for i, new_one in keepN:
                self.one_replace(i, new_one)
        self.gr_log_list.append(self.gr_log)

    def run_one_instance(self, i, file_name):
        data_params = self.data_params
        method_params = self.method_params
        pop_size = method_params['pop_size']
        select_rate = method_params.get("select_rate", None)
        mutate_rate = method_params['mutate_rate']
        mx_eval_num = method_params['mx_eval_num']
        mx_time = method_params['mx_time']

        input_dir = data_params['input_dir']
        output_dir = data_params['output_dir']
        # 记录一下每个文件花费的总时间
        self.logger.info('=================================================================')
        self.logger.info(f"File {i}: {file_name}")

        # 重置状态和evaluate
        self.reset(file_name)
        self.evaluate = Evaluate(input_dir, file_name)
        gens_f1f2 = []
        #  开始计时
        start = time.process_time()
        gen = 1  # init 算作一代
        # 初始化种群（moead）
        self.pop = get_init_pop(pop_size, self.visited_sols_dict, self.evaluate)
        now_f1f2, pre_pop = self.after_init_pop(gens_f1f2)
        use_time = time.process_time() - start
        self.logger.info("Gen {:5d}: Time: {:.3f},  Eval: {:5d},  LenEP: {:3d}".format(
            gen, use_time, self.eval_num, len(self.A)))
        pre_eval_num = self.eval_num
        gen += 1
        # 开始MOEAD的进化过程
        delta_T = self.method_params.get('delta_T',None)
        while use_time < mx_time and self.eval_num < mx_eval_num:
            selected_indices = self.before_run_one_moead(gen, pre_pop)
            self.run_one_moead(gen, selected_indices, select_rate, mutate_rate, mx_eval_num)
            # after run_one_moead
            self.A = get_no_domain_pop(self.A + self.pop)
            # 更新历代f1f2值 GRA
            if 'GRA' in self.method_params['trick']:
                for j in range(len(self.pop)):
                    f1_value = self.pop[j].f1
                    f2_value = self.pop[j].f2
                    MOEAD_MD.update_subproblem_values(self.subproblem_f1, j, f1_value, delta_T)
                    MOEAD_MD.update_subproblem_values(self.subproblem_f2, j, f2_value, delta_T)

            # logging
            use_time = time.process_time() - start
            if self.eval_num % 200 == 0 or self.eval_num >= mx_eval_num:
                gens_f1f2.append([[one.f1, one.f2] for one in self.pop])  # 添加一下中间种群的f1f2画图要用
            if 'GRA' in self.method_params['trick']:
                if self.eval_num - pre_eval_num >= 500:
                    pre_eval_num = self.eval_num
                    self.logger.info("Gen {:5d}: Time: {:.3f},  Eval: {:5d},  LenEP: {:3d}".format(
                        gen, use_time, self.eval_num, len(self.A)))
            else:
                if self.eval_num % 500 == 0:
                    self.logger.info("Gen {:5d}: Time: {:.3f},  Eval: {:5d},  LenEP: {:3d}".format(
                        gen, use_time, self.eval_num, len(self.A)))
            gen += 1

        use_time = time.process_time() - start
        self.result_log.append(f'use_time', i, use_time)
        self.logger.info("Gen {:5d}: Time: {:.3f},  Eval: {:5d},  LenEP: {:3d}".format(
            gen, use_time, self.eval_num, len(self.A)))

        self.max_u_equal0_count.append(self.now_max_u_equal0)
        self.instances_gens_f1f2[file_name] = gens_f1f2
        write_pareto(get_no_domain_pop(self.A), output_dir, file_name)
        return self.gr_log_list

    def after_init_pop(self, gens_f1f2):
        self.eval_num += self.method_params['pop_size']
        self.A = get_no_domain_pop(self.pop)
        now_f1f2 = [[one.f1, one.f2] for one in self.pop]
        self.pop_f1f2 = np.array(now_f1f2)
        gens_f1f2.append(now_f1f2)
        self.z_min = [min([one.f1 for one in self.pop]), min([one.f2 for one in self.pop])]
        self.z_max = [max([one.f1 for one in self.pop]), max([one.f2 for one in self.pop])]
        pre_pop = self.pop[:]
        # x in self.method_params['trick'] for x in ['IGR', 'GR']
        return now_f1f2, pre_pop

    def cal_spa(self):  # The Spa function of a sub problem
        spa = [-1 for _ in range(self.method_params['pop_size'])]
        all_x_k_index = [i for i in range(self.method_params['pop_size'])]
        # 对每个子问题先找到他对应的 optimal个体
        for k in range(self.method_params['pop_size']):
            x_k_index = all_x_k_index[k]
            mn_value = self.fun(self.pop[x_k_index], k)
            for index in range(self.method_params['pop_size']):
                now_value = self.fun(self.pop[index], k)
                if now_value < mn_value:
                    x_k_index = index
                    mn_value = now_value
            all_x_k_index[k] = x_k_index

        for k in range(self.method_params['pop_size']):
            x_k = self.pop[all_x_k_index[k]]
            for i in self.neighbors[k]: 
                if i == k:
                    continue
                x_i = self.pop[all_x_k_index[i]]
                tmp = ((x_k.f1 - x_i.f1) ** 2 + (x_k.f2 - x_i.f2) ** 2) ** 0.5
                spa[k] = tmp if spa[k] == -1 else min(tmp, spa[k])
        return spa

    def adjust_weight_vector(self, spa):
        sorted_indices = np.argsort(spa)
        index_of_min, index_of_max = sorted_indices[0], sorted_indices[-1]
        for m in range(2):
            self.ref_dirs[index_of_min][m] = (self.ref_dirs[index_of_min][m] + self.ref_dirs[index_of_max][m]) / 2

    def adjust_neighborhood_size(self, gen):
        gen_max = math.ceil(self.method_params['mx_eval_num'] / self.method_params['pop_size'])
        alpha = self.method_params['alpha']
        beta = self.method_params['beta']
        for i in range(self.method_params['pop_size']):
            self.ns_size[i] = max(2, int(self.ns_size[i] * (1 - alpha * (gen-1) / (gen_max-1))))
        self.re_get_neighbors()
        spa = self.cal_spa()
        if max(spa) != 0:
            for i in range(self.method_params['pop_size']):
                self.ns_size[i] = max(2, int(self.ns_size[i] * (1 - beta * spa[i] / max(spa))))
        self.re_get_neighbors()

    def re_get_neighbors(self):
        tmp = np.argsort(cdist(self.ref_dirs, self.ref_dirs), axis=1, kind='quicksort')
        if isinstance(self.neighbors, np.ndarray):
            self.neighbors = self.neighbors.tolist()
        for i in range(self.method_params['pop_size']):
            self.neighbors[i] = tmp[i][:self.ns_size[i]]

    def before_run_one_moead(self, gen, pre_pop):
        # 更新一下选择概率, 用于DRA选择个体
        delta_T = self.method_params.get('delta_T', None)
        pop_size = self.method_params['pop_size']

        if 'DRA' in self.method_params['trick']:
            if 'test_trick' not in self.method_params and gen % delta_T == 0:
                now_pop = self.pop[:]
                deltas = []
                for i in range(pop_size):
                    delta = self.fun(pre_pop[i], i) - self.fun(now_pop[i], i)
                    deltas.append(delta)
                    if delta < 0.005:
                        self.pi[i] *= (0.95 + 0.05 * (delta / 0.005))
                    # else:
                    #     self.pi[i] = 1
                pre_pop = now_pop
                # draw(np.array(deltas))  # 显示一下种群进化情况 # 会爆内存 别运行完了

            if 'test_trick' in self.method_params and self.method_params['test_trick'] == 'case1':
                if gen > delta_T:
                    for i in range(pop_size):
                        delta = sum(self.subproblemj_improve_others_delta[
                                        i]) if i in self.subproblemj_improve_others_delta else 0
                        if delta < 0.05:
                            self.pi[i] *= (0.95 + delta / 0.05)
                        else:
                            self.pi[i] = 1

            if 'test_trick' in self.method_params and self.method_params['test_trick'] == 'case2':
                if gen % delta_T == 0:
                    for i in range(pop_size):
                        delta = sum(self.subproblemj_improve_others_delta[
                                        i]) if i in self.subproblemj_improve_others_delta else 0
                        if delta < 0.05:
                            self.pi[i] *= (0.95 + delta / 0.05)
                        else:
                            self.pi[i] = 1

            if 'test_trick' in self.method_params and self.method_params['test_trick'] == 'case3':
                if gen % delta_T == 0:
                    for i in range(pop_size):
                        delta = sum(self.subproblemj_improve_others_delta[
                                        i]) if i in self.subproblemj_improve_others_delta else 0
                        if delta < 0.05:
                            self.pi[i] *= (0.95 + delta / 0.05)

        selected_indices = range(pop_size)
        if 'DRA' in self.method_params['trick']:
            now_pi = self.pi
            selected_indices = np.array(roulette_wheel_selection(now_pi, int(pop_size // 5)))
        if 'GRA' in self.method_params['trick']:
            delta_T = self.method_params['delta_T']
            selected_indices = []
            if len(self.subproblem_f1[0]) < delta_T:
                self.pi = [0.5 for _ in range(pop_size)]
            else:
                u = []
                lenS = [MOEAD_MD.count_occurrences(i, self.choose_i) for i in range(pop_size)]
                for i in range(pop_size):
                    if 'test_trick' in self.method_params:
                        if 'matchV' in self.method_params['test_trick']:
                            if 'sumT' in self.method_params['test_trick']:
                                u.append(sum(self.subproblemj_improve_others_delta[
                                                 i]) if i in self.subproblemj_improve_others_delta else 0)
                            elif 'meanT' in self.method_params['test_trick']:
                                if i not in self.subproblemj_improve_others_delta:
                                    u.append(0)
                                else:
                                    tmp = self.subproblemj_improve_others_delta[i]
                                    u.append(sum(tmp) / len(tmp) if len(tmp) > 0 else 0)

                            elif 'meanS' in self.method_params['test_trick'] or 'meanSV2' in self.method_params[
                                'test_trick']:
                                if i not in self.subproblemj_improve_others_delta or lenS[i] == 0:
                                    u.append(0)
                                else:
                                    u.append(sum(self.subproblemj_improve_others_delta[i]) / lenS[i])

                        elif 'paperV' in self.method_params['test_trick']:
                            g_t_minus_delta = self.fun([self.subproblem_f1[i][0], self.subproblem_f2[i][0]], i,
                                                       self.ref_dirs, self.z_min, self.z_max)
                            g_t = self.fun([self.subproblem_f1[i][-1], self.subproblem_f2[i][-1]], i, self.ref_dirs,
                                           self.z_min, self.z_max)
                            u_i = (g_t_minus_delta - g_t) / g_t_minus_delta
                            u.append(u_i)
                max_u = max(u)
                if max_u == 0:
                    self.now_max_u_equal0 += 1
                    self.pi = [1 for _ in range(pop_size)]
                else:
                    bias = 0
                    pre_pi = copy.copy(self.pi)
                    if 'test_trick' in self.method_params:
                        if 'attenuate' in self.method_params['test_trick']:
                            self.pi = [pre_pi * (0.95 + 0.05 * u_i) for u_i, pre_pi in zip(u, pre_pi)]
                        elif 'bias' in self.method_params['test_trick']:
                            bias = self.method_params['bias']

                        self.pi = [(bias + (1 - bias) * (u_i / max_u)) for u_i in u]

                        if 'meanSV2' in self.method_params['test_trick']:
                            for i, lenS_i in enumerate(lenS):
                                if lenS_i == 0:
                                    self.pi[i] = pre_pi[i]

            for i in range(pop_size):
                random_number = random.random()
                if random_number <= self.pi[i]:
                    selected_indices.append(i)
        return selected_indices


    def get_p1_p2(self, i: int, select_rate):
        pop = self.pop
        ep = self.A
        ns = self.neighbors
        p1 = pop[i]
        if random.random() < select_rate or len(ep) == 0:
            index_p2 = random.sample(ns[i].tolist(), 1)[0]
            tag = 1000
            while index_p2 == i and tag > 0:
                index_p2 = random.sample(ns[i].tolist(), 1)[0]
                tag -= 1
            p2 = pop[index_p2]
        else:
            p2 = random.sample(ep, 1)[0]
        return p1, p2
