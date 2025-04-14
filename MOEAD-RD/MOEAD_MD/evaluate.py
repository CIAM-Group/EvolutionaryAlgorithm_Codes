import os
import random
import time
import joblib
import numpy as np

from MOEAD_MD.routing import get_sub_sol
from MOEAD_MD.packing import route_packing
from MOEAD_MD.my_io import join_path, read_input_file
from MOEAD_MD.process_data import get_platform_info, get_truck_type_info, turn_truck_to_ans_dict, get_platform_box
from utils.moead_utils import time_count_hooks

class DotDict(dict):
    def __init__(self, **kwargs):
        super().__init__()
        self.update(kwargs)
        self.__dict__ = self


class Evaluate:
    def __init__(self, input_dir, file_name):
        self.input_dir = input_dir
        self.file_name = file_name
        self.init_data(input_dir, file_name)

    def init_data(self, input_dir, file_name):
        data = read_input_file(join_path(input_dir, file_name))
        platform_list, must_visited_dict = get_platform_info(data)
        platform_box = get_platform_box(data['boxes'])
        truck_type_list = sorted(get_truck_type_info(data), key=lambda x: x.volume, reverse=True)
        distance_map = data["algorithmBaseParamDto"]["distanceMap"]

        self.data = data
        self.platform_list = platform_list
        self.must_visited_dict = must_visited_dict
        self.platform_box = platform_box
        self.truck_type_list = truck_type_list

        self.raw_distance_map = distance_map
        self.distance_map = {(key.split('+')[0], key.split('+')[1]): distance_map[key] for key in distance_map}

    def get_random_sol(self):
        sol = self.platform_list[:]
        random.shuffle(sol)
        return sol

    def get_loading_rate(self, truck):
        space_rate = truck.sum_used_space / (truck.truck_type.height * truck.truck_type.width * truck.truck_type.length)
        weight_rate = 1 - truck.left_weight / truck.truck_type.maxLoad
        return max(space_rate, weight_rate)

    def get_distance(self, truck, distance_map=None):
        if distance_map is None:
            distance_map = self.distance_map
        distance = distance_map["start_point", truck.visited_platform[0]] + distance_map[
            truck.visited_platform[-1], "end_point"]
        for i in range(len(truck.visited_platform) - 1):
            distance += distance_map[truck.visited_platform[i], truck.visited_platform[i + 1]]
        return distance

    def get_loading_rate_by_res_truck_list(self, res_truck_list):
        def get_loading_rate_by_res_truck(truck):
            space_rate = truck["volume"] / (truck["innerLength"] * truck["innerWidth"] * truck["innerHeight"])
            if "maxLoad" in truck:
                weight_rate = truck["weight"] / truck["maxLoad"]
            else:
                weight_rate = truck["weight"] / truck["maxLoadWeight"]
            return max(space_rate, weight_rate)

        loading_rate_list = [get_loading_rate_by_res_truck(truck) for truck in res_truck_list]
        f1 = 1 - sum(loading_rate_list) / len(loading_rate_list)
        return f1

    def get_distance_by_res_truck_list(self, res_truck_list, distance_map=None):
        def get_distance_by_res_truck(truck, distance_map=None):
            if distance_map is None:
                distance_map = self.distance_map
            distance = distance_map["start_point", truck["platformArray"][0]] + distance_map[
                truck["platformArray"][-1], "end_point"]
            for i in range(len(truck["platformArray"]) - 1):
                distance += distance_map[truck["platformArray"][i], truck["platformArray"][i + 1]]
            return distance

        distance_list = [get_distance_by_res_truck(truck, distance_map) for truck in res_truck_list]
        f2 = sum(distance_list)
        return f2

    @time_count_hooks
    def expensive_eval(self, sol, must_visited_dict=None, truck_type_list=None, platform_box=None, distance_map=None):
        start_time = time.time()
        if must_visited_dict is None:
            must_visited_dict = self.must_visited_dict
        if truck_type_list is None:
            truck_type_list = self.truck_type_list
        if platform_box is None:
            platform_box = self.platform_box
        if distance_map is None:
            distance_map = self.distance_map

        sub_sols = get_sub_sol(sol, must_visited_dict)

        res_truck_list_f1_f2_list = []
        # my_pack
        truck_list = []
        for sub_sol in sub_sols:
            used_truck_list = route_packing(sub_sol, truck_type_list, platform_box)
            truck_list.extend(used_truck_list)
        res_truck_list = turn_truck_to_ans_dict(truck_list)
        f1 = self.get_loading_rate_by_res_truck_list(res_truck_list)
        f2 = self.get_distance_by_res_truck_list(res_truck_list, distance_map)
        use_time = [time.time()-start_time]
        return use_time, res_truck_list, f1, f2
        # return res_truck_list, f1, f2

    def greedy_eval(self, sol, logger=None):
        def try_small_truck(last_truck):
            for truck_type in reversed(self.truck_type_list[1:]):
                if truck_type.volume > last_truck.sum_used_space \
                        and truck_type.maxLoad > last_truck.truck_type.maxLoad - last_truck.left_weight:
                    tmp_sum_used_space = last_truck.sum_used_space
                    tmp_left_weight = truck_type.maxLoad - (last_truck.truck_type.maxLoad - last_truck.left_weight)
                    tmp_visited_platform = last_truck.visited_platform
                    last_truck = LoadingTruck(truck_type)
                    last_truck.sum_used_space = tmp_sum_used_space
                    last_truck.left_weight = tmp_left_weight
                    last_truck.visited_platform = tmp_visited_platform
                    return last_truck
            return last_truck
        from MOEAD_MD.packing import LoadingTruck
        last_truck = LoadingTruck(self.truck_type_list[0])
        use_truck_list = []
        for platform in sol:
            box_list = self.platform_box[platform]
            box_list = sorted(box_list, key=lambda one:
            one['length'] * one['width'] * one['height'])  # 后面可以换成先装大的试试
            for box in box_list:
                box_volume = box['length'] * box['width'] * box['height']
                if not (box['weight'] < last_truck.left_weight \
                        and box_volume + last_truck.sum_used_space < last_truck.truck_type.volume):
                    use_truck_list.append(try_small_truck(last_truck))
                    last_truck = LoadingTruck(self.truck_type_list[0])
                last_truck.sum_used_space += box_volume
                last_truck.left_weight -= box['weight']
                if len(last_truck.visited_platform) == 0 or last_truck.visited_platform[-1] != platform:
                    last_truck.visited_platform.append(platform)

        if last_truck is not None:
            use_truck_list.append(try_small_truck(last_truck))

        loading_rate_list = [self.get_loading_rate(truck) for truck in use_truck_list]
        f1 = 1 - sum(loading_rate_list) / len(loading_rate_list)
        distance_list = [self.get_distance(truck) for truck in use_truck_list]
        f2 = sum(distance_list)
        return f1, f2
