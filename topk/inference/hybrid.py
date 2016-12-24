

import Text_Files
import portrait
import mall_process
import statue
import historyevents
from scipy.stats import norm
import math
import random
import copy
from scipy import optimize
from RatingBased import GenCompare
from Deal_with_text_files import varying_k, write_to_files, ACC
import GenRate

global nodes, edges, Matrix, id_truth, id_vote, already_used_edges
global mapping, reverse_mapping


def Load_Rating_Comparison_Dataset():
    id_truth_choice, id_voted_choice = Text_Files.load_portrait_dataset()
    nodes, edges, Matrix, mapping = portrait.last50()
    transfered_id_truth = {}
    transfered_id_vote = {}
    for key in id_truth_choice.keys():
        if key in mapping:
            transfered_id_truth[mapping[key]] = id_truth_choice[key]
            transfered_id_vote[mapping[key]] = id_voted_choice[key]

    return nodes, edges, Matrix, transfered_id_truth, transfered_id_vote


def Load_Rating_Dataset():
    id_truth_choice, id_voted_choice = Text_Files.load_statue_dataset()
    nodes, edges, Matrix = statue.statue_process()
    transfered_id_truth = {}
    transfered_id_vote = {}
    for key in id_truth_choice.keys():
        transfered_id_truth[key] = id_truth_choice[key]
        transfered_id_vote[key] = id_voted_choice[key]

    return nodes, edges, Matrix, transfered_id_truth, transfered_id_vote


def The_First_Rating_Stage():
    global nodes, edges, Matrix, id_truth, id_vote
    nodes, edges, Matrix, id_truth, id_vote = Load_Rating_Dataset()
    category = 2
    candidate = []
    for key in id_vote.keys():
        if id_vote[key] <= category:
            candidate.append(key)
    return candidate


def cumulative_distribution(mu, delta, x):
    factor1 = x - mu
    factor2 = math.sqrt(2 * delta * delta)
    factor3 = 0.5 * (1 + math.erf(factor1 / factor2))
    return factor3


def likelihood(s):
    global already_used_edges, mapping
    SUM = 0
    min_value = 0.00001
    for edge in already_used_edges:
        SUM += math.log10(cumulative_distribution(
            (s[mapping[edge[0]]] - s[mapping[edge[1]]]), 2, 0) + min_value)

    return SUM


def test_likelihood(candidate, percent):

    global mapping, reverse_mapping
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


def The_Second_Comparison_Stage():
    global nodes, edges, Matrix, id_truth, id_vote, already_used_edges
    candidate = The_First_Rating_Stage()
    print candidate
    print len(candidate)

    y_value = float(len(nodes) * (len(nodes) - 1) / 2)
    candidate_edges = []
    for edge in edges:
        if edge[0] in candidate and edge[1] in candidate:
            candidate_edges.append(edge)

    Total_Questions = len(candidate_edges) + len(nodes)
    fraction = Total_Questions / float(y_value)

    already_used_edges = copy.deepcopy(candidate_edges)

    test_likelihood(candidate, int(fraction * 100))

    print(len(nodes) + len(already_used_edges)) / y_value


if __name__ == "__main__":

    for index in range(1000):

        The_Second_Comparison_Stage()
