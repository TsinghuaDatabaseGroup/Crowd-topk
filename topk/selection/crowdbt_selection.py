
import sys
from numpy import nan, Inf
sys.path.append("..")
import numpy
import time
import scipy.stats
import random
import heapq
from math import exp as e
from math import pow as pow
from InferenceForSelection import sig_local, Hybrid, MLECrowdBT, sig_iterative, ELO
from InferenceForSelection import SSRW
from text_files import mall_process, historyevents, statue, portrait, Record_Choosen_Pairs
global score, variance, worker_quality, number_of_worker
global nodes, edges, Matrix, number_of_questions, Asked_Pairs

global Count_Node, number_in_round


def Initial_Process():
    global score, variance, worker_quality
    global nodes, edges, Matrix, number_of_worker

    nodes, edges, Matrix = mall_process.mall_process()

    score = {}
    variance = {}
    worker_quality = {}

    number_of_worker = 10
    for number_of_worker in range(number_of_worker):
        worker_quality[number_of_worker] = [10, 1]

    for node in nodes:
        score[node] = 0
        variance[node] = 1


def positive(arrayA, arrayB):

    resultA = []
    resultB = []

    for i in range(len(arrayA)):
        if arrayA[i] * arrayB[i] > 0:
            resultA.append(arrayA[i])
            resultB.append(arrayB[i])

    return resultA, resultB


'The winner is i'


def update_score_winner(i, j, k):

    inner_factor_1 = worker_quality[k][
        0] * e(score[i]) / (worker_quality[k][0] * e(score[i]) + worker_quality[k][1] * e(score[j]))

    inner_factor_2 = e(score[i]) / (e(score[i]) + e(score[j]))

    result = score[i] + pow(variance[i], 2) * (inner_factor_1 - inner_factor_2)

    return result


def update_score_loser(i, j, k):

    inner_factor_1 = worker_quality[k][
        0] * e(score[i]) / (worker_quality[k][0] * e(score[i]) + worker_quality[k][1] * e(score[j]))

    inner_factor_2 = e(score[i]) / (e(score[i]) + e(score[j]))

    result = score[j] - pow(variance[j], 2) * (inner_factor_1 - inner_factor_2)

    return result


def update_variance_winner(i, j, k):

    inner_first_para_upper = worker_quality[k][
        0] * worker_quality[k][1] * e(score[i]) * e(score[j])

    inner_first_para_lower = pow(
        (worker_quality[k][0] * e(score[i]) + worker_quality[k][1] * e(score[j])), 2)

    inner_second_para = e(
        score[i]) * e(score[j]) / pow(e(score[i]) + e(score[j]), 2)

    max_candidate_one = 1 + \
        pow(variance[i], 2) * (inner_first_para_upper /
                               inner_first_para_lower - inner_second_para)

    max_candidate_two = 0.0001

    result = pow(variance[i], 2) * max(max_candidate_one, max_candidate_two)

    return result


def update_variance_lose(i, j, k):

    inner_first_para_upper = worker_quality[k][
        0] * worker_quality[k][1] * e(score[i]) * e(score[j])

    inner_first_para_lower = pow(
        (worker_quality[k][0] * e(score[i]) + worker_quality[k][1] * e(score[j])), 2)

    inner_second_para = e(
        score[i]) * e(score[j]) / pow(e(score[i]) + e(score[j]), 2)

    max_candidate_one = 1 + \
        pow(variance[j], 2) * (inner_first_para_upper /
                               inner_first_para_lower - inner_second_para)

    max_candidate_two = 0.0001

    result = pow(variance[j], 2) * max(max_candidate_one, max_candidate_two)

    return result


def computation_C1_C2(i, j):

    inner_para_first = e(score[i]) / (e(score[i]) + e(score[j]))

    inner_para_second = 0.5 * (pow(variance[i], 2) + pow(variance[j], 2))

    inner_para_third = e(
        score[i]) * e(score[j]) * (e(score[j]) - e(score[i])) / pow(e(score[i]) + e(score[j]), 3)

    C1 = inner_para_first + inner_para_second * inner_para_third
    C2 = 1 - C1

    return C1, C2


def computation_C(i, j, k):

    C1, C2 = computation_C1_C2(i, j)

    C = (C1 * worker_quality[k][0] + C2 * worker_quality[k]
         [1]) / (worker_quality[k][0] + worker_quality[k][1])

    return C


def computation_first_order_worker_quality(i, j, k):

    C1, C2 = computation_C1_C2(i, j)
    C = computation_C(i, j, k)

    inner_para_upper = C1 * (worker_quality[k][0] + 1) * worker_quality[k][
        0] + C2 * worker_quality[k][0] * worker_quality[k][1]

    inner_para_lower = C * \
        (worker_quality[k][0] + worker_quality[k][1] + 1) * \
        (worker_quality[k][0] + worker_quality[k][1])

    first_order_worker = inner_para_upper / float(inner_para_lower)

    return first_order_worker


