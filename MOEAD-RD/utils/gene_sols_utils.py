import random

class CrossForNNCoding:
    @staticmethod
    def pmx_crossover(parent1, parent2):
        length = len(parent1)
        start, end = sorted(random.sample(range(length), 2))
        offspring1 = [-1] * length
        offspring2 = [-1] * length
        for i in range(start, end + 1):
            offspring1[i] = parent2[i]
            offspring2[i] = parent1[i]
        for i in range(length):
            if i < start or i > end:
                gene1 = parent1[i]
                gene2 = parent2[i]
                while gene1 in offspring1:
                    idx = parent2.index(gene1)
                    gene1 = parent1[idx]
                while gene2 in offspring2:
                    idx = parent1.index(gene2)
                    gene2 = parent2[idx]
                offspring1[i] = gene1
                offspring2[i] = gene2
        return offspring1, offspring2
    
    @staticmethod
    def ox_crossover(parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1)), 2))
        offspring = [-1] * len(parent1)
        offspring[start:end+1] = parent1[start:end+1]
        for i in range(len(parent2)):
            if parent2[i] not in offspring:
                for j in range(len(offspring)):
                    if offspring[j] == -1:
                        offspring[j] = parent2[i]
                        break
        return offspring

    @staticmethod
    def cross(sol1, sol2):
        index1 = random.randint(0, len(sol1) - 1)
        index2 = random.randint(index1, len(sol1) - 1)
        tempGene = sol2[index1:index2]
        newGene = []
        p1len = 0
        for g in sol1:
            if p1len == index1:
                newGene.extend(tempGene)  # 插入基因片段
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        return newGene, None


class MutateForNNCoding:
    def random_swap(lst):
        new_lst = lst[:]
        idx1, idx2 = random.sample(range(len(new_lst)), 2)
        new_lst[idx1], new_lst[idx2] = new_lst[idx2], new_lst[idx1]
        return new_lst
    
    def opt2(lst):
        new_lst = lst[:]
        start, end = sorted(random.sample(range(len(new_lst)), 2))
        new_lst[start:end+1] = new_lst[start:end+1][::-1]
        return new_lst
    
    def relocate(lst):
        new_lst = lst[:]
        idx = random.randint(0, len(new_lst)-1)
        val = new_lst.pop(idx)
        new_idx = random.randint(0, len(new_lst))
        new_lst.insert(new_idx, val)
        return new_lst
    def relocate_old_version(sol):
        index1 = random.randint(0, len(sol) - 1)
        index2 = random.randint(0, len(sol) - 1)
        tag = 1000
        while tag > 0 and index1 == index2:
            index2 = random.randint(0, len(sol) - 1)
            tag -= 1
        if index1 == index2:
            return sol
        index1, index2 = min(index1, index2), max(index1, index2)
        newSol = sol[:]  # 防止变异到父代

        if index2 != len(sol) - 1:
            newSol = newSol[:index1] + [newSol[index2]] + newSol[index1 + 1:index2] + [newSol[index1]] + newSol[index2 + 1:]
        else:
            newSol = newSol[:index1] + [newSol[index2]] + newSol[index1 + 1:index2] + [newSol[index1]]
        assert set(newSol) == set(sol) and len(newSol) == len(sol)
        return newSol