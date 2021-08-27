import numpy as np


class CostVehicleRoutingCalculator:

    def __init__(self, bitstring, graph, number_of_cars, penalty_factor):
        self.dimensionality = graph.order()
        self.adjacency_matrix = self.bitstring_to_adjacency_matrix(bitstring)
        self.number_of_cars = number_of_cars
        self.graph = graph
        self.penalty_factor = penalty_factor

    def get_adjacency_matrix(self):
        return self.adjacency_matrix

    def vehicle_routing_cost(self):
        cost_trip = self.compute_cost_trip()
        cost_outgoing_cars = self.compute_cost_outgoing_cars()
        cost_incoming_cars = self.compute_cost_incoming_cars()
        cost_outgoing_cars_base = self.compute_cost_outgoing_cars_base()
        cost_incoming_cars_base = self.compute_cost_incoming_cars_base()
        return cost_trip + cost_outgoing_cars + cost_incoming_cars + cost_incoming_cars_base + cost_outgoing_cars_base

    def compute_cost_trip(self):
        cost = 0
        for i in range(0, self.dimensionality):
            for j in range(0, self.dimensionality):
                if i != j and self.graph.has_edge(i, j):
                    edge_weight = self.graph.edges[i, j]['weight']
                    cost += edge_weight * self.adjacency_matrix[i, j]
        return cost

    def compute_cost_outgoing_cars(self):
        cost = 0
        for i in range(1, self.dimensionality):
            outgoing_cars_i_node = 0
            for j in range(0, self.dimensionality):
                outgoing_cars_i_node += self.adjacency_matrix[i, j]
            cost += self.penalty_factor * (1 - outgoing_cars_i_node) ** 2
        return cost

    def compute_cost_incoming_cars(self):
        cost = 0
        for i in range(1, self.dimensionality):
            incoming_cars_i_node = 0
            for j in range(0, self.dimensionality):
                incoming_cars_i_node += self.adjacency_matrix[j, i]
            cost += self.penalty_factor * (1 - incoming_cars_i_node) ** 2
        return cost

    def compute_cost_incoming_cars_base(self):
        cost = 0
        incoming_cars_base = 0
        for i in range(1, self.dimensionality):
            incoming_cars_base += self.adjacency_matrix[0, i]
        cost += self.penalty_factor * (self.number_of_cars - incoming_cars_base) ** 2
        return cost

    def compute_cost_outgoing_cars_base(self):
        cost = 0
        outgoing_cars_base = 0
        for i in range(1, self.dimensionality):
            outgoing_cars_base += self.adjacency_matrix[i, 0]
        cost += self.penalty_factor * (self.number_of_cars - outgoing_cars_base) ** 2
        return cost

    def bitstring_to_adjacency_matrix(self, bitstring):
        matrix = np.zeros((self.dimensionality, self.dimensionality))
        index = 0
        lengthBitString = len(bitstring)
        if (lengthBitString + self.dimensionality) == (self.dimensionality * self.dimensionality):
            for i in range(0, self.dimensionality):
                for j in range(0, self.dimensionality):
                    if j == i:
                        matrix[i][j] = 0
                    else:
                        matrix[i][j] = bitstring[index]
                        index += 1
            index += 1
        else:
            print('Dimensionality is inconsistent')
        return matrix