def computation_second_order_worker_quality(i, j, k):

    C1, C2 = computation_C1_C2(i, j)
    C = computation_C(i, j, k)

    para_upper_one = C1 * \
        (worker_quality[k][0] + 2) * \
        (worker_quality[k][0] + 1) * worker_quality[k][0]
    para_upper_two = C2 * \
        (worker_quality[k][0] + 1) * \
        worker_quality[k][0] * worker_quality[k][1]

    para_upper = para_upper_one + para_upper_two

    para_lower = C * (worker_quality[k][0] + worker_quality[k][1] + 2) *\
        (worker_quality[k][0] + worker_quality[k][1] + 1) * \
        (worker_quality[k][0] + worker_quality[k][1])

    second_order_worker = para_upper / float(para_lower)

    return second_order_worker


def update_worker_para(i, j, k):

    first_order = computation_first_order_worker_quality(i, j, k)

    second_order = computation_second_order_worker_quality(i, j, k)

    worker_quality_first = (
        (first_order - second_order) * first_order) / (second_order - pow(first_order, 2))

    worker_quality_second = (first_order - second_order) * \
        (1 - first_order) / (second_order - pow(first_order, 2))

    return worker_quality_first, worker_quality_second


def select_pair_with_max_information():
    from math import exp as e
    start = time.time()
    estimated_entropy = {}

    esti_not_topk = []
    if len(Asked_Pairs) >= 0.1*len(edges):
        esti_not_topk = heapq.nsmallest(
            int(len(nodes) * 0.5), score, key=score.get)

    threshold = (number_in_round / float(len(nodes))) * 2.0

    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):

            if nodes[i] in esti_not_topk or nodes[j] in esti_not_topk:
                for k_iter in range(number_of_worker):
                    estimated_entropy[(nodes[i], nodes[j], k_iter)] = -Inf
                continue

            if Count_Node[nodes[i]] >= threshold or Count_Node[nodes[j]] >= threshold:
                for k_iter in range(number_of_worker):
                    estimated_entropy[(nodes[i], nodes[j], k_iter)] = -Inf
                continue

            if (nodes[i], nodes[j]) in Asked_Pairs or (nodes[j], nodes[i]) in Asked_Pairs:
                for k_iter in range(number_of_worker):
                    estimated_entropy[(nodes[i], nodes[j], k_iter)] = -Inf
                continue

            for k in range(number_of_worker):

                'The case of i is superior to j'
                posterior_score_i = update_score_winner(i, j, k)
                posterior_variance_i = update_variance_winner(i, j, k)**0.5

                posterior_score_j = update_score_loser(i, j, k)
                posterior_variance_j = update_variance_lose(i, j, k)**0.5

                posterior_worker_first, posterior_worker_second = update_worker_para(
                    i, j, k)

                'Computation of the entropy if i wins'
                post_distribution_i = numpy.random.normal(
                    posterior_score_i, posterior_variance_i, 100)
                post_distribution_j = numpy.random.normal(
                    posterior_score_j, posterior_variance_j, 100)
                post_distribution_k = numpy.random.beta(
                    posterior_worker_first, posterior_worker_second, 100)

                prior_distribution_i = numpy.random.normal(
                    score[i], variance[i], 100)
                prior_distribution_j = numpy.random.normal(
                    score[j], variance[j], 100)
                prior_distribution_k = numpy.random.beta(
                    worker_quality[k][0], worker_quality[k][1], 100)

                list_post_distribution_i, list_prior_distribution_i = positive(
                    post_distribution_i, prior_distribution_i)
                list_post_distribution_j, list_prior_distribution_j = positive(
                    post_distribution_j, prior_distribution_j)

                distance_one = scipy.stats.entropy(
                    list_post_distribution_i, list_prior_distribution_i)
                distance_two = scipy.stats.entropy(
                    list_post_distribution_j, list_prior_distribution_j)
                distance_three = scipy.stats.entropy(
                    post_distribution_k, prior_distribution_k)

                accuracy_of_k = random.betavariate(
                    worker_quality[k][0], worker_quality[k][1])

                probability_i_win = accuracy_of_k * e(score[i]) / (e(score[i]) + e(score[j])) + (
                    1 - accuracy_of_k) * e(score[j]) / (e(score[i]) + e(score[j]))

                PART_ONE = probability_i_win * \
                    (distance_one + distance_two + distance_three)

                'The case of j is superior to i'
                'update the posterior para for i,j,k when i is the loser'
                posterior_score_j = update_score_winner(j, i, k)
                posterior_variance_j = update_variance_winner(j, i, k)**0.5

                posterior_score_i = update_score_loser(j, i, k)
                posterior_variance_i = update_variance_lose(j, i, k)**0.5

                posterior_worker_first, posterior_worker_second = update_worker_para(
                    j, i, k)

                'Computation of the entropy if j wins'
                post_distribution_i = numpy.random.normal(
                    posterior_score_i, posterior_variance_i, 100)
                post_distribution_j = numpy.random.normal(
                    posterior_score_j, posterior_variance_j, 100)
                post_distribution_k = numpy.random.beta(
                    posterior_worker_first, posterior_worker_second, 100)

                prior_distribution_i = numpy.random.normal(
                    score[i], variance[i], 100)
                prior_distribution_j = numpy.random.normal(
                    score[j], variance[j], 100)
                prior_distribution_k = numpy.random.beta(
                    worker_quality[k][0], worker_quality[k][1], 100)

                list_post_distribution_i, list_prior_distribution_i = positive(
                    post_distribution_i, prior_distribution_i)
                list_post_distribution_j, list_prior_distribution_j = positive(
                    post_distribution_j, prior_distribution_j)

                distance_one = scipy.stats.entropy(
                    list_post_distribution_i, list_prior_distribution_i)
                distance_two = scipy.stats.entropy(
                    list_post_distribution_j, list_prior_distribution_j)
                distance_three = scipy.stats.entropy(
                    post_distribution_k, prior_distribution_k)

                accuracy_of_k = random.betavariate(
                    worker_quality[k][0], worker_quality[k][1])

                probability_j_wins = accuracy_of_k * e(score[j]) / (e(score[i]) + e(score[j])) + (
                    1 - accuracy_of_k) * e(score[i]) / (e(score[i]) + e(score[j]))

                PART_TWO = probability_j_wins * \
                    (distance_one + distance_two + distance_three)

                estimated_entropy[(i, j, k)] = PART_ONE + PART_TWO

    try:
        max_value = max(estimated_entropy.values())
        can_array = []
        for key in estimated_entropy.keys():
            if estimated_entropy[key] == max_value:
                can_array.append(key)
        selected_triplet = random.choice(can_array)

    except Exception, e:
        selected_edge = random.choice(list(set(edges) - set(Asked_Pairs)))
        selected_triplet = (selected_edge[0], selected_edge[1], 0)

    if Count_Node[selected_triplet[0]] > threshold or Count_Node[selected_triplet[1]] > threshold:
        selected_edge = random.choice(list(set(edges) - set(Asked_Pairs)))
        selected_triplet = (selected_edge[0], selected_edge[1], 0)

    end = time.time()
    print 'computation of the entropy', (end - start)
    return selected_triplet


