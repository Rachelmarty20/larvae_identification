import sys
import time
import mahotas as mh
import numpy as np
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import ndimage


# Goal: compare predictions to actual gold standard to assess the classifier for a particular photo

# Input: gold standard, prediction matrix (numpy matrix) <- these must be the same size
# Output: accuracy score file

# run_classifier parameters: test_photo_file, classifier_file, image_size, step, recombination
def main(test_photo, species, image_size, step, recombination):

    prediction_matrix = pickle.load(open("/cellar/users/ramarty/Data/ants/gold_standard/predictions/{0}/{1}.{2}.{3}.{4}.p".format(species, test_photo, image_size, step, recombination), "rb"))
    gold_standard = mh.imread('/cellar/users/ramarty/Data/ants/gold_standard/photos/{0}.png'.format(test_photo))

    # make gold standard binary for comaprison
    gs_binary = np.arange(len(gold_standard)*len(gold_standard[0])).reshape(len(gold_standard), len(gold_standard[0]))
    for row in range(len(gold_standard)):
        for col in range(len(gold_standard[0])):
            gs_binary[row][col] = f(gold_standard[row][col])

    # percentile_filter
    prediction_matrix_filtered = ndimage.filters.percentile_filter(prediction_matrix, percentile=20, size=10)
    output_results(test_photo, species, image_size, step, recombination, gs_binary, prediction_matrix_filtered, 'percentile_20')

    prediction_matrix_filtered = ndimage.filters.percentile_filter(prediction_matrix, percentile=40, size=10)
    output_results(test_photo, species, image_size, step, recombination, gs_binary, prediction_matrix_filtered, 'percentile_40')

    prediction_matrix_filtered = ndimage.filters.percentile_filter(prediction_matrix, percentile=60, size=10)
    output_results(test_photo, species, image_size, step, recombination, gs_binary, prediction_matrix_filtered, 'percentile_60')

    # Gaussian
    prediction_matrix_filtered = ndimage.filters.gaussian_filter(prediction_matrix, 2, mode='nearest')
    output_results(test_photo, species, image_size, step, recombination, gs_binary, prediction_matrix_filtered, 'gaussian')

    # Minimum
    prediction_matrix_filtered = ndimage.filters.minimum_filter(prediction_matrix, size=20)
    output_results(test_photo, species, image_size, step, recombination, gs_binary, prediction_matrix_filtered, 'minimum')

    # Maxium
    prediction_matrix_filtered = ndimage.filters.maximum_filter(prediction_matrix, size=20)
    output_results(test_photo, species, image_size, step, recombination, gs_binary, prediction_matrix_filtered, 'maximum')

    # grey erosian?
    prediction_matrix_filtered = ndimage.grey_erosion(prediction_matrix, size=20)
    output_results(test_photo, species, image_size, step, recombination, gs_binary, prediction_matrix_filtered, 'grey_erosian')


def output_results(test_photo, species, image_size, step, recombination, gs_binary, prediction_matrix, filter_name):

    diff = gs_binary - prediction_matrix
    total_dim = gs_binary.shape[0] * gs_binary.shape[1]
    tpr = 1 - (diff[(diff > 0)].sum() / gs_binary.sum())
    fpr = abs(diff[(diff < 0)].sum()) / (total_dim - gs_binary.sum()) # okay -- doesn't account for lightly colored

    print gs_binary.sum(), diff[(diff > 0)].sum()
    print 'True Positive Rate:', tpr
    print 'False Positive Rate:', fpr

    # Save results to a txt file
    with open("/cellar/users/ramarty/Data/ants/gold_standard/predictions/{0}/{1}.{2}.{3}.{4}.{5}.txt".format(species, test_photo, image_size, step, recombination, filter_name), 'w') as outfile:
        outfile.write('True Positive Rate: {0}\n'.format(tpr))
        outfile.write('False Positive Rate: {0}\n'.format(fpr))

    # Save images to a file
    plt.figure(figsize=(6,8))
    sns.heatmap(prediction_matrix)
    plt.savefig("/cellar/users/ramarty/Data/ants/gold_standard/predictions/{0}/{1}.{2}.{3}.{4}.{5}.png".format(species, test_photo, image_size, step, recombination, filter_name))

def f(x):
    if ((x[0] == 246) & (x[1] == 255) & (x[2] == 0)) | ((x[0] == 169) & (x[1] == 206) & (x[2] == 114)) | ((x[0] == 251) & (x[1] == 175) & (x[2] == 93)):
        return 1
    else:
        return 0

def plot_results(prediction_matrix, test_file_gs):
    plt.figure(figsize=(6,8))
    # predictions
    sns.heatmap(prediction_matrix)
    plt.show()
    plt.clf()
    # gold standard
    im = mh.imread(test_file_gs)
    plt.imshow(im)
    plt.show()
    plt.clf()





###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 6:
        sys.exit()
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    print time.time() - start_time
    sys.exit()