import os
import json


def join_path(*args):
    return os.path.join(*args)


def read_input_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        message_str = f.read()
    return json.loads(message_str)


def write_output_file(data, file_path):
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def write_pareto(pareto, output_dir, file_name):
    ans = {"estimateCode": file_name, "solutionArray": []}
    for one in pareto:
        ans["solutionArray"].append(one.res_truck_list)
    write_output_file(ans, join_path(output_dir, file_name))
