
import sys
sys.path.append("..")
import random
from InferenceForSelection import sig_local, Hybrid, MLECrowdBT, sig_iterative, sig_local, ELO
from InferenceForSelection import SSRW
from Deal_with_text_files import portrait, historyevents, statue, mall_process
global nodes, edges, Matrix


def initial_process():

    global nodes, edges, Matrix
    nodes, edges, Matrix = statue.statue_process()


def sample_process():

    global nodes, edges, Matrix

    for percent in range(10, 110, 10):

        sample_percent = percent / 100.0

        sample_edges = random.sample(edges, int(sample_percent * len(edges)))

        trans_Matrix = {}

        for edge in sample_edges:
            trans_Matrix[edge] = Matrix[edge]

        ELO.ELO_Ranking('random', nodes, sample_edges, trans_Matrix, percent)


def process():
    initial_process()
    for xe in range(1000):
        print xe
        sample_process()

if __name__ == "__main__":
    process()
