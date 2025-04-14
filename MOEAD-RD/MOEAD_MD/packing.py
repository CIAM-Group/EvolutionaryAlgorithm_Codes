# packing
SUPPORT_RATIO = 0.8
BEYOND_BETA = 150


class TruckType:
    def __init__(self, truckTypeId, truckTypeCode, truckTypeName, length, width, height, maxLoad):
        self.__dict__.update({k: v for k, v in locals().items() if k != 'self'})
        self.volume = length * width * height


class Space:
    def __init__(self, x, y, z, lx, ly, lz):
        self.__dict__.update({k: v for k, v in locals().items() if k != 'self'})

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and \
               self.lx == other.lx and self.ly == other.ly and self.lz == other.lz

    def __lt__(self, other):
        def spaces_corner_sum(space):
            return space.x + space.y + space.z  # 选空间的规则

        def space_xyz(space):
            return space.x, space.y, space.z

        def space_xyz_2(space):
            return space.x, space.y, space.z, -(space.lx * space.ly * space.lz)

        return space_xyz(self) < space_xyz(other)


class LoadingTruck:
    def __init__(self, truck_type):
        self.truck_type = truck_type
        self.free_space_list = [
            Space(0, 0, 0, self.truck_type.length, self.truck_type.width, self.truck_type.height)]
        self.discard_space_list = []  # [Space]
        self.used_space_list = []  # [Space] 对应block_list中block使用的空间
        self.block_list = []  # [Block]
        self.left_weight = self.truck_type.maxLoad
        self.visited_platform = []  # 为了求PF方便以及写入数据方便
        self.sum_used_space = 0  # 总使用体积
        self.box_list = []  # 为了换小车的


class Block:
    def __init__(self, stack_count_xyz, unit_size, sum_weight, box_list):
        self.__dict__.update({k: v for k, v in locals().items() if k != 'self'})
        self.volume = unit_size[0] * stack_count_xyz[0] * \
                      unit_size[1] * stack_count_xyz[1] * \
                      unit_size[2] * stack_count_xyz[2]

    def __gt__(self, other):
        return (self.volume, self.unit_size[1]) > (other.volume, other.unit_size[1])


def get_block_list(space, size_box, left_weight, used_space_list, truck_type):
    block_list1 = []
    filter_size_box = filter(lambda one: one[0] <= space.lx and one[1] <= space.ly and one[2] <= space.lz, size_box)
    for size in filter_size_box:
        box_list = size_box[size]
        # 按照现在的box顺序,最多可以放下多少箱子的重量
        pre_sum_weigt = []
        for max_num, box in enumerate(box_list):
            pre_sum_weigt.append(box["weight"] + (pre_sum_weigt[max_num - 1] if max_num > 0 else 0))
            if left_weight < pre_sum_weigt[-1]:
                break
        else:
            max_num = len(box_list)
        # 空间约束
        nx, ny, nz = int(space.lx / size[0]), int(space.ly / size[1]), int(space.lz / size[2])
        if max_num <= ny:
            ny = max_num
            nz = nx = 1
        elif max_num <= ny * nz:
            nz = int(max_num / ny)
            nx = 1
        elif max_num <= nx * ny * nz:
            nx = int(max_num / (ny * nz))
        if nx * ny * nz > 0:
            block_list1.append(Block((nx, ny, nz), size, pre_sum_weigt[nx * ny * nz - 1], box_list[:nx * ny * nz]))
    block_list2 = []
    # 再次遍历所有size, 寻找超大快 #发现之前的代码的一个bug，没判断超出车厢
    # 否定条件是 lz 超过 lz, 或者超出车厢，或者完全被包住
    filter_size_box = filter(lambda one: not (one[2] > space.lz or space.x + one[0] > truck_type.length or
                                              space.y + one[1] > truck_type.width or
                                              (one[0] <= space.lx and one[1] <= space.ly)), size_box)
    for size in filter_size_box:
        box_list = size_box[size][:]
        box_list.sort(key=lambda x: x["weight"], reverse=True)
        # weight 和 space约束
        if box_list[0]["weight"] <= left_weight and \
                size[0] - space.lx < BEYOND_BETA and space.lx / size[0] > SUPPORT_RATIO and \
                size[1] - space.ly < BEYOND_BETA and space.ly / size[1] > SUPPORT_RATIO and \
                (min(size[0], space.lx) * min(size[1], space.ly)) / (size[0] * size[1]) > SUPPORT_RATIO:
            # 判断与其他已用空间有没有遮挡以及重叠
            now_space = Space(space.x, space.y, space.z, size[0], size[1], size[2])
            is_ok = True
            for used_space in used_space_list:
                if check_overlap_3d(now_space, used_space) or (
                        used_space.x > now_space.x and check_overlap_2d(now_space, used_space)):
                    is_ok = False
                    break
            if is_ok:
                block_list2.append(Block((1, 1, 1), size, box_list[0]["weight"], [box_list[0]]))
    return block_list1, block_list2




