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
import sklearn
from sklearn import metrics
from scipy import signal
import gc

# Goal: compare predictions to actual gold standard to assess the classifier for a particular photo

# Input: gold standard, prediction matrix (numpy matrix) <- these must be the same size
# Output: accuracy score file

# run_classifier parameters: test_photo_file, classifier_file, image_size, step, recombination
def main(test_photo, species, image_size, kernel_size):

    # Import prediction matrix
    prediction_matrix_original = pickle.load(open('/cellar/users/ramarty/Data/ants/version5.0/predictions/{0}/random_forest.{1}.pkl.{2}.p'.format(species, image_size, test_photo)))

    # Import binarized result
    gs = pickle.load(open('/cellar/users/ramarty/Data/ants/photos/{0}.p'.format(test_photo)))

    print('Files imported.')

    ######## Filters ########


    filter_thresholds1 = [0.4, 0.5, 0.6, 0.7]
    filter_thresholds2 = [0.2, 0.3, 0.4, 0.5]


    # Filter then threshold
    for filter_threshold1 in filter_thresholds1:
        for filter_threshold2 in filter_thresholds2:
            prediction_matrix = prediction_matrix_original.copy()

            prediction_matrix[prediction_matrix < filter_threshold1] = 0
            kernel = np.array([[1 for x in range(kernel_size)] for y in range(kernel_size)])
            prediction_matrix = signal.convolve2d(prediction_matrix, kernel, boundary='wrap', mode='same')/kernel.sum()
            prediction_matrix_copy = prediction_matrix.copy()
            prediction_matrix_copy[prediction_matrix_copy > 0] = 1
            auc, fpr, tpr = assess(gs, prediction_matrix_copy)
            output_base = '/cellar/users/ramarty/Data/ants/version5.0/predictions/{0}/random_forest.{1}.pkl.{2}.filter_{3}.kernel_{4}'.format(species, image_size, test_photo, filter_threshold1, kernel_size)
            save_result(output_base, prediction_matrix, auc, fpr, tpr)

            prediction_matrix[prediction_matrix < filter_threshold2] = 0
            prediction_matrix[prediction_matrix > 0] = 1
            auc, fpr, tpr = assess(gs, prediction_matrix)
            output_base = '/cellar/users/ramarty/Data/ants/version5.0/predictions/{0}/random_forest.{1}.pkl.{2}.filter_{3}.kernel_{4}.filter_{5}'.format(species, image_size, test_photo, filter_threshold1, kernel_size, filter_threshold2)
            save_result(output_base, prediction_matrix, auc, fpr, tpr)

            del prediction_matrix
            del prediction_matrix_copy
            del fpr, tpr

        print('Filter: {0}, Kernel: {1}'.format(filter_threshold1, kernel_size))



def assess(gs, prediction_matrix):
    real, predicted = [], []
    for i in range(prediction_matrix.shape[0]):
        for j in range(prediction_matrix.shape[1]):
            real.append(gs[i][j])
            predicted.append(prediction_matrix[i][j])
    auc = sklearn.metrics.roc_auc_score(real, predicted)
    fpr, tpr, thresholds = sklearn.metrics.roc_curve(real, predicted, pos_label=1)
    return auc, fpr, tpr


def save_result(output_base, prediction_matrix, auc, fpr, tpr):
    # Save results to a text file
    with open("{0}.txt".format(output_base), 'w') as outfile:
        outfile.write('AUC: {0}\n'.format(auc))
    with open("{0}.fpr.txt".format(output_base), 'w') as outfile:
        for i in fpr:
            outfile.write("{0}\n".format(i))
    with open("{0}.tpr.txt".format(output_base), 'w') as outfile:
        for i in tpr:
            outfile.write("{0}\n".format(i))
    # Save images to a file
    plt.figure(figsize=(6,8))
    sns.heatmap(prediction_matrix, cmap=sns.cubehelix_palette(100))
    plt.savefig("{0}.png".format(output_base))


###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 5:
        print "Wrong number of arguments."
        sys.exit()
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    print time.time() - start_time
    sys.exit()