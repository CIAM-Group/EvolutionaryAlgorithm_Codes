import numpy as np
import time
from Benchmarks.MVOP import MVOPT
from Algorithm.My_CEEO import CEEO
from Application.ParamOP import TPLeNet5
import os
import warnings
import torch
warnings.filterwarnings('ignore')

def assign_gpu(gpu=None):
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu)
    os.environ['TF_ENABLE_WINOGRAD_NONFUSED'] = '1'
def run_benchmark(pname, maxFEs, trials):

    problem = TPLeNet5(10)

    # problem = TPLeNet5(10)


    save_y_best = np.zeros(trials)
    save_c_reslut = np.zeros((maxFEs,trials))
    start_time = time.time()
    for i in range(trials):
        print("Running trial: ", i)

        problem2 = MVOPT(fun_name, problem.r, problem.dim - problem.r)
        opt = CEEO(maxFEs=maxFEs, popsize=100, dim=problem.dim, clb=problem.bounds[0],
                      cub=problem.bounds[1], N_lst=problem.N_lst, v_dv=problem2.v_dv, prob=problem.F,
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
        # index = np.argsort(save_c_reslut[jj, :])
        median_result_cov[jj] = np.median(save_c_reslut[jj, :])

    last_value = [mean_value, std_value, np.min(median_result_cov), time_cost]
    # cov_curve = np.mean(save_c_reslut, axis=1)
    cov_curve = np.zeros((maxFEs, trials+1))
    cov_curve[:, 0:trials] = save_c_reslut
    cov_curve[:, trials] = np.mean(save_c_reslut, axis=1)

    np.savetxt('./result/%s.txt' % fun_name, last_value) # 均值与方差
    np.savetxt('./result/%s_Convergence curve.txt' % fun_name, cov_curve)

    print("optimum on {}:{}".format(fun_name, y_best))


if __name__ == "__main__":
    assign_gpu(gpu=0)
    np.seterr(divide='ignore', invalid='ignore')
    torch.autograd.set_detect_anomaly(False)
    torch.autograd.profiler.profile(False)
    torch.autograd.profiler.emit_nvtx(False)

    K = 1

    maxFEs = 300
    trials = 5
    fun_name = 'TPLeNet5'
    # fun_name = 'TPAlexNet'


    run_benchmark(fun_name, maxFEs, trials)
