
import sys
sys.path.append("..")
import random
import math
from scipy.stats import norm
import copy
import numpy as np
from scipy.optimize import minimize
from Deal_with_text_files import portrait, GenerateTestFile, statue
from Deal_with_text_files import write_to_files, mall_process, historyevents, RecordFiles
global nodes, edges, Matrix, sample_edges
global result, range_number


def pre_process():
    global nodes, edges, Matrix, range_number
    nodes, edges, Matrix = mall_process.mall_process()


def CrowdBT_optimization(s):
    global result
    SUM = 0
    yitak = 0.9
    balance = 0.000001
    try:
        for edge in sample_edges:
            i = edge[0]
            j = edge[1]

            factor1 = yitak * \
                math.exp(s[i]) / (math.exp(s[i]) + math.exp(s[j]) + balance)
            factor2 = (
                1 - yitak) * math.exp(s[j]) / (math.exp(s[i]) + math.exp(s[j]) + balance)
            SUM += math.log10(factor1 + factor2)

        for i in range(len(nodes)):
            factor3 = math.exp(
                1.0) / (math.exp(1.0) + math.exp(s[i]) + balance)
            factor4 = math.exp(
                s[i]) / (math.exp(1.0) + math.exp(s[i]) + balance)
            SUM += 0.5 * (math.log10(factor3) + math.log10(factor4))
    except Exception, e:
        return -1 * SUM

    return -1 * SUM


def optimization_crowdbt(percent):
    x0 = [1.0] * len(nodes)
    res = minimize(
        CrowdBT_optimization, x0, method='BFGS', options={"maxiter": 100})
    print res.x
    score = {}
    for i in range(len(nodes)):
        score[i] = res.x[i]
    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=False)
    xresult = []
    for item in sorted_score:
        xresult.append(item[0])
    for item in sorted_score:
        print item
    reverse_xresult = list(reversed(xresult))

    recall_factor1 = 0
    recall_factor2 = 0

    for item in xresult[:10]:
        if item < 10:
            recall_factor1 += 1
    for item in reverse_xresult[:10]:
        if item < 10:
            recall_factor2 += 1
    if recall_factor1 > recall_factor2:
        print xresult
        RecordFiles.record_results('CrowdBT', xresult, percent)
    else:
        print reverse_xresult
        RecordFiles.record_results('CrowdBT', reverse_xresult, percent)


def percent():
    global sample_edges
    for percent in np.arange(0.1, 1.1, 0.1):
        sample_edges = random.sample(edges, int(percent * len(edges)))
        optimization_crowdbt(int(percent * 100))


def average_recall():
    for re in range(1000):
        print "CrowdBT", re
        percent()


def execute():
    pre_process()
    average_recall()

if __name__ == "__main__":

    execute()
