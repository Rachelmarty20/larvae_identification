import os
import sys
import time
import mahotas as mh
import numpy as np
import pandas as pd


# Input: test file, test file gold standard, classifier, style of recombination
# Output: prediction matrix

test1_file = '/cellar/users/ramarty/Data/ants/gold_standard/photos/{0}.pgm'.format(files[19])
test1_file_gs = '/cellar/users/ramarty/Data/ants/gold_standard/photos/{0}.png'.format(files[19])


def test_photo(test_file, training_size):
    prediction_matrix = []
    im = mh.imread(test_file)
    y1, y2, x1, x2 = 0, im.shape[0], 0, im.shape[1]
    print y1, y2, x1, x2
    # cycle through photo
    y_total, x_total = im[y1:y2, x1:x2].shape
    print y_total, x_total
    # assigning values
    for i in range(0, y_total-training_size, training_size):
        prediction_array = [[] for x in range(training_size)]
        for j in range(0, x_total-training_size, training_size):
            test_features = mh.features.haralick(im[y1+i:y1+i+training_size, x1+j:x1+j+training_size], return_mean_ptp=True)
            prediction = clf.predict_proba(test_features)[0][0]
            for k in range(training_size):
                prediction_array[k].extend([prediction for w in range(training_size)])
        for k in range(training_size):
            prediction_matrix.append(prediction_array[k])
    # filling in edge gaps
    arrays_needed = im.shape[0] - len(prediction_matrix)
    values_needed = im.shape[1] - len(prediction_matrix[0])
    for i, prediction_array in enumerate(prediction_matrix):
        prediction_matrix[i].extend([0 for x in range(values_needed)])
    for i in range(arrays_needed):
        prediction_matrix.append([0 for x in range(im.shape[1])])
    return prediction_matrix



test_file, test_file_gs = test1_file, test1_file_gs
prediction_matrix1 = test_photo(test_file)

# overlapping elements

location_matrix = []
im = mh.imread(test_file)
y1, y2, x1, x2 = 0, im.shape[0], 0, im.shape[1]
y_total, x_total = im[y1:y2, x1:x2].shape
for i in range(0, y_total-20, 20):
    location_array = []
    for j in range(0, x_total-20, 20):
        location_array.append([i, i+20, j, j+20])
    location_matrix.append(location_array)

prediction_matrix = [[[] for k in range(int(float(x_total-20)/20))] for l in range(int(float(y_total-20)/20))]
im = mh.imread(test_file)
y1, y2, x1, x2 = 0, im.shape[0], 0, im.shape[1]
print y1, y2, x1, x2
# cycle through photo
y_total, x_total = im[y1:y2, x1:x2].shape
print y_total, x_total
for i_index, i in enumerate(range(0, y_total-20, 20)):
    print i_index
    for j_index, j in enumerate(range(0, x_total-20, 20)):
        test_features = mh.features.haralick(im[y1+i:y1+i+100, x1+j:x1+j+100], return_mean_ptp=True)
        prediction = clf.predict_proba(test_features)[0][0]
        for i_single in range(i_index, i_index+5):
            for j_single in range(j_index, j_index+5):
                try:
                    prediction_matrix[i_single][j_single].append(prediction)
                except:
                    None

summary_matrix = [[0 for k in range(int(float(x_total-20)/20))] for l in range(int(float(y_total-20)/20))]
for i_index, i in enumerate(range(0, y_total-100, 20)):
    for j_index, j in enumerate(range(0, x_total-100, 20)):
        #summary_matrix[i_index][j_index] = np.percentile(prediction_matrix[i_index][j_index], 35)
        summary_matrix[i_index][j_index] = np.median(prediction_matrix[i_index][j_index])
        #summary_matrix[i_index][j_index] = cutoff(prediction_matrix[i_index][j_index])

# output prediction matrix to a file of sorts, maybe convert to a numpy matrix and save like that?

###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 5:
        sys.exit()
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print time.time() - start_time
    sys.exit()