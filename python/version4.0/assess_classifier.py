import sys
import time
import mahotas as mh
import numpy as np
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


# Goal: compare predictions to actual gold standard to assess the classifier for a particular photo

# Input: gold standard, prediction matrix (numpy matrix) <- these must be the same size
# Output: accuracy score file

# run_classifier parameters: test_photo_file, classifier_file, image_size, step, recombination
def main(test_photo, species, image_size, step, recombination):

    prediction_matrix = np.array(pickle.load(open("/cellar/users/ramarty/Data/ants/version4.0/predictions/{0}/{1}.{2}.{3}.{4}.p".format(species, test_photo, image_size, step, recombination), "rb")))
    gold_standard = mh.imread('/cellar/users/ramarty/Data/ants/photos/{0}.png'.format(test_photo))

    # make gold standard binary for comaprison
    gs_binary = np.arange(len(gold_standard)*len(gold_standard[0])).reshape(len(gold_standard), len(gold_standard[0]))
    for row in range(len(gold_standard)):
        for col in range(len(gold_standard[0])):
            gs_binary[row][col] = f(gold_standard[row][col])

    cutoff = 0.5
    TP, FP, FN = 0, 0, 0
    for i in range(image_size):
        for j in range(image_size):
            # val_predictions should == 1 for TP and FP
            if (gs_binary[i][j] > cutoff) & (prediction_matrix[i][j] > cutoff):
                TP += 1
            elif (gs_binary[i][j] <= cutoff) & (prediction_matrix[i][j] > cutoff):
                FP += 1
            elif (gs_binary[i][j] > cutoff) & (prediction_matrix[i][j] <= cutoff):
                FN += 1

    #print 'True Positive Rate:', tpr
    #print 'False Positive Rate:', fpr

    # Save results to a txt file
    with open("/cellar/users/ramarty/Data/ants/gold_standard/predictions/{0}/{1}.{2}.{3}.{4}.txt".format(species, test_photo, image_size, step, recombination), 'w') as outfile:
        if (TP + FP > 0) & (TP + FN > 0):
            precision = TP/float(TP+FP)
            recall = TP/float(TP+FN)
            outfile.write('Precision: {0}\n'.format(precision))
            outfile.write('Recall: {0}\n'.format(recall))
        else:
            outfile.write('TP: {0}\n'.format(TP))
            outfile.write('FP: {0}\n'.format(FP))
            outfile.write('FN: {0}\n'.format(FN))

    # Save images to a file
    plt.figure(figsize=(6,8))
    sns.heatmap(prediction_matrix)
    plt.savefig("/cellar/users/ramarty/Data/ants/gold_standard/predictions/{0}/{1}.{2}.{3}.{4}.png".format(species, test_photo, image_size, step, recombination))

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