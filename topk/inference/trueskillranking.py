
import sys
sys.path.append("..")
import time
import trueskill
import numpy
import random
import copy
from Deal_with_text_files import write_to_files, GenerateTestFile, historyevents, portrait, statue, mall_process,\
    AddedTestFile, RecordFiles, writing_time

global nodes, edges, Matrix, range_number


def pre_process():
    global nodes, edges, Matrix, range_number
    nodes, edges, Matrix = GenerateTestFile.simulant_dataset()


def TrueSkill_Ranking(sample_edges, percent):

    env = trueskill.TrueSkill(mu=25.0, sigma=20,
                              beta=30, tau=0.08333333333333334,
                              draw_probability=0, backend=None)

    env.make_as_global()

    score = {}
    for node in nodes:
        score[node] = trueskill.Rating()

    for edge in sample_edges:
        compare_result = trueskill.rate_1vs1(score[edge[0]], score[edge[1]])
        score[edge[0]] = compare_result[0]
        score[edge[1]] = compare_result[1]

    sorted_score = sorted(
        score.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

    result = []

    for item in sorted_score:
        print item
        result.append(item[0])

#     RecordFiles.record_dataset('TrueSkill', result, percent)


def main():
    for percent in numpy.arange(0.1, 1.0, 0.1):
        sample_edges = random.sample(edges, int(percent * len(edges)))
        TrueSkill_Ranking(sample_edges, int(percent * 100))


def Redo():
    for re in range(1000):
        print "TrueSkill", re

        main()

if __name__ == "__main__":
    pre_process()
    Redo()
