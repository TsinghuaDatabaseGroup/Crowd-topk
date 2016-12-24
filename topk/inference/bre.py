
import sys
sys.path.append("..")
import random
import numpy
import time
from Deal_with_text_files import GenerateTestFile, mall_process, portrait, \
    write_to_files, historyevents, statue, AddedTestFile, RecordFiles, writing_time
global nodes, edges, Matrix


def pre_process():
    global nodes, edges, Matrix
    nodes, edges, Matrix = GenerateTestFile.simulant_dataset()
    for key in Matrix.keys():
        if Matrix[key] > 5:
            Matrix[key] = 5


def BRE(sample_edges, percent):

    score = {}
    for node in nodes:
        score[node] = 0
    set_sample_edges = set(sample_edges)
    for j in range(len(nodes)):
        xsum = 0
        for i in range(len(nodes)):
            if i != j:
                if (nodes[i], nodes[j]) in set_sample_edges:
                    xsum += 2 * 1 - 1
                elif (nodes[j], nodes[i]) in set_sample_edges:
                    xsum += 2 * 0 - 1

        score[nodes[j]] = xsum
    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=False)

    print sorted_score[:10]

    result = []
    for item in sorted_score:
        result.append(item[0])

    result_sequence = []

    for item in result:
        temp_array = []
        if item not in result_sequence:
            for key in score.keys():
                if score[key] == score[item]:
                    temp_array.append(key)
        random.shuffle(temp_array)
        result_sequence.extend(temp_array)


def percent_recall():
    for percent in numpy.arange(0.1, 1.1, 0.1):
        sample_edges = random.sample(edges, int(len(edges) * percent))
        BRE(sample_edges, int(percent * 100))


def Average_recall():
    pre_process()
    for re in range(1000):
        print 'BRE', re
        percent_recall()


Average_recall()
