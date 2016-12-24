
import sys
sys.path.append("..")
import time
import random
import numpy
import heapq
from Deal_with_text_files import historyevents, write_to_files, portrait, GenerateTestFile, \
    statue, mall_process, AddedTestFile, RecordFiles, writing_time
global nodes, edges, Matrix


def Borda_Count(nodes, sample_edges, the_number_of_edges):

    score = {}
    for node in nodes:
        score[node] = 0
    for edge in sample_edges:
        score[edge[0]] += 1
        score[edge[1]] += 0
    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
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

    write_to_files.write_to_files('BordaCount', result, the_number_of_edges)
    write_to_files.acc_write_to_files(
        'BordaCount_ACC', result_sequence, the_number_of_edges)


def Copeland(nodes, sample_edges, the_number_of_edges):

    score = {}
    for node in nodes:
        score[node] = 0
    for edge in sample_edges:
        score[edge[0]] += 1
        score[edge[1]] -= 1
    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
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

    write_to_files.write_to_files('Copeland', result, the_number_of_edges)
    write_to_files.acc_write_to_files(
        'Copeland_ACC', result_sequence, the_number_of_edges)


def main_borda_count():
    for number in numpy.arange(0.1, 1.1, 0.1):
        sample_edges = random.sample(edges, int(len(edges) * number))
        Borda_Count(nodes, sample_edges, int(number * 100))


def main_copeland():
    for number in numpy.arange(0.1, 1.1, 0.1):
        sample_edges = random.sample(edges, int(len(edges) * number))
        Copeland(nodes, sample_edges, int(number * 100))


def Redo():
    for re in range(1000):
        print re
        main_borda_count()
        main_copeland()

if __name__ == "__main__":
    nodes, edges, Matrix = GenerateTestFile.simulant_dataset()
    Redo()
