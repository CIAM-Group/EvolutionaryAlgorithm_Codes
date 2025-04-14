import random


def get_random_sol(platfrom_list):
    sol = platfrom_list[:]
    random.shuffle(sol)
    return sol


def get_sub_sol(sol, must_visted_dict):
    """
	param: sol: ["platCode", ...]
		   must_visted_dict: {"platCode": True/False, ...}
	return: subsol: [["platCode", ...], ...]
	"""
    sub_sols = []
    end_pointer = len(sol)
    start_pointer = len(sol)
    for platform in reversed(sol):
        start_pointer -= 1
        if must_visted_dict[platform]:
            sub_sols.append([x for x in sol[start_pointer:end_pointer]])
            end_pointer = start_pointer
    if must_visted_dict[sol[0]] is False:
        sub_sols.append([x for x in sol[0:end_pointer]])
    return sub_sols