def Copeland(used_nodes, used_pairs, percent):

    rank_score = {}
    for node in used_nodes:
        rank_score[node] = 0

    for edge in used_pairs:
        rank_score[edge[0]] += 1
        rank_score[edge[1]] -= 1

    sorted_rank_score = sorted(
        rank_score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

    result = []
    for item in sorted_rank_score:
        result.append(item[0])


def selection_process():

    global number_of_questions, Asked_Pairs, Count_Node, number_in_round

    for percent in numpy.arange(0.1, 1.1, 0.1):

        print 'round', percent
        Asked_Pairs = []
        Count_Node = {}

        for node in nodes:
            Count_Node[node] = 0

        number_in_round = int(percent * len(edges))

        for xe in range(number_in_round):

            selected_triplet = select_pair_with_max_information()

            print selected_triplet

            pair = (selected_triplet[0], selected_triplet[1])
            worker_k = selected_triplet[2]

            if pair in edges:
                winner = pair[0]
                loser = pair[1]
            else:
                winner = pair[1]
                loser = pair[0]

            score[winner] = update_score_winner(winner, loser, worker_k)
            score[loser] = update_score_loser(winner, loser, worker_k)

            variance[winner] = pow(
                update_variance_winner(winner, loser, worker_k), 0.5)
            variance[loser] = pow(
                update_variance_lose(winner, loser, worker_k),  0.5)

            worker_para = update_worker_para(winner, loser, worker_k)
            worker_quality[worker_k][0] = worker_para[0]
            worker_quality[worker_k][1] = worker_para[1]

            Asked_Pairs.append((winner, loser))
            Count_Node[winner] += 1
            Count_Node[loser] += 1

        trans_Matrix = {}

        for edge in Asked_Pairs:
            trans_Matrix[edge] = Matrix[edge]

#         sig_iterative.Iterative_Ranking('CrowdBT_10_1', nodes, Asked_Pairs, trans_Matrix, int(percent * 100))
#         Record_Choosen_Pairs.record_choosen_pairs('CrowdBT_10_1', percent, Asked_Pairs)


if __name__ == "__main__":

    for xre in range(1000):

        print xre

        Initial_Process()

        selection_process()
