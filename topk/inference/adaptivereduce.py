
import sys
sys.path.append("..")
import time
import math
import random
import numpy
import copy
from Deal_with_text_files import GenerateTestFile, mall_process, portrait,\
    AddedTestFile, RecordFiles, writing_time
from Deal_with_text_files import write_to_files, historyevents, statue
global nodes, BaseEdges, Matrix, TOPK


def Max_Verify(X, q, pro_fail):

    N = len(X)
    factor1 = 4 * math.log10(N) / (pro_fail * math.log10(8.0 / 7))
    factor2 = 64 * math.log10(4 * math.log10(N) / (pro_fail * math.log10(8.0 / 7))) + \
        2 * math.log10(64) - 2
    return max(factor1, factor2)


def adaptiveReduce(X, q, Edges, percent):
    global TOPK
    set_Edges = set(Edges)
    N = len(X)
    factor = (16 * math.pow((0.5 - q), -2) + 32) * math.log10(N)
    try:
        X_random = random.sample(X, int(factor))
    except Exception, e:
        X_random = X

    win_counts = {}
    for item in X_random:
        win_counts[item] = 0

    for item in X_random:
        for node in X:
            if (item, node) in set_Edges:
                win_counts[item] += 1
    X_vote = []
    for item in X_random:
        if win_counts[item] >= 0.25 * N and win_counts[item] <= 0.75 * N:
            X_vote.append(item)

    voting_counts = {}
    for item in X:
        voting_counts[item] = 0

    for item in X:
        for node in X_vote:
            if (item, node) in set_Edges:
                voting_counts[item] += 1

    sorted_score = sorted(
        voting_counts.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result = []
    for item in sorted_score:
        result.append(item[0])

    back_result = []
    for item in result:
        input_item_array = []
        if item not in back_result:
            for itemB in result:
                if voting_counts[item] == voting_counts[itemB]:
                    input_item_array.append(itemB)
            random.shuffle(input_item_array)
            back_result.extend(input_item_array)

    ReducedSet = back_result[:TOPK]

    Candidate_ReducedSet = []

    for item in result:
        if voting_counts[item] >= len(X_vote) / 2.0:
            Candidate_ReducedSet.append(item)
    if len(Candidate_ReducedSet) > TOPK:
        random.shuffle(Candidate_ReducedSet)
        return Candidate_ReducedSet
    else:
        print 'False'
        return ReducedSet


def robustAdaptiveSearch(X, q, pro_fail, Edges, percent):
    global TOPK
    '''
    max_factor = Max_Verify(X, q, pro_fail)
    '''
    TOPK = 10
    while len(X) > (TOPK + 1):
        reduced_set = adaptiveReduce(X, q, Edges, percent)
        X = copy.deepcopy(reduced_set)
        print reduced_set
    return X


def main():
    for percent in numpy.arange(0.3, 1.1, 0.1):
        Edges = random.sample(BaseEdges, int(percent * len(BaseEdges)))

        random.shuffle(nodes)

        result = robustAdaptiveSearch(nodes, 0.1, 0.2, Edges, percent)

        print percent, result


if __name__ == "__main__":
    global nodes, BaseEdges, Matrix

    nodes, BaseEdges, Matrix = GenerateTestFile.simulant_dataset()

    candidate_edges = []
    for edge in BaseEdges:
        if edge[0] in nodes and edge[1] in nodes:
            candidate_edges.append(edge)

    BaseEdges = copy.deepcopy(candidate_edges)

    for re in range(1000):
        random.seed(time.time())
        time.sleep(0.2)
        main()
