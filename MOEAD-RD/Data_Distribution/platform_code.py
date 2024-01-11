import re
import os
from MOEAD_MD.my_io import join_path, read_input_file
from MOEAD_MD.process_data import get_platform_info, get_truck_type_info, get_platform_box

def get_platform_code(input_dir):
    file_names = os.listdir(input_dir)
    for file_name in file_names:
        data = read_input_file(join_path(input_dir, file_name))
        platform_list, must_visited_dict = get_platform_info(data)
        # Use regular expressions to extract the digits from each string in platform_list
        platform_digits = [int(re.findall(r'\d+', platform)[0]) for platform in platform_list]
        if any(num > 99 for num in platform_digits):
            print("no")
get_platform_code('../data/inputs250')