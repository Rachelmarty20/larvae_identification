import os
import sys
import time
import mahotas as mh
import numpy as np
import pandas as pd
import pickle
from sklearn.externals import joblib


# Input: test file, classifier, style of recombination
# Output: prediction matrix (the same size as the input file)

# image_size=100, step=20
# classifier and image_size need to align

# will this take a really, really long time?
def main(test_photo, species, image_size, step, recombination):

    # Import classifier
    clf = joblib.load('/cellar/users/ramarty/Data/ants/gold_standard/classifiers/{0}/random_forest.size_{1}.pkl'.format(species, image_size))

    # Makes several predictions for each pixel
    im = mh.imread('/cellar/users/ramarty/Data/ants/gold_standard/photos/{0}.pgm'.format(test_photo))
    x_total, y_total = im.shape[1], im.shape[0]
    prediction_matrix = [[[] for k in range(x_total)] for l in range(y_total)]
    # cycle through photo
    print y_total, x_total
    for i_index, i in enumerate(range(0, y_total-step, step)):
        print i_index
        for j_index, j in enumerate(range(0, x_total-step, step)):
            test_features = mh.features.haralick(im[i:i+image_size, j:j+image_size], return_mean_ptp=True)
            prediction = clf.predict_proba(test_features)[0][0]
            for i_single in range(i, i+image_size):
                for j_single in range(j, j+image_size):
                    try:
                        prediction_matrix[i_single][j_single].append(prediction)
                    except:
                        None

    # Sumarizes the predictions for each pixel
    summary_matrix = [[0 for k in range(x_total)] for l in range(y_total)]
    for i_index, i in enumerate(range(y_total)):
        for j_index, j in enumerate(range(x_total)):
            if recombination == 'percentile':
                summary_matrix[i_index][j_index] = np.percentile(prediction_matrix[i_index][j_index], 35)
            elif recombination == 'median':
                summary_matrix[i_index][j_index] = np.median(prediction_matrix[i_index][j_index])
            else: # mean
                summary_matrix[i_index][j_index] = np.mean(prediction_matrix[i_index][j_index])

    prediction_matrix_np = np.matrix(summary_matrix)
    prediction_matrix_np = np.nan_to_num(prediction_matrix_np)

    pickle.dump(prediction_matrix_np, open("/cellar/users/ramarty/Data/ants/gold_standard/predictions/{0}/{1}.{2}.{3}.{4}.p".format(species, test_photo, image_size, step, recombination), "wb"))


###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 6:
        sys.exit()
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    print time.time() - start_time
    sys.exit()