# import numba
# @numba.jit()
def get_overlap_space(space1, space2):
    # 求两个空间的交集(可能交集不存在，此时对应轴长<=0)
    overlap_space = dict(x=max(space1.x, space2.x), y=max(space1.y, space2.y), z=max(space1.z, space2.z),
                         lx=max(min(space1.x + space1.lx, space2.x + space2.lx) - max(space1.x, space2.x), 0),
                         ly=max(min(space1.y + space1.ly, space2.y + space2.ly) - max(space1.y, space2.y), 0),
                         lz=max(min(space1.z + space1.lz, space2.z + space2.lz) - max(space1.z, space2.z), 0))
    return overlap_space


def check_overlap_3d(space1, space2):
    return not (space1.x >= space2.x + space2.lx or space1.x + space1.lx <= space2.x or
                space1.y >= space2.y + space2.ly or space1.y + space1.ly <= space2.y or
                space1.z >= space2.z + space2.lz or space1.z + space1.lz <= space2.z)


def check_overlap_2d(space1, space2):
    return not (space1.y >= space2.y + space2.ly or space1.y + space1.ly <= space2.y or \
                space1.z >= space2.z + space2.lz or space1.z + space1.lz <= space2.z)


def update_space_list_by_block_space(block_space, space_list):
    updated_space_list = []
    for pre_space in space_list:
        if check_overlap_3d(block_space, pre_space):
            deltaY = block_space.y + block_space.ly - pre_space.y
            deltaX = block_space.x + block_space.lx - pre_space.x
            if deltaY < min(BEYOND_BETA, block_space.ly / SUPPORT_RATIO - block_space.ly):
                tmpLy = pre_space.ly - deltaY
                pre_space.ly = tmpLy
                pre_space.y = block_space.y + block_space.ly

            if deltaX < min(BEYOND_BETA, block_space.lx / SUPPORT_RATIO - block_space.lx):
                tmpLx = pre_space.lx - deltaX
                pre_space.lx = tmpLx
                pre_space.x = block_space.x + block_space.lx

            if pre_space.ly <= 0 or pre_space.lx <= 0:
                continue
        if pre_space.x < block_space.x and check_overlap_2d(block_space, pre_space):
            deltaY = block_space.y + block_space.ly - pre_space.y
            tmpLy = pre_space.ly - deltaY
            pre_space.ly = tmpLy
            pre_space.y = block_space.y + block_space.ly

        if pre_space.ly > 0 and pre_space.lx > 0:
            updated_space_list.append(pre_space)
    return updated_space_list


def get_refresh_spaces(block_space, discard_space_list):
    refresh_spaces_list = []
    for space in discard_space_list:
        if check_overlap_2d(block_space, space):
            space.ly = space.ly - (block_space.y + block_space.ly - space.y)
            space.y = block_space.y + block_space.ly
            if space.ly > 0:
                refresh_spaces_list.append(space)
    discard_space_list = filter(lambda space: space.ly > 0, discard_space_list)
    return refresh_spaces_list, discard_space_list


def update_info(loading_truck, size_box, space, block):
    if len(loading_truck.visited_platform) == 0 or loading_truck.visited_platform[-1] != block.box_list[0][
        "platformCode"]:
        loading_truck.visited_platform.append(block.box_list[0]["platformCode"])
    # 更新装载的箱子列表
    loading_truck.box_list.extend(block.box_list)
    # 车辆存上block
    loading_truck.block_list.append(block)
    # 更新车辆已用空间
    block_space = Space(space.x, space.y, space.z,
                        *tuple(x * y for x, y in zip(block.unit_size, block.stack_count_xyz)))
    loading_truck.used_space_list.append(block_space)
    loading_truck.sum_used_space += block_space.lx * block_space.ly * block_space.lz
    # 更新剩余可装载重量
    loading_truck.left_weight -= block.sum_weight
    # 更新剩余箱子 # 要根据uuid更新
    tmp_box_id_dict = {box["uuid"]: True for box in block.box_list}
    sizes = [block.unit_size]
    if block.unit_size[0] != block.unit_size[1]:
        sizes.append((block.unit_size[1], block.unit_size[0], block.unit_size[2]))
    for size in sizes:
        if size not in size_box:
            continue
        size_box[size] = list(filter(lambda box: box["uuid"] not in tmp_box_id_dict, size_box[size]))
        if len(size_box[size]) == 0:
            del size_box[size]
    loading_truck.free_space_list.pop()
    # refresh_space用于后面合并空间
    refresh_spaces_list, loading_truck.discard_space_list = get_refresh_spaces(block_space,
                                                                               loading_truck.discard_space_list)
    # 遍历之前的判断重叠
    loading_truck.free_space_list = update_space_list_by_block_space(block_space, loading_truck.free_space_list)
    loading_truck.discard_space_list = update_space_list_by_block_space(block_space, loading_truck.discard_space_list)

    # 判断完之后把新生成的加上
    deltaX = space.lx - block_space.lx
    deltaY = space.ly - block_space.ly
    deltaZ = space.lz - block_space.lz
    if deltaX > 0:
        space1 = Space(block_space.x + block_space.lx, block_space.y, block_space.z, deltaX, space.ly, space.lz)
        loading_truck.free_space_list.append(space1)
    if deltaY > 0:
        space2 = Space(block_space.x, block_space.y + block_space.ly, block_space.z,
                       min(block_space.lx, space.lx), deltaY, space.lz)
        for pre_space in refresh_spaces_list:
            if pre_space.x + pre_space.lx == space2.x and pre_space.y == space2.y and pre_space.z == space2.z and \
                    pre_space.ly == space2.ly and pre_space.lz == space2.lz:
                space2.x = pre_space.x
                space2.lx = space2.lx + pre_space.lx
                loading_truck.discard_space_list.remove(pre_space)
        loading_truck.free_space_list.append(space2)

    if deltaZ > 0:
        space3 = Space(block_space.x, block_space.y, block_space.z + block_space.lz,
                       block_space.lx, block_space.ly, deltaZ)
        if block_space.lx > space.lx or block_space.ly > space.ly:
            overlapRects = list(filter(
                lambda boxSpace: check_overlap_3d(space3, boxSpace), loading_truck.used_space_list))
            if len(overlapRects) > 0:
                space3.ly = min(overlapRects, key=lambda x: x.y).y - space3.y
        loading_truck.free_space_list.append(space3)


