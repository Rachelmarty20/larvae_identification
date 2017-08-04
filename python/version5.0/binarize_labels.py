import mahotas as mh
import numpy as np
from matplotlib import pyplot as plt
import PIL.Image as Image
import seaborn as sns
import sklearn
import sys

path = sys.argv[1]

def f(x):
    if ((x[0] == 246) & (x[1] == 255) & (x[2] == 0)) | ((x[0] == 169) & (x[1] == 206) & (x[2] == 114)) | ((x[0] == 251) & (x[1] == 175) & (x[2] == 93)):
        return 1
    else:
        return 0

gold_standard = mh.imread(path)
gs_binary = np.arange(len(gold_standard)*len(gold_standard[0])).reshape(len(gold_standard), len(gold_standard[0]))
for row in range(len(gold_standard)):
    for col in range(len(gold_standard[0])):
        gs_binary[row][col] = f(gold_standard[row][col])
