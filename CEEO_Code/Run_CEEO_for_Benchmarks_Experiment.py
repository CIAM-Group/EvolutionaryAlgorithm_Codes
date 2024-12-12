import numpy as np
import time
from Benchmarks.MVOP import MVOPT
from Algorithm.My_CEEO import CEEO
import os
import warnings

warnings.filterwarnings('ignore')


def run_benchmark(pname, n_c, n_d, maxFEs, trials):


    save_y_best = np.zeros(trials)
    save_c_reslut = np.zeros((maxFEs,trials))
    start_time = time.time()
    for i in range(trials):
        print("Running trial: ", i)
        problem = MVOPT(pname, n_c, n_d)
        opt = CEEO(maxFEs=maxFEs, popsize=100, dim=problem.dim, clb=[problem.bounds[0]] * problem.r,
                      cub=[problem.bounds[1]] * problem.r, N_lst=problem.N_lst, v_dv=problem.v_dv, prob=problem.F,
                      r=problem.r)
        x_best, y_best, y_lst, database, melst, c_result = opt.run()
        save_y_best[i] = y_best
        index = min(maxFEs, len(c_result))
        save_c_reslut[:index, i] = c_result[:index]
    end_time = time.time()
    os.makedirs('./result', exist_ok=True)
    mean_value = np.mean(save_y_best)
    std_value = np.std(save_y_best)
    time_cost = end_time - start_time
    median_result_cov = np.zeros(maxFEs)
    for jj in range(maxFEs):

        median_result_cov[jj] = np.median(save_c_reslut[jj, :])

    last_value = [mean_value, std_value, np.min(median_result_cov), time_cost]

    cov_curve = np.zeros((maxFEs, trials+1))
    cov_curve[:, 0:trials] = save_c_reslut
    cov_curve[:, trials] = np.mean(save_c_reslut, axis=1)

    np.savetxt('./result/%s.txt' % pname, last_value) # 均值与方差
    np.savetxt('./result/%s_Convergence curve.txt' % pname, cov_curve)

    print("optimum on {}:{}".format(pname, y_best))


if __name__ == "__main__":

    total = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
             'F11', 'F12', 'F13', 'F14', 'F15',
             'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24',
             'F25', 'F26', 'F27', 'F28', 'F29', 'F30']

    trials = 20
    pop = 100
    maxFEs = 600
    for i in range(0, 30):
        fun_name = total[i]

        if total[i] in ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"]:
           n_c = 8
           n_d = 2
        elif total[i] in ["F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F19", "F20"]:
            n_c = 2
            n_d = 8
        elif total[i] in ["F21", "F22", "F23", "F24", "F25", "F26", "F27", "F28", "F29", "F30"]:
            n_c = 5
            n_d = 5
        run_benchmark(fun_name, n_c, n_d, maxFEs, trials)
