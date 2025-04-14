##########################################################################################
# parameters
method_params = {
    'method_name': "moead",  # "moead" "nsga2",
    'moead_params': {
        'method_name': 'moead',
        'pop_size': 75,
        'ns_size': 5,
        'select_rate': 0.6,
        'mutate_rate': 0.3,
        'mx_eval_num': 2000,
        'mx_time': 1000,  # 单位s
        'fun': 'gTe',  # 'gWs'
        'trick': [],  # 'IGR', 'MFI', 'DRA', 'N+N'
        'test_trick': [],  # 'bias0.1', 'relative', 'real'/'mean'/'matchJ/sum', 'sumT'/'meanT'/'meanS/meanSV2', 'deltaT5'
        'gr_rate': 1,
        'delta_T': 5,
        'bias': 0
    }
}
output_name = ""

data_params = {
    'input_dir': './data/inputs250',
    'output_dir': f'./all_data/outputs250/{output_name}',
}

logger_params = {
    'log_file': {
        'desc': f'{output_name}',  # f'{output_name}_{model_pk_name}'
        'filename': 'run_log'
    }
}

##########################################################################################
# main
import re
import sys
import logging
from utils.utils import create_logger, copy_all_src, get_result_folder
from MOEAD_MD.moead_md import MOEAD_MD

def main():
    # 第一个参数是编号
    # 第二个参数是ns_size
    method_params['moead_params']['ns_size'] = sys.argv[2]
    output_name = f'MOEAD_IGRCount_ns{sys.argv[2]}_no{sys.argv[1]}'
    data_params['output_dir'] = f'./all_data/outputs250/{output_name}'
    logger_params['log_file']['desc'] = f'{output_name}'

    create_logger(**logger_params)
    _print_config()

    copy_all_src(get_result_folder())
    # 执行算法
    moead_md = MOEAD_MD(method_params=method_params,
                        data_params=data_params)
    moead_md.run()

def _print_config():
    logger = logging.getLogger('root')
    [logger.info(g_key + "{}".format(globals()[g_key])) for g_key in globals().keys() if g_key.endswith('params')]


if __name__ == '__main__':
    main()
