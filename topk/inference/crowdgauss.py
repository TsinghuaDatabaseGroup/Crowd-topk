
import sys
sys.path.append("..")
import random
import math
import time
sys.setcheckinterval(10000)
from scipy.stats import norm
import numpy as np
import copy
from scipy import optimize
from Deal_with_text_files import portrait, GenerateTestFile, write_to_files, historyevents, \
    statue, mall_process, AddedTestFile, RecordFiles
global nodes, edges, M, BaseMatrix, already_used_edges

already_used_edges = []


def likelihood(s):
    global called_count, already_used_edges
    global nodes, M
    SUM = 0
    min_value = 0.00001
    for edge in already_used_edges:
        SUM += M[edge] * \
            math.log10(norm.cdf(s[edge[0]] - s[edge[1]]) + min_value)

    return -1 * SUM


def test_likelihood(percent):
    x0 = []
    for item in xrange(len(nodes)):
        x0.append(random.random())
    res = optimize.minimize(
        likelihood, x0, method='BFGS', options={"maxiter": 100})
    score = {}
    for i in xrange(len(nodes)):
        score[nodes[i]] = res.x[i]
    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result = []
    for item in sorted_score:
        result.append(item[0])
    print percent, result


def main():
    global nodes, edges, M, already_used_edges
    left_edges = copy.deepcopy(edges)
    for percent in np.arange(0.1, 1.1, 0.1):
        if len(left_edges) >= int(len(edges) * 0.1):
            edges_round = random.sample(left_edges, int(len(edges) * 0.1))
        else:
            edges_round = left_edges
        already_used_edges.extend(edges_round)
        left_edges = list(set(left_edges) - set(edges_round))
        test_likelihood(percent)


def Average_Recall():
    global nodes, edges, M, BaseMatrix
    nodes, edges, M = statue.statue_process()

    for re in xrange(1000):
        print 'AdaptivePolling', re
        main()


if __name__ == "__main__":

    Average_Recall()
