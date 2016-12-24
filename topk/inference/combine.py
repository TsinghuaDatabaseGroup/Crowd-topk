

import Text_Files
import portrait
import mall_process
import statue
import historyevents
from scipy.stats import norm
import math
import random
import operator
import copy
from scipy import optimize
from Deal_with_text_files import write_to_files, ACC
global nodes, edges, Matrix, id_truth, id_vote, already_used_edges
global mapping, reverse_mapping, Rating_Convert, candidiate
global BaseMatrix


def Load_Rating_Comparison_Dataset():
    global BaseMatrix
    id_truth_choice, id_voted_choice = Text_Files.load_portrait_dataset()
    nodes, edges, Matrix, mapping = portrait.last50()

    BaseMatrix = copy.deepcopy(Matrix)

    transfered_id_truth = {}
    transfered_id_vote = {}
    for key in id_truth_choice.keys():
        if key in mapping:
            transfered_id_truth[mapping[key]] = id_truth_choice[key]
            transfered_id_vote[mapping[key]] = id_voted_choice[key]

    return nodes, edges, Matrix, transfered_id_truth, transfered_id_vote

'''statue,mall'''


def Load_Rating_Dataset():
    global BaseMatrix
    id_truth_choice, id_voted_choice = Text_Files.load_mall_dataset()
    nodes, edges, Matrix = mall_process.mall_process()

    BaseMatrix = copy.deepcopy(Matrix)

    transfered_id_truth = {}
    transfered_id_vote = {}
    for key in id_truth_choice.keys():
        transfered_id_truth[key] = id_truth_choice[key]
        transfered_id_vote[key] = id_voted_choice[key]

    return nodes, edges, Matrix, transfered_id_truth, transfered_id_vote


def c(n, k):
    if k == 0:
        return 1
    else:
        return reduce(operator.mul, range(n - k + 1, n + 1)) / reduce(operator.mul, range(1, k + 1))


def Selection():
    global nodes, edges, Matrix, id_truth, id_vote
    nodes, edges, Matrix, id_truth, id_vote = Load_Rating_Dataset()

    for itemA in nodes:
        for itemB in nodes:
            if (itemA, itemB) not in Matrix:
                Matrix[(itemA, itemB)] = 0

    candidate = []
    for key in id_vote.keys():
        if id_vote[key] <= 5:
            candidate.append(key)
    return candidate


def cumulative_distribution(x, mu=0, delta=1):
    factor1 = x - mu
    factor2 = math.sqrt(2 * delta * delta)
    factor3 = 0.5 * (1 + math.erf(factor1 / factor2))
    return factor3


def likelihood(s):
    global nodes, Matrix, id_vote, mapping, Rating_Convert, candidate

    SUM = 0
    min_value = 0.00001
    for i in xrange(len(candidate)):
        for j in xrange(i+1, len(candidate)):
            if i != j and (Matrix[(i, j)] != 0 or Matrix[(j, i)] != 0):
                factor1 = math.log10(
                    c(Matrix[(i, j)] + Matrix[(j, i)], Matrix[(i, j)]) + min_value)
                factor2 = math.log10(
                    cumulative_distribution(s[i]-s[j]) + min_value) * Matrix[(i, j)]
                factor3 = math.log10(
                    cumulative_distribution(s[j]-s[i]) + min_value) * Matrix[(j, i)]
                SUM += (factor1 + factor2 + factor3)

    for i in xrange(len(candidate)):
        SUM += (cumulative_distribution(Rating_Convert[(id_vote[nodes[i]] + 1)] - s[nodes[i]])
                - cumulative_distribution(Rating_Convert[id_vote[nodes[i]]] - s[nodes[i]]))

    return -1*SUM


def test_likelihood(percent):

    global mapping, reverse_mapping, candidate
    mapping = {}
    reverse_mapping = {}
    count = 0
    for item in candidate:
        mapping[item] = count
        reverse_mapping[count] = item
        count += 1

    x0 = []
    for item in xrange(len(candidate)):
        x0.append(random.random())
    res = optimize.minimize(
        likelihood, x0, method='BFGS', options={"maxiter": 100})
    score = {}
    for i in xrange(len(candidate)):
        score[reverse_mapping[i]] = res.x[i]
    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result = []
    for item in sorted_score:
        print item
        result.append(item[0])

    print len(result)


def Comparison():
    global nodes, edges, Matrix, id_truth, id_vote, already_used_edges, Rating_Convert, candidate
    global BaseMatrix
    candidate = Selection()

    Rating_Convert = [0, 1, 2, 3, 4, 5]
    percent = 0.8
    left_length = int(
        (len(nodes) * (len(nodes) - 1) / 2) * percent) - len(nodes)

    if left_length <= len(edges):
        already_used_edges = random.sample(edges, left_length)
    else:
        already_used_edges = copy.deepcopy(edges)

    for edge in edges:
        if edge in already_used_edges:
            Matrix[edge] = BaseMatrix[edge]
        else:
            Matrix[edge] = 0

    test_likelihood(int(percent * 100))


if __name__ == "__main__":
    for index in range(1000):
        Comparison()
