
import sys
sys.path.append("..")
import time
import networkx as nx
import random
import copy
import numpy
from Deal_with_text_files import portrait, GenerateTestFile, historyevents,\
    AddedTestFile, RecordFiles, writing_time
from Deal_with_text_files import write_to_files, statue, mall_process, varying_k
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


def Local(sample_edges, number_of_edges):
    global nodes, edges, Matrix
    weight = copy.deepcopy(Matrix)
    score = {}
    wins = {}
    loses = {}
    for node in nodes:
        score[node] = 0
        wins[node] = 0
        loses[node] = 0

    set_sample_edges = set(sample_edges)

    for edge in set_sample_edges:
        wins[edge[0]] += weight[edge]
        loses[edge[1]] += weight[edge]

    for i in range(len(nodes)):
        score[nodes[i]] = wins[nodes[i]] - loses[nodes[i]]
        for j in range(len(nodes)):
            if i != j and weight[(nodes[i], nodes[j])] > weight[(nodes[j], nodes[i])]:
                score[nodes[i]] += wins[nodes[j]]
            elif i != j and weight[(nodes[i], nodes[j])] < weight[(nodes[j], nodes[i])]:
                score[nodes[i]] -= loses[nodes[j]]

    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

    result = []

    for item in sorted_score:
        result.append(item[0])
    for item in sorted_score:
        print item

    print result

    result_sequence = []

    for item in result:
        temp_array = []
        if item not in result_sequence:
            for key in score.keys():
                if score[key] == score[item]:
                    temp_array.append(key)
        random.shuffle(temp_array)
        result_sequence.extend(temp_array)

    write_to_files.write_to_files('Local', result, number_of_edges)
    write_to_files.acc_write_to_files(
        'Local_ACC', result_sequence, number_of_edges)


def main():
    for percent in numpy.arange(0.1, 1.1, 0.1):
        print percent

        sample_edges = random.sample(edges, int(percent * len(edges)))
        pre_process(sample_edges)

        Local(sample_edges, int(percent * 100))


def repeat_main():
    for xiter in range(1000):
        print "SIGMODLocal", xiter
        main()

if __name__ == "__main__":
    global nodes, edges, Matrix
    nodes, edges, BaseMatrix = GenerateTestFile.simulant_dataset()
    repeat_main()
