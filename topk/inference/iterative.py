
import sys
sys.path.append("..")
import time
import networkx as nx
import random
import copy
import numpy
from Deal_with_text_files import portrait, GenerateTestFile, historyevents,\
    AddedTestFile, RecordFiles, writing_time
from Deal_with_text_files import write_to_files, statue, mall_process
global nodes, edges, Matrix, BaseMatrix, range_number


def pre_process(sample_edges):
    global nodes, edges, Matrix, range_number
    Matrix = {}
    Matrix = copy.deepcopy(BaseMatrix)
    set_sample_edges = set(sample_edges)
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if (nodes[i], nodes[j]) not in set_sample_edges:
                Matrix[(nodes[i], nodes[j])] = 0


def Iterative_Ranking(percent, K=10):

    dif = {}
    for node in nodes:
        dif[node] = 0

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                dif[nodes[j]] = dif[nodes[j]] - Matrix[(nodes[i], nodes[j])]
                dif[nodes[i]] = dif[nodes[i]] + Matrix[(nodes[i], nodes[j])]
    Q = copy.deepcopy(nodes)

    while len(Q) > K:
        print len(Q), Q
        sorted_Q = sorted(
            dif.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        result = []
        for item in sorted_Q:
            result.append(item[0])

        if len(Q) / 2 > K:
            array_length = len(Q) / 2
        else:
            array_length = K

        for i in result[array_length:]:
            Q.remove(i)
            for j in Q:
                if Matrix[(j, i)] > 0:
                    dif[j] = dif[j] - Matrix[(j, i)]
                    dif[i] = dif[i] + Matrix[(j, i)]
                if Matrix[(i, j)] > 0:
                    dif[i] = dif[i] - Matrix[(i, j)]
                    dif[j] = dif[j] + Matrix[(i, j)]
            dif.pop(i)
    print Q
    write_to_files.write_to_files('Iterative', Q, percent)
    random.shuffle(Q)
    write_to_files.acc_write_to_files('Iterative_ACC', Q, percent)


def main():
    for percent in numpy.arange(0.1, 1.1, 0.1):
        sample_edges = random.sample(edges, int(percent * len(edges)))
        pre_process(sample_edges)
        random.shuffle(nodes)

        Iterative_Ranking(int(percent * 100), K=10)


def repeat_main():
    for xiter in range(1000):
        print xiter
        print "SIGMODIterative", xiter
        main()

if __name__ == "__main__":
    global nodes, edges, Matrix, range_number
    nodes, edges, BaseMatrix = GenerateTestFile.simulant_dataset()

    repeat_main()
