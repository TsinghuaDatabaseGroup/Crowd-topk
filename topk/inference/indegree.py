
import sys
sys.path.append("..")
import time
import networkx as nx
import random
import copy
import numpy
import math
import operator
from Deal_with_text_files import portrait, GenerateTestFile, historyevents,\
    AddedTestFile, RecordFiles, writing_time
from Deal_with_text_files import write_to_files, statue, mall_process
global nodes, edges, Matrix, BaseMatrix


def pre_process(sample_edges):
    global Matrix
    Matrix = {}
    Matrix = copy.deepcopy(BaseMatrix)
    set_sample_edges = set(sample_edges)
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if (nodes[i], nodes[j]) not in set_sample_edges:
                Matrix[(nodes[i], nodes[j])] = 0


def c(n, k):
    if k == 0:
        return 1
    else:
        return reduce(operator.mul, range(n - k + 1, n + 1)) / reduce(operator.mul, range(1, k + 1))


def Indegree(sample_edges, percent):
    global nodes, Matrix
    score = {}
    for node in nodes:
        score[node] = 0

    probability = 0.55

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:

                win_point = i
                lose_point = j

                OIJ = c( ( Matrix[(win_point, lose_point)] + Matrix[(lose_point, win_point)] ) , Matrix[(win_point, lose_point)]) * \
                    math.pow(probability, Matrix[
                             (win_point, lose_point)]) * math.pow((1 - probability), Matrix[(lose_point, win_point)])

                OJI = c( ( Matrix[(win_point, lose_point)] + Matrix[(lose_point, win_point)] ) , Matrix[(lose_point, win_point)]) * \
                    math.pow(probability, Matrix[
                             (lose_point, win_point)]) * math.pow((1 - probability), Matrix[(win_point, lose_point)])

                score[win_point] += float(OIJ) / (OIJ + OJI)

    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

    result = []

    for item in sorted_score:
        result.append(item[0])
        print item

#     RecordFiles.record_dataset('SIG_Indegree', result, percent)


def main():
    for percent in numpy.arange(0.1, 1.1, 0.1):
        sample_edges = random.sample(edges, int(percent * len(edges)))
        pre_process(sample_edges)
        random.shuffle(nodes)

        Indegree(sample_edges, int(percent * 100))


def repeat_main():
    for xiter in range(1000):
        print "SIGMODIndegree", xiter
        main()

if __name__ == "__main__":
    global nodes, edges, Matrix, BaseMatrix
    nodes, edges, BaseMatrix = GenerateTestFile.simulant_dataset()
    Matrix = copy.deepcopy(BaseMatrix)
    repeat_main()
