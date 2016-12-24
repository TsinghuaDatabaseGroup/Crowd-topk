
import time
import copy
import random
import numpy
import math
from Deal_with_text_files import portrait, GenerateTestFile, writing_time
from Deal_with_text_files import mall_process, historyevents, portrait, statue
from Deal_with_text_files import write_to_files, varying_k, Gen_TwoStageHeap
global nodes, edges, Matrix, count_compare, set_sample_edges, original_edges


def Algorithm_1(nodes, NL):

    global count_compare

    delta = 0.1
    size_of_nodes = len(nodes)

    X = size_of_nodes / (math.log(1/delta, 2) * math.log(1/delta, 2))
    if X < 1:
        X = 1

    candidate_result = copy.deepcopy(nodes)
    for iteration_times in range(1, int(math.log(X, 2)) + 1):
        temporary = []
        for index in range(0, len(candidate_result), 2):
            # Only compare once for each edge in original_edges
            if (candidate_result[index], candidate_result[index+1]) in original_edges:
                count_compare += 1
                temporary.append(candidate_result[index])
            else:
                count_compare += 1
                temporary.append(candidate_result[index+1])

        candidate_result = copy.deepcopy(temporary)

    left = int(math.log(X, 2)) + 1
    right = int(math.log(size_of_nodes, 2)) + 1
    for iteration_times in range(left, right):
        temporary = []
        for index in range(0, len(candidate_result), 2):
            # Results in set_sample_edges is the aggregated results after N_Ls
            # comparisons
            if (candidate_result[index], candidate_result[index+1]) in set_sample_edges:
                count_compare += 3
                temporary.append(candidate_result[index])
            else:
                count_compare += 3
                temporary.append(candidate_result[index+1])

        candidate_result = copy.deepcopy(temporary)

    return candidate_result[0]


def Heapify(xlist, heapSize, index):
    global count_compare
    left = 2 * index + 1
    right = left + 1
    large = index
    if right < heapSize and (xlist[right], xlist[large]) in set_sample_edges:
        count_compare += 3
        large = right

    if left < heapSize and (xlist[left], xlist[large]) in set_sample_edges:
        count_compare += 3
        large = left

    if large != index:
        xlist[large], xlist[index] = xlist[index], xlist[large]
        Heapify(xlist, heapSize, large)


def BuildMaxHeap(xlist):
    heapSize = len(xlist)
    for i in range(heapSize / 2 - 1, -1, -1):
        Heapify(xlist, heapSize, i)


def HeapSort(xlist):
    global count_compare
    initial_list = copy.deepcopy(xlist)
    BuildMaxHeap(initial_list)
    result = []
    value_of_K = 10
    for xiter in range(value_of_K):
        result.append(initial_list[0])
        initial_list.remove(initial_list[0])
        Heapify(initial_list, len(initial_list), 0)

    print result


def TOPK_Algorithm(nodes):
    max_elements = []
    for i in range(0, len(nodes) - 1, 4):
        # We conduct stage 1 in this step
        max_elements.append(Algorithm_1(nodes[i:i + 4], 3))

    # We conduct stage 2 in this step
    HeapSort(max_elements)


if __name__ == "__main__":

    global nodes, edges, count_compare, set_sample_edges, original_edges
    # We set the N_L = 3, this function is the aggregated results after N_L
    # votes
    nodes, edges, Matrix = Gen_TwoStageHeap.simulant_dataset()

    # Only compare once for each edge in the set of original_edges
    original_nodes, original_edges = Gen_TwoStageHeap.simulant_dataset_original()

    for re in range(1000):
        count_compare = 0
        random.shuffle(nodes)
        set_sample_edges = set(edges)
        TOPK_Algorithm(nodes)
        print count_compare
