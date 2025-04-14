import uuid as UUID
# 处理数据
def get_platform_box(box_list):
    platform_box = {}
    for box in box_list:
        if box['platformCode'] not in platform_box:
            platform_box[box['platformCode']] = []
        # 增加一个key值,因为spuID不是唯一的
        box['uuid'] = UUID.uuid4()
        platform_box[box['platformCode']].append(box)
    return platform_box


def get_size_box(box_list):
    size_box = {}
    for box in box_list:
        sizes = [(box["length"], box["width"], box["height"])]
        if box["length"] != box["width"]:
            sizes.append((box["width"], box["length"], box["height"]))
        for size in sizes:
            if size not in size_box:
                size_box[size] = []
            size_box[size].append(box)
    return size_box


def get_platform_info(data):
    platfrom_list = []
    must_visted_dict = {}

    for x in data["algorithmBaseParamDto"]['platformDtoList']:
        platfrom_list.append(x['platformCode'])
        must_visted_dict[x['platformCode']] = x['mustFirst']
    return platfrom_list, must_visted_dict


from MOEAD_MD.packing import TruckType


def get_truck_type_info(data):
    return [TruckType(raw_truckType["truckTypeId"],
                      raw_truckType["truckTypeCode"],
                      raw_truckType["truckTypeName"],
                      raw_truckType["length"],
                      raw_truckType["width"],
                      raw_truckType["height"],
                      raw_truckType["maxLoad"]
                      ) for raw_truckType in data['algorithmBaseParamDto']['truckTypeDtoList']]


def turn_truck_to_ans_dict(truck_list):
    ans_truck_list = []
    for truck in truck_list:
        ans_truck = {"truckTypeId": truck.truck_type.truckTypeId, "truckTypeCode": truck.truck_type.truckTypeCode,
                     "piece": 0, "volume": 0, "weight": 0, "innerLength": truck.truck_type.length,
                     "innerWidth": truck.truck_type.width, "innerHeight": truck.truck_type.height,
                     "maxLoadWeight": truck.truck_type.maxLoad, "platformArray": truck.visited_platform, "spuArray": []}

        order = 1
        for block, space in zip(truck.block_list, truck.used_space_list):
            ans_truck["piece"] += len(block.box_list)
            ans_truck["volume"] += space.lx * space.ly * space.lz
            ans_truck["weight"] += block.sum_weight
            for i, box in enumerate(block.box_list):
                ans_box = {**box, "direction": 100 if box["length"] == block.unit_size[0] else 200}
                x = space.x + (i % (block.stack_count_xyz[0] * block.stack_count_xyz[1])) // block.stack_count_xyz[1] * \
                    block.unit_size[0]
                y = space.y + i % block.stack_count_xyz[1] * block.unit_size[1]
                z = space.z + i // (block.stack_count_xyz[0] * block.stack_count_xyz[1]) * block.unit_size[2]
                ans_box["x"] = x - ans_truck["innerLength"] / 2 + block.unit_size[0] / 2
                ans_box["y"] = y - ans_truck["innerWidth"] / 2 + block.unit_size[1] / 2
                ans_box["z"] = z - ans_truck["innerHeight"] / 2 + block.unit_size[2] / 2
                ans_box["x"], ans_box["y"], ans_box["z"] = ans_box["y"], ans_box["z"], ans_box["x"]
                ans_box["order"] = order
                order += 1
                # 输入和输出的box的ID的代称不一样
                ans_box["spuId"] = ans_box.pop("spuBoxId")
                # 存文件的时候要删掉uuid
                del ans_box['uuid']
                ans_truck["spuArray"].append(ans_box)
        ans_truck_list.append(ans_truck)
    return ans_truck_list
