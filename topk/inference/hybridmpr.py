

import Text_Files
import Text_Files_Full
import portrait
import mall_process
import statue
import historyevents
from scipy.stats import norm
import math
import random
import copy
from scipy import optimize
from Deal_with_text_files import write_to_files, ACC

global nodes, edges, Matrix, id_truth, id_vote, already_used_edges
global mapping, reverse_mapping
global candidate, id_array
global id_rating
global w


def Load_Rating_Comparison_Dataset():
    id_truth_choice, id_voted_choice = Text_Files.load_portrait_dataset()
    id_array_choice = Text_Files_Full.portrait_dataset()
    nodes, edges, Matrix, mapping = portrait.last50()

    transfered_id_truth = {}
    transfered_id_vote = {}
    transfered_id_array = {}

    for key in id_truth_choice.keys():
        if key in mapping:
            transfered_id_truth[mapping[key]] = id_truth_choice[key]
            transfered_id_vote[mapping[key]] = id_voted_choice[key]
            transfered_id_array[mapping[key]] = id_array_choice[key]

    return nodes, edges, Matrix, transfered_id_truth, transfered_id_vote, transfered_id_array


def Load_Rating_Dataset():
    id_truth_choice, id_voted_choice = Text_Files.load_statue_dataset()
    id_array_choice = Text_Files_Full.statue_dataset()
    nodes, edges, Matrix = statue.statue_process()
    transfered_id_truth = {}
    transfered_id_vote = {}
    transfered_id_array = {}

    for key in id_truth_choice.keys():
        transfered_id_truth[key] = id_truth_choice[key]
        transfered_id_vote[key] = id_voted_choice[key]
        transfered_id_array[key] = id_array_choice[(key + 1)]

    return nodes, edges, Matrix, transfered_id_truth, transfered_id_vote, transfered_id_array


def The_First_Rating_Stage():
    global nodes, edges, Matrix, id_truth, id_vote
    nodes, edges, Matrix, id_truth, id_vote, id_array = Load_Rating_Dataset()

    for nodeA in nodes:
        for nodeB in nodes:
            if (nodeA, nodeB) not in Matrix:
                Matrix[(nodeA, nodeB)] = 0

    category = 2

    candidate = []
    for key in id_vote.keys():
        if id_vote[key] <= category:
            candidate.append(key)
    return candidate, id_array


def The_Second_Comparison_Stage():
    global nodes, edges, Matrix, id_truth, id_vote, already_used_edges
    global candidate, id_array
    candidate, id_array = The_First_Rating_Stage()
    print candidate
    print len(candidate)

    all_number_candidate = (len(candidate) * (len(candidate) - 1)) / 2
    all_number_nodes = (len(nodes) * (len(nodes) - 1)) / 2
    print 'The fraction of the candidate is:', all_number_candidate / float(all_number_nodes)

    already_used_edges = []
    for edge in edges:
        if edge[0] in candidate and edge[1] in candidate:
            already_used_edges.append(edge)


def computation_of_r():
    global id_rating
    id_rating = {}
    for node in candidate:
        if len(id_array[node]) == 0:
            id_rating[node] = 0.5
        else:
            total_count = 0
            array = id_array[node]
            xarray = []
            for item in array:
                xarray.append(item / 5.0)
                total_count += item

            first_para = 0
            for item in xarray:
                first_para += item

            second_para = float(5 * total_count)
            third_para = 1 / 10.0
            result = first_para / second_para - third_para
            id_rating[node] = result


def computation_of_w():
    global w
    w = {}
    min_value = 0.0001
    for nodeA in candidate:
        for nodeB in candidate:
            w[(nodeA, nodeB)] = 0

    for nodeA in candidate:
        for nodeB in candidate:
            if Matrix[(nodeA, nodeB)] + Matrix[(nodeB, nodeA)] == 0 and id_rating[nodeA] < id_rating[nodeB]:
                w[(nodeA, nodeB)] = 1
            elif Matrix[(nodeA, nodeB)] + Matrix[(nodeB, nodeA)] == 0 and id_rating[nodeA] > id_rating[nodeB]:
                w[(nodeA, nodeB)] = 0
            else:
                w[(nodeA, nodeB)] = (Matrix[(nodeA, nodeB)] + min_value) / \
                    (Matrix[(nodeA, nodeB)] +
                     Matrix[(nodeB, nodeA)] + 2 * min_value)

    for nodeA in candidate:
        xsum = 0
        for nodeB in candidate:
            xsum += nodeB
        w[nodeA] = xsum


def MPR():
    MPR_Score = {}
    for i in range(len(candidate)):
        MPR_Score[candidate[i]] = random.random()

    for iter in range(10):
        for i in range(len(candidate)):
            xsum_one = 0
            for j in range(len(candidate)):
                if w[candidate[j]] != 0:
                    xsum_one += (w[(candidate[i], candidate[j])] /
                                 w[candidate[j]]) * MPR_Score[candidate[j]]
            xsum_one = xsum_one * 0.6

            xsum_two = 0
            for j in range(len(candidate)):
                xsum_two += id_rating[candidate[j]]

            first_para = xsum_one
            second_para = 0.4 * id_rating[candidate[i]] / xsum_two
            MPR_Score[candidate[i]] = first_para + second_para

    sorted_score = sorted(
        MPR_Score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result = []
    for item in sorted_score:
        print item
        result.append(item[0])

    Total_Questions = len(nodes) + (len(candidate) * (len(candidate) - 1)) / 2
    ALL_PAIRS = len(nodes) * (len(nodes) - 1) / 2
    fraction = Total_Questions / float(ALL_PAIRS)


if __name__ == "__main__":
    for re_iter in range(1000):
        The_Second_Comparison_Stage()
        computation_of_r()
        computation_of_w()
        MPR()
