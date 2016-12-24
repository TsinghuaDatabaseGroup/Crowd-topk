
import sys
sys.path.append("..")
import random
import math
import copy
from scipy.optimize import minimize
import numpy
import sys
sys.setrecursionlimit(1000000)
from Deal_with_text_files import portrait, GenerateTestFile, statue, historyevents
from Deal_with_text_files import write_to_files, mall_process, RecordFiles

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


def BTL_model(x):

    return 1 / (1 + math.exp(-1 * x))


def computation_Y(i, j):
    global nodes, edges, Matrix

    regular = 0.1

    if j < i:
        pro = float(Matrix[(j, i)]) / \
            (Matrix[(i, j)] + Matrix[(j, i)] + 0.00001)
        return math.log(((pro + regular) / (1 - pro + regular)), math.e)

    elif j > i:
        pro = float(Matrix[(j, i)]) / \
            (Matrix[(i, j)] + Matrix[(j, i)] + 0.00001)
        return math.log((pro + regular) / (1 - pro + regular), math.e)


def f_function(f):
    global nodes, edges, Matrix
    SUM = 0
    set_edges = set(edges)
    for i in range(len(f)):
        for j in range(len(f)):
            if i != j and ((i, j) in set_edges or (j, i) in set_edges):
                SUM += math.pow(((f[j] - f[i]) - computation_Y(i, j)), 2)
    return SUM


def test_likelihood(number_of_edges):
    global nodes, edges, Matrix
    x0 = []
    for i in range(len(nodes)):
        x0.append(random.random())
    res = minimize(f_function, x0, method='L-BFGS-B', options={"maxiter": 100})

    score = {}
    for i in range(len(nodes)):
        score[nodes[i]] = res.x[i]

    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

    result = []

    for item in sorted_score:
        result.append(item[0])

    print result

    RecordFiles.record_results('HodgeRank', result, number_of_edges)


def main():
    for percent in numpy.arange(0.1, 1.1, 0.1):
        sample_edges = random.sample(edges, int(percent * len(edges)))
        pre_process(sample_edges)
        test_likelihood(int(percent * 100))


def Redo():
    for re in range(1000):
        print "HodgeRank", re
        main()

if __name__ == "__main__":

    global nodes, edges, Matrix, BaseMatrix
    nodes, edges, BaseMatrix = mall_process.mall_process()
    Redo()
