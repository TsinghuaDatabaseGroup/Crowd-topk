
import sys
sys.path.append("..")
import time
import math
import random
import heapq
import numpy
import copy
from Deal_with_text_files import GenerateTestFile, write_to_files, portrait, historyevents, mall_process,\
    AddedTestFile, ACC, writing_time
from Deal_with_text_files import statue
from InferenceForSelection import MLECrowdBT, Hybrid, sig_iterative, sig_local, ELO
from InferenceForSelection import SSRW
global nodes, edges, Matrix, BaseMatrix
global counts


def estimation_of_c(i, j, N, NMAX):
    delta = 0.1
    factor1 = 1.0 / (2 * Matrix[(i, j)])
    factor2 = math.log(2 * N * N * NMAX / delta)
    return math.pow(factor1 * factor2, 0.5)


def pre_process():
    global nodes, edges, Matrix, counts, BaseMatrix
    counts = {}
    Matrix = BaseMatrix
    for nodeA in nodes:
        for nodeB in nodes:
            counts[(nodeA, nodeB)] = 0
            if (nodeA, nodeB) not in Matrix:
                Matrix[(nodeA, nodeB)] = 0
            if Matrix[(nodeA, nodeB)] > 5:
                Matrix[(nodeA, nodeB)] = 5


def PBR_SSSE(K=10):

    upper_bound = {}
    lower_bound = {}
    node_upper_bound = {}
    node_lower_bound = {}

    for nodeA in nodes:
        for nodeB in nodes:
            upper_bound[(nodeA, nodeB)] = 0
            lower_bound[(nodeA, nodeB)] = 0

    select = []
    discard = []
    count_edges = 0
    random.shuffle(edges)
    used_edges = []

    for edge in edges:

        if edge[0] in set(select).union(set(discard)) or edge[1] in set(select).union(set(discard)):
            continue

        used_edges.append(edge)
        count_edges += 1
        counts[edge] += 1
        confidence_bounds = estimation_of_c(edge[0], edge[1], len(nodes), 10)
        upper_bound[edge] = Matrix[edge] / \
            (Matrix[edge] + Matrix[(edge[1], edge[0])]) + confidence_bounds
        lower_bound[edge] = Matrix[edge] / \
            (Matrix[edge] + Matrix[(edge[1], edge[0])]) - confidence_bounds

        for nodeA in nodes:
            lose_count_sum = 0
            for nodeB in nodes:
                if nodeA != nodeB:
                    lose_count_sum += lower_bound[(nodeA, nodeB)]
            node_lower_bound[nodeA] = lose_count_sum

        for nodeA in nodes:
            win_count_sum = 0
            for nodeB in nodes:
                if nodeA != nodeB:
                    win_count_sum += upper_bound[(nodeA, nodeB)]
            node_upper_bound[nodeA] = win_count_sum

        if count_edges > 0:
            for nodeA in nodes:
                absolute_win = 0
                for nodeB in nodes:
                    if node_lower_bound[nodeA] > node_upper_bound[nodeB]:
                        absolute_win += 1
                if absolute_win >= (len(nodes) - K) and nodeA not in select:
                    select.append(nodeA)

            for nodeA in nodes:
                absolute_lose = 0
                for nodeB in nodes:
                    if node_upper_bound[nodeA] < node_lower_bound[nodeB]:
                        absolute_lose += 1
                if absolute_lose >= K and nodeA not in discard:
                    discard.append(nodeA)

        for percent in numpy.arange(0.1, 1.1, 0.1):

            if count_edges == int(percent * len(edges)):

                start_time = time.time()

                for nodeA in nodes:
                    lose_count_sum = 0
                    for nodeB in nodes:
                        if nodeA != nodeB:
                            lose_count_sum += lower_bound[(nodeA, nodeB)]
                    node_lower_bound[nodeA] = lose_count_sum

                for nodeA in nodes:
                    win_count_sum = 0
                    for nodeB in nodes:
                        if nodeA != nodeB:
                            win_count_sum += upper_bound[(nodeA, nodeB)]
                    node_upper_bound[nodeA] = win_count_sum

                if count_edges > 0:
                    for nodeA in nodes:
                        absolute_win = 0
                        for nodeB in nodes:
                            if node_lower_bound[nodeA] > node_upper_bound[nodeB]:
                                absolute_win += 1
                        if absolute_win >= (len(nodes) - K) and nodeA not in select:
                            select.append(nodeA)

                    for nodeA in nodes:
                        absolute_lose = 0
                        for nodeB in nodes:
                            if node_upper_bound[nodeA] < node_lower_bound[nodeB]:
                                absolute_lose += 1
                        if absolute_lose >= K and nodeA not in discard:
                            discard.append(nodeA)

                print 'select', select, '\t',
                print 'discard', discard

                estimated_score = {}
                edge_score = {}
                for node in nodes:
                    estimated_score[node] = 0

                for nodeA in nodes:
                    for nodeB in nodes:
                        edge_score[(nodeA, nodeB)] = 0

                for edge in used_edges:
                    edge_score[edge] = Matrix[edge] / \
                        (Matrix[edge] + Matrix[(edge[1], edge[0])])

                for nodeA in nodes:
                    for nodeB in nodes:
                        estimated_score[nodeA] += edge_score[(nodeA, nodeB)]

                result = heapq.nlargest(
                    100, estimated_score, key=estimated_score.get)

                end_time = time.time()
                used_time = end_time - start_time

                trans_Matrix = {}

                for edge in used_edges:
                    trans_Matrix[edge] = Matrix[edge]

                ELO.ELO_Ranking(
                    'PBRSSSE', nodes, used_edges, trans_Matrix, int(percent * 100))


def main():
    global nodes, edges, BaseMatrix

    for xe in range(1000):
        print xe
        nodes, edges, BaseMatrix = mall_process.mall_process()
        pre_process()
        random.shuffle(edges)

        PBR_SSSE(K=10)


if __name__ == "__main__":

    main()