def single_truck_packing(loading_truck, size_box):
    # 根据6要素设计的单车厢装箱过程
    # note: 会改变loading_truck内部变量以及size_box_dict
    while len(loading_truck.free_space_list) > 0 and len(size_box) > 0:
        # 1. 选择空间 K3  argmin(x+y+z)
        # 2. 构建块 K2
        # 3. 选择块 K4
        # 4. 放置块，更新空间, 更新剩余箱子, 更新货车的相关状态 K5
        space = loading_truck.free_space_list[-1]
        # space_index, space = min(enumerate(loading_truck.free_space_list), key=lambda x: (x[1], x[0]))
        block_list1, block_list2 = get_block_list(space, size_box,
                                                  loading_truck.left_weight,
                                                  loading_truck.used_space_list,
                                                  loading_truck.truck_type)

        if len(block_list1) == 0 and len(block_list2) == 0:
            # loading_truck.discard_space_list.append(space) #.insert(0, chooseSpace)?
            loading_truck.discard_space_list.insert(0, space)
            loading_truck.free_space_list.pop()
            continue

        block1 = max(block_list1) if len(block_list1) != 0 else None
        block2 = max(block_list2) if len(block_list2) != 0 else None
        block = block2
        if block is None or (block1 is not None and block1.volume > block.volume):
            block = block1
        update_info(loading_truck, size_box, space, block)  # 下次debug从这里开始看


# 换小车
from MOEAD_MD.process_data import get_size_box, get_platform_box


def switch_smaller_vehicle(truck_type_list, truck):
    smaller_truck_type_list = list(filter(lambda
                                              x: truck.sum_used_space <= x.volume < truck.truck_type.volume and x.maxLoad >= truck.truck_type.maxLoad - truck.left_weight,
                                          truck_type_list))
    smaller_truck_type_list.sort(key=lambda x: x.volume)
    route = truck.visited_platform
    platform_box = get_platform_box(truck.box_list)
    for truck_type in smaller_truck_type_list:
        loading_truck = LoadingTruck(truck_type)
        for platform in route:
            size_box = get_size_box(platform_box[platform])
            single_truck_packing(loading_truck, size_box)
            if len(size_box) > 0:
                break
        else:
            return loading_truck
    return truck


def route_packing(route, truck_type_list, platform_box):
    # 对一条路径进行装载
    loading_truck_list = []
    last_loading_truck = None
    for platform in route:
        size_box = get_size_box(platform_box[platform])
        while len(size_box) > 0:
            if last_loading_truck is None:
                last_loading_truck = LoadingTruck(truck_type_list[0])
            else:
                last_loading_truck.free_space_list.extend(last_loading_truck.discard_space_list)
                last_loading_truck.free_space_list.sort(reverse=True)
                last_loading_truck.discard_space_list = []

            single_truck_packing(last_loading_truck, size_box)
            if len(size_box) > 0:
                loading_truck_list.append(switch_smaller_vehicle(truck_type_list, last_loading_truck))
                last_loading_truck = None

    if last_loading_truck is not None:
        loading_truck_list.append(switch_smaller_vehicle(truck_type_list, last_loading_truck))

    return loading_truck_list
