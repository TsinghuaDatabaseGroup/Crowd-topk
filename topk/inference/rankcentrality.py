
import sys
sys.path.append("..")
import time
import random
import math
import numpy
import copy
from evaluate_metric import acc, recall
from text_files import portrait, GenerateTestFile, historyevents, statue, mall_process


global n, nodes, edges, Matrix, BaseMatrix, range_number


def pre_process(sample_edges):
    global n, nodes, edges, Matrix, BaseMatrix, range_number
    Matrix = {}
    Matrix = copy.deepcopy(BaseMatrix)
    set_sample_edges = set(sample_edges)
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if (nodes[i], nodes[j]) not in set_sample_edges:
                Matrix[(nodes[i], nodes[j])] = 0


def BTL_model(x):

    return 1 / (1 + math.exp(-1 * x))


def computation_A(i, j):
    if (Matrix[(i, j)] + Matrix[(j, i)]) != 0:
        return float(Matrix[(j, i)]) / (Matrix[(i, j)] + Matrix[(j, i)])
    else:
        return 0.5

def computation_P(i, j):

    global n, nodes, edges, Matrix

    dmax = 200.0

    if i != j:
        return (1 / dmax) * computation_A(i, j)
    elif i == j:
        xsum = 0
        for k in range(n):
            if k != i:
                xsum += computation_A(i, k)

        return 1 - (1 / dmax) * xsum

def spearman_distance(array):
    
    length = len(array)
    result = 0
    for index in range(1, length + 1):
        result += math.fabs(array[index - 1] - index)
    return result

def topk_estimation(array):
    recall = 0
    for item in array[:10]:
        if item < 10:
            recall += 1
    return recall

def computation_stationary_distribution(number_of_edges):
    global n, nodes, edges, Matrix
    n = len(nodes)
    P = numpy.identity(n)
    for i in range(n):
        for j in range(n):
            P[i][j] = computation_P(i, j)

    initial_p_value = numpy.zeros((1, n))
    for i in range(n):
        initial_p_value[0][i] = random.random()

    for xiter in range(1):

        P_next = numpy.dot(initial_p_value, P)

        initial_p_value = copy.deepcopy(P_next)

    score = {}
    for nodeA in nodes:
        xsum = 0
        nodeAsum = 0
        for nodeB in nodes:
            nodeAsum += computation_A(nodeA, nodeB)

        for nodeB in nodes:
            xsum += (initial_p_value[0][nodeB] *
                     computation_A(nodeB, nodeA)) / float(nodeAsum)
        score[nodeA] = xsum

    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse = True)

    result = []
    for item in sorted_score:
        print item
        result.append(item[0])

    print result
    
    reversed_result = result[::-1]
    
    if topk_estimation(result) > topk_estimation(reversed_result):
        recall.simple_recall('RankCentrality', result, number_of_edges)
    else:
        recall.simple_recall('RankCentrality', reversed_result, number_of_edges)
    
#     if spearman_distance(result) < spearman_distance(reversed_result):
#         acc.to_files('RankCentrality_17', result, number_of_edges)
#     else:
#         acc.to_files('RankCentrality_17', reversed_result, number_of_edges)


def main():
    for percent in numpy.arange(0.1, 1.0, 0.1):
        number_of_edges = int(percent * len(edges))
        sample_edges = random.sample(edges, number_of_edges)
        pre_process(sample_edges)

        computation_stationary_distribution(int(percent * 100))

def repeat_main():
    for xiter in range(10000):
        print "RankCentrality", xiter
        main()

if __name__ == "__main__":

    global n, nodes, edges, Matrix, BaseMatrix, range_number
    nodes, edges, Matrix = GenerateTestFile.simulant_dataset()
    BaseMatrix = copy.deepcopy(Matrix)

    repeat_main()
