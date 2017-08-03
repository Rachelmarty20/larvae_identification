import os
import sys
import time
import mahotas as mh
import numpy as np
import pandas as pd
import pickle
from keras.models import load_model
import PIL.Image as Image


# Input: test file, classifier, style of recombination
# Output: prediction matrix (the same size as the input file)

# image_size=100, step=20
# classifier and image_size need to align

# will this take a really, really long time?

# only need to import classifier and photo (the rest can be deduced, no?)
def main(test_photo, species, image_size, step, recombination):

    # Import classifier
    model = load_model('/cellar/users/ramarty/Data/ants/version4.0/classifiers/{0}/convnet.size_{1}.h5'.format(species, image_size))

    # Makes several predictions for each pixel
    image = np.expand_dims(Image.open('/cellar/users/ramarty/Data/ants/photos/{0}.pgm'.format(test_photo)), axis=2)
    x_total, y_total = image.shape[1], image.shape[0]
    prediction_matrix = [[[] for k in range(x_total)] for l in range(y_total)]
    # cycle through photo
    for i_index, i in enumerate(range(0, y_total-(image_size), step)):
        for j_index, j in enumerate(range(0, x_total-(image_size), step)):
            #print np.expand_dims(np.array(image[i:i+image_size, j:j+image_size]), axis=0).shape
            #print j, j_index
            prediction = model.predict(np.expand_dims(np.array(image[i:i+image_size, j:j+image_size]), axis=0))
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

    pickle.dump(prediction_matrix_np, open("/cellar/users/ramarty/Data/ants/version4.0/predictions/{0}/{1}.{2}.{3}.{4}.p".format(species, test_photo, image_size, step, recombination), "wb"))


###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 6:
        sys.exit()
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    print time.time() - start_time
    sys.exit()