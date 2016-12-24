
import sys
sys.path.append("..")
import time
import random
import copy
import numpy
from evaluate_metric import acc
from collections import Counter
from text_files import portrait, GenerateTestFile, historyevents, statue, mall_process

global nodes, edges, Matrix, BaseMatrix, range_number


def pre_process(sample_edges):
    global nodes, edges, Matrix, range_number
    Matrix = {} 
    Matrix = copy.deepcopy(BaseMatrix)
    set_sample_edges = set(sample_edges)
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if (nodes[i], nodes[j]) not in set_sample_edges:
                Matrix[(nodes[i], nodes[j])] = 0
                
def computation_period(ProRecord):
    notes = {}
    period_each_node = {}
    results = {}
    
    for each_dict in ProRecord[-10:]:
        for each_key in each_dict.keys():
            if each_key not in notes:
                notes[each_key] = []
                notes[each_key].append(each_dict[each_key] )
            else:
                notes[each_key].append(each_dict[each_key] )
    
    for key in notes.keys():
        array = notes[key]
        candidate = Counter(array).most_common(1)
        
        candidate_node = candidate[0][0]
        candidate_times = candidate[0][1]
        
        if candidate_times == 1:
            results[key] = array[-1]
        else:
            right_index = 0
            for i in range(len(array) - 1, 0, -1):
                if array[i] == candidate_node:
                    right_index = i
                    break
            for i in range(right_index - 1, 0, -1):
                if array[i] == candidate_node:
                    left_index = i
                    break
            
            period = right_index - left_index
            period_each_node[key] = period
            results[key] = sum(array[left_index:right_index]) / (period)
    
    return results


def PageRank_Ranking(number_of_edges, iteration_times=1):
    global nodes, edges, Matrix
    d = {}
    pro = {}
    weight = {}
    ProRecord = []
    used_edges = []

    for edge in edges:
        used_edges.append((edge[1], edge[0]))

    for item in Matrix:
        weight[(item[1], item[0])] = Matrix[item]

    for node in nodes:
        d[node] = 0
        pro[node] = 1 / float(len(nodes))

    for edge in used_edges:
        d[edge[0]] += weight[edge]

    for node in nodes:
        if d[node] == 0:
            weight[(node, node)] = 1

    copy_pro = copy.deepcopy(pro)
    ProRecord.append(copy_pro)

    for xiter in range(iteration_times):
        print xiter
        for node in nodes:
            pro[node] = 0
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if i != j and d[nodes[j]] != 0:
                    pro[nodes[i]] = pro[nodes[i]] + (float(weight[(nodes[j], nodes[i])]) / (
                        d[nodes[j]])) * ProRecord[-1][nodes[j]]

        copy_pro = copy.deepcopy(pro)
        ProRecord.append(copy_pro)
    
    final_res = computation_period(ProRecord)

    for item in ProRecord:
        print item

    sorted_score = sorted(final_res.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    result = []
    for item in sorted_score:
        result.append(item[0])
        print item

    print result
    print Counter(result).most_common(5)

def main():
    for percent in numpy.arange(0.1, 1.1, 0.1):
        sample_edges = random.sample(edges, int(percent * len(edges)))
        pre_process(sample_edges)
        random.shuffle(nodes)
        PageRank_Ranking(int(percent * 100), iteration_times = 20)

def repeat_main():
    for xiter in range(1000):
        print "SIGMODPageRank", xiter
        main()

if __name__ == "__main__":
    global nodes, edges, Matrix, range_number
    nodes, edges, BaseMatrix = GenerateTestFile.paper_dataset()

    repeat_main()

