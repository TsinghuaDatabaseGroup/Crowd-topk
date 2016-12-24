
import sys
sys.path.append("..")
import elo
import heapq
import math
import time
from Deal_with_text_files import write_to_files, historyevents, portrait, GenerateTestFile, statue, mall_process
from Deal_with_text_files import statue, AddedTestFile, RecordFiles, varying_k, writing_time
import random
global nodes, edges, Matrix


def ELO_formula(nodes, sample_edges, number_of_edges):

    score = {}
    for node in nodes:
        score[node] = 50

    for edge in sample_edges:
        i = edge[0]
        j = edge[1]
        score[i] = score[i] + 32 * \
            (1 - 1 / (1 + math.pow(10, (score[j] - score[i]) / 400.0)))
        score[j] = score[j] + 32 * \
            (0 - 1 / (1 + math.pow(10, (score[i] - score[j]) / 400.0)))

    result = heapq.nlargest(10, score, key=score.get)
    print result

    for item in nodes:
        print item, score[item]


def ELO_Ranking(nodes, sample_edges, number_of_edges):

    score = {}
    for node in nodes:
        score[node] = random.randint(40, 60)

    for edge in sample_edges:
        compare_result = elo.rate_1vs1(score[edge[0]], score[edge[1]])
        score[edge[0]] = compare_result[0]
        score[edge[1]] = compare_result[1]

    result = heapq.nlargest(10, score, key=score.get)
    print result

    for item in nodes:
        print item, score[item]


def main():
    for percent in range(10, 110, 10):
        sample_edges = random.sample(
            edges, int((percent / 100.0) * len(edges)))
        ELO_formula(nodes, sample_edges, percent)


def Redo():
    for re in range(1000):
        print "ELO", re
        main()


if __name__ == "__main__":
    nodes, edges, Matrix = GenerateTestFile.simulant_dataset()
    Redo()
