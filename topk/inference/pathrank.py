
import sys
sys.path.append("..")
import random
import networkx as nx
import numpy
import time
from Deal_with_text_files import GenerateTestFile, portrait, mall_process, write_to_files,\
    historyevents, statue, AddedTestFile, RecordFiles, writing_time
global nodes, edges, Matrix


def pre_process():
    global nodes, edges, Matrix
    nodes, edges, Matrix = GenerateTestFile.simulant_dataset()


def PathRank(nodes, sample_edges, percent):
    random.shuffle(nodes)
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(sample_edges)
    candidate_set = []

    for edge in sample_edges:
        G.add_edge(edge[0], edge[1])
        if nx.is_directed_acyclic_graph(G):
            continue
        else:
            G.remove_edge(edge[0], edge[1])

    print nx.is_directed_acyclic_graph(G)

    for nodeA in nodes:
        print nodeA
        FalseFlag = False
        for nodeB in nodes:
            if nodeA != nodeB and nx.has_path(G, nodeB, nodeA):
                paths = nx.all_simple_paths(G, nodeB, nodeA)
                for item in paths:
                    if len(item) >= 10:
                        FalseFlag = True
                        break

        if FalseFlag == False:
            candidate_set.append(nodeA)

    print len(candidate_set)
    print 'result set',  candidate_set


def Test():

    for percent in numpy.arange(0.1, 1.1, 0.1):

        print percent
        sample_edges = random.sample(edges, int(percent * len(edges)))
        random.shuffle(nodes)
        PathRank(nodes, sample_edges, int(percent * 100))


def Average_Recall():
    pre_process()
    for re in range(1000):
        print 'PathRank', re
        Test()

Average_Recall()
