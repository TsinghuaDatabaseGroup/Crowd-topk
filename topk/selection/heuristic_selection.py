

import time
from Deal_with_text_files import portrait, GenerateTestFile, mall_process, write_to_files, historyevents, statue
from InferenceForSelection import Score_PageRank, Score_MLECrowdBT
from InferenceForSelection import sig_local, Hybrid, MLECrowdBT, sig_iterative, sig_local, ELO
from InferenceForSelection import SSRW
import random
import numpy
import heapq
global nodes, edges, Matrix


def PairedSelection(score, n, number_of_pairs):

    start = time.time()

    next_pairs = []

    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result = []
    for item in sorted_score:
        result.append(item[0])

    try:
        for i in range(0, n, 2):
            next_pairs.append((result[i], result[i+1]))
    except Exception, e:
        return next_pairs[:number_of_pairs]

    end = time.time()

    return next_pairs[:number_of_pairs]


def MaxSelection(score, n, number_of_pairs):

    start = time.time()

    next_pairs = []

    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result = []
    for item in sorted_score:
        result.append(item[0])

    for i in range(1, n):
        next_pairs.append((result[0], result[i]))

    end = time.time()

    return next_pairs[:number_of_pairs]


def GreedySelection(score, n, number_of_pairs):

    start = time.time()

    edge_score = {}

    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result = []
    for item in sorted_score:
        result.append(item[0])

    for i in range(len(result)):
        for j in range(i+1, len(result)):
            edge_score[(result[i], result[j])] = (
                score[i]+1000) * (score[j]+1000)

    edge_sorted_score = sorted(
        edge_score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    edge_result = []
    for item in edge_sorted_score:
        edge_result.append(item[0])

    end = time.time()

    return edge_result[:number_of_pairs]


def CompleteSelection(score, n, number_of_pairs, k=5, b=10):

    next_pairs = []
    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result = []
    for item in sorted_score:
        result.append(item[0])

    for index in range(k):
        for indexB in range(index+1, k):
            next_pairs.append((result[index], result[indexB]))

    candidate_pairs = []
    for i in range(k):
        candidate_pairs.append((result[i], result[k]))

    for index in range((b - k * (k - 1) / 2)):
        if index < len(candidate_pairs):
            next_pairs.append(candidate_pairs[index])

    if len(next_pairs) == number_of_pairs:

        return next_pairs[:number_of_pairs]

    return next_pairs[:number_of_pairs]


def initial_process():
    global nodes, edges, Matrix

    nodes, edges, Matrix = mall_process.mall_process()

    for nodeA in nodes:
        for nodeB in nodes:
            if (nodeA, nodeB) not in Matrix:
                Matrix[(nodeA, nodeB)] = 0


def Copeland(test_edges):

    score = {}
    for node in nodes:
        score[node] = 0
    for edge in test_edges:
        score[edge[0]] += 1
        score[edge[1]] -= 1

    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result = []
    for item in sorted_score:
        result.append(item[0])
    return score


def selection_process():

    initial_process()

    for percent in numpy.arange(0.1, 1.1, 0.1):

        print percent

        number_of_edges_round = int(len(edges) * (percent-0.1))

        selected_edges = random.sample(edges, int(len(edges) * 0.1))

        for x in range(0, number_of_edges_round, 10):

            if x+10 <= number_of_edges_round:
                sample_number = 10

            elif x+10 > number_of_edges_round:
                sample_number = number_of_edges_round - x

            trans_Matrix = {}

            for trans_edge in selected_edges:
                trans_Matrix[trans_edge] = Matrix[trans_edge]

            estimated_score = Score_PageRank.PageRank_Ranking(
                nodes, selected_edges, trans_Matrix)

            selected_edges.extend(
                CompleteSelection(estimated_score, len(nodes), sample_number))

        trans_Matrix = {}
        for trans_edge in selected_edges:
            trans_Matrix[trans_edge] = Matrix[trans_edge]

        '''PairedSelection, MaxSelection, GreedySelection, CompleteSelection'''

        ELO.ELO_Ranking(
            'CompleteSelection', nodes, selected_edges, trans_Matrix, int(percent * 100))


if __name__ == "__main__":

    for xiter in range(1000):
        selection_process()
