from logging import getLogger
from scipy.spatial.distance import cdist
from pymoo.util.reference_direction import UniformReferenceDirectionFactory


from utils.utils import *
from utils.moead_utils import *
from utils.getHV_utils import *
from global_var import *

class MOEAD_MD_BASE():

    def __init__(self, method_params, data_params):
        # save arguments
        self.method_params = method_params[method_params["method_name"] + "_params"]
        self.data_params = data_params

        # result folder, logger
        self.logger = getLogger(name='trainer')
        self.result_folder = get_result_folder()
        self.result_log = LogData()

        # Main Components
        self.pop = []
        self.pop_f1f2 = []
        self.eval_num = 0
        self.A = []
        self.visited_sols_dict = {}
        self.pi = []  # MOEAD-DRA/GRA
        self.fun = self.get_func()

        self.ref_dirs = UniformReferenceDirectionFactory(2, n_partitions=self.method_params['pop_size'] - 1).do()
        self.all_sort_rank = np.argsort(cdist(self.ref_dirs, self.ref_dirs), axis=1, kind='quicksort')
        self.T_r = None
        self.neighbors = self.all_sort_rank[:, :self.method_params['ns_size']]

        self.z_min = []
        self.z_max = []
        self.evaluate = None
        self.unMatchedSub = [0 for _ in range(self.method_params['pop_size'])]
        self.deltas_for_ls = []
        self.gr_log_list = []  # 存储每一代gr可执行的次数
        self.Subproblemi_BeimprovedBy_subproblemj = {}  # i 被 subProblem j的解 提升过
        self.subproblemj_improve_others_delta = {}  # 保留前5代的improve的列表
        self.subproblem_g = []  # 每个子问题i最近delta_T代的子问题value值
        self.max_u_equal0_count = []  # 存储所有instance max_u_equal0的次数
        self.now_max_u_equal0 = 0  # 当前instance max_u_equal0的次数
        self.subproblem_FEs = []  # 当前instance累计FE次数
        self.all_subproblem_FEs = {}  # 记录一下特定次数时候的FE次数
        self.file_name = None  # 当前file_name
        self.choose_i = []  # 最近delta T 选择的子问题
        self.ns_size = []  # 所有子问题的邻域大小
        self.rf_point_tag = 0

    def reset(self, file_name):
        self.file_name = file_name
        self.subproblem_FEs = [0 for _ in range(self.method_params['pop_size'])]
        # 处理下一个file
        self.pop = []
        self.pop_f1f2 = []  # 用来做kmeans的
        self.eval_num = 0
        self.A = []

        self.visited_sols_dict = {}
        self.pi = [1 for _ in range(self.method_params['pop_size'])]  # MOEAD-DRA
        self.unMatchedSub = [0 for _ in range(self.method_params['pop_size'])]
        self.z_min = []
        self.z_max = []
        self.evaluate = None
        self.deltas_for_ls = []
        self.gr_log = 0  # 当前累计的gr_log
        self.gr_log_list = []  # 每代记录一次
        self.subproblemi_BeimprovedBy_subproblemj = {}
        self.subproblemj_improve_others_delta = {}
        self.subproblem_g = [[] for _ in range(self.method_params['pop_size'])]
        self.subproblem_f1 = [[] for _ in range(self.method_params['pop_size'])]
        self.subproblem_f2 = [[] for _ in range(self.method_params['pop_size'])]
        self.now_max_u_equal0 = 0
        self.choose_i = []  # 最近delta T 选择的子问题
        self.ns_size = [self.method_params['ns_size'] for i in range(self.method_params['pop_size'])]  # 所有子问题的邻域大小
        self.rf_point_tag=0

    @staticmethod
    def count_occurrences(target, nested_list):
        count = 0
        for sublist in nested_list:
            count += sublist.count(target)
        return count

    @staticmethod
    def update_subproblem_values(subproblem_values, index, value, delta_T):
        if len(subproblem_values[index]) < delta_T:
            subproblem_values[index].append(value)
        else:
            subproblem_values[index].pop(0)
            subproblem_values[index].append(value)

    def run(self, test=False):
        data_params = self.data_params
        method_params = self.method_params
        mx_eval_num = method_params['mx_eval_num']

        input_dir = data_params['input_dir']
        output_dir = data_params['output_dir']

        # 
        total_start = time.process_time()
        file_names = os.listdir(input_dir)
        self.instances_gens_f1f2 = {instance: [] for instance in file_names}
        total_gr_log_list = {}
        if test:
            file_names = ["E1597884759924", "E1597283167355", "E1598317160241"]
            self.all_subproblem_FEs = {file: {500: [], 1000: [], 1500: [], 2000: []} for file in file_names}

        for i, file_name in enumerate(file_names):
            gener_use_times.clear()
            eval_use_times.clear()
            init_use_times.clear()
            gr_log_list = self.run_one_instance(i, file_name)
            total_gr_log_list[file_name] = gr_log_list
            list_init_use_times.append(np.mean(init_use_times))
            list_eval_use_times.append(np.mean(eval_use_times))
            list_gener_use_times.append(np.mean(gener_use_times))

        if test:
            with open('new_subproblem_FEs.json', 'w') as f:
                json.dump(self.all_subproblem_FEs, f)
        all_time = time.process_time() - total_start
        self.logger.info(" *** All Done *** ")
        if len(self.max_u_equal0_count) > 0:
            self.logger.info(f"{self.max_u_equal0_count}")
        self.logger.info("Now, printing log array...")
        util_print_log_array(self.logger, self.result_log)
        self.logger.info('Total Time: {:.3f}, Eval: {:5d}'.format(all_time, mx_eval_num))
        self.logger.info(f'{output_dir}')

        self.logger.info('=================================================================')
        self.logger.info('Now, calculate HV value...')
        start = time.time()
        # HV
        all_output_dir = self.data_params['output_dir'].split('/')
        output_name = all_output_dir.pop()
        all_output_dir = os.sep.join(all_output_dir)
        F1F2s, all_nondomain_f1f2 = printHV(self.data_params['input_dir'], all_output_dir, self.logger)
        self.logger.info('Total Time: {:.3f}'.format(time.time() - start))
        self.logger.info('=================================================================')

        return total_gr_log_list

    def get_func(self):
        def wrapper(one, index):
            fun_dict = {
                'gTe': gTe,
                'gWs': gWs,
                'gPBI': gPBI
            }
            func = fun_dict[self.method_params['fun']]
            return func(one, index, self.ref_dirs, self.z_min, self.z_max, self.rf_point_tag)
        return wrapper

