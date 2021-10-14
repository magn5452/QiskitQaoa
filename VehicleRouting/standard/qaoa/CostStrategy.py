import numpy as np

from VehicleRouting.framework.qaoa.CostStategy import CostStrategy


class MinCostStrategy(CostStrategy):
    def __init__(self):
        pass

    def calculate_cost(self, count_dic, qubo):
        min_value = np.inf

        total = 0
        for _, count in count_dic.items():
            total += count

        for bitstring, count in count_dic.items():
            epsilon = 0.01
            if count / total < epsilon:
                integer_array = np.fromiter(bitstring, np.int8)  # convert string of number to np.array of integer
                value = qubo.calculate_qubo_cost(integer_array)
                if value < min_value:
                    min_value = value
        return min_value


class CVaRCostStrategy(CostStrategy):
    def __init__(self, alpha):
        self.alpha = alpha

    def calculate_cost(self, count_dic, qubo):
        counts = count_dic.values()
        total = sum(counts)  # total counts
        max_count = self.alpha * total
        cost_dic = self.get_cost_dic(count_dic, qubo)
        sorted_cost_dic = self.sort_dic(cost_dic)

        result = 0
        count_accumulator = 0
        for bitstring in sorted_cost_dic:
            if count_accumulator < max_count:
                count = count_dic[bitstring]
                cost = cost_dic[bitstring]
                new_count = np.minimum(count, max_count - count_accumulator)
                result += cost * new_count
                count_accumulator += new_count
            else:
                break

        return result / count_accumulator

    def sort_dic(self, cost_dic):
        sorted_cost_dic = dict(sorted(cost_dic.items(), key=lambda item: item[1]))  # sort dictionary by value
        return sorted_cost_dic

    def get_cost_dic(self, count_dic, qubo):
        cost_dic = {}
        for bitstring in count_dic:
            integer_array = np.fromiter(bitstring, np.int8)
            cost = qubo.calculate_qubo_cost(integer_array)
            cost_dic.update({bitstring: cost})
        return cost_dic


class AverageCostStrategy(CostStrategy):
    def __init__(self):
        pass

    def calculate_cost(self, count_dic, qubo):
        sum_cost = 0
        sum_count = 0
        for bitstring, count in count_dic.items():
            integer_array = np.fromiter(bitstring, np.int8)  # convert string of number to np.array of integer
            cost = qubo.calculate_qubo_cost(integer_array)
            sum_cost += cost * count
            sum_count += count

        expectation_value = sum_cost / sum_count
        return expectation_value


class ProjectionStrategy(CostStrategy):
    def __init__(self, bitstring):
        self.bitstring = bitstring

    def calculate_cost(self, count_dic, qubo):
        counts = count_dic.values()
        total = sum(counts)
        count = count_dic[self.bitstring]
        return 1-count/total

