import os
import mahotas as mh
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import sys
import time


def main():

    species = 'cfellah'
    size = 100

    if species == 'cfellah':
        files = list(set([x.split('.')[0] for x in os.listdir('/cellar/users/ramarty/Data/ants/photos/') if ('2017' in x) or ('2016' in x)]))
    else: # species == 'leptothorax':
        files = list(set([x.split('.')[0] for x in os.listdir('/cellar/users/ramarty/Data/ants/photos/') if ('2014' in x) or ('box101' in x)]))

    photos_directory = '/cellar/users/ramarty/Data/ants/photos'
    training_directory = '/cellar/users/ramarty/Data/ants/version3.0/training'

    # make directories if they don't exist
    # species directory
    if not os.path.exists('{0}/{1}'.format(training_directory, species)):
        os.makedirs('{0}/{1}'.format(training_directory, species))
    # size directory
    if not os.path.exists('{0}/{1}/{2}'.format(training_directory, species, size)):
        os.makedirs('{0}/{1}/{2}'.format(training_directory, species, size))
    # image directory and target directory
    if not os.path.exists('{0}/{1}/{2}/images'.format(training_directory, species, size)):
        os.makedirs('{0}/{1}/{2}/images'.format(training_directory, species, size))
    if not os.path.exists('{0}/{1}/{2}/targets'.format(training_directory, species, size)):
        os.makedirs('{0}/{1}/{2}/targets'.format(training_directory, species, size))


    counter = 1849
    for f in files[5:]:
        print f
        im_ann = mh.imread('{0}/{1}.png'.format(photos_directory, f))
        im_org = mh.imread('{0}/{1}.pgm'.format(photos_directory, f))

        if species == 'cfellah':
            y_total, x_total = im_ann.shape[0], 2800
        else: # species == 'leptothorax':
            y_total, x_total = im_ann.shape[0], im_ann.shape[1]


        for i in range(0, y_total-size, int(size/float(2))):
            for j in range(0, x_total-size, int(size/float(2))):
                larvae = 0
                # save targets - transform into single digit classified output
                #np.save('{0}/{1}/{2}/targets/{3}.npy'.format(training_directory, species, str(size), str(counter)), im_ann[i:i+size, j:j+size])
                matrix = []
                for m in range(size):
                    array = []
                    for n in range(size):
                        values = im_ann[i:i+size, j:j+size][m][n]
                        # larvae or pupae -- currently counted as the same
                        if ((values[0] == 246) & (values[1] == 255) & (values[2] == 0)) | ((values[0] == 169) & (values[1] == 206) & (values[2] == 114)) | ((values[0] == 251) & (values[1] == 175) & (values[2] == 93)):
                            array.append(1)
                            larvae += 1
                        else:
                            array.append(0)
                    matrix.append(array)
                if larvae >= 20:
                    np.save('{0}/{1}/{2}/targets/{3}.npy'.format(training_directory, species, str(size), str(counter)), np.array(matrix))

                    # save image
                    mh.imsave('{0}/{1}/{2}/images/{3}.pgm'.format(training_directory, species, str(size), str(counter)),
                          im_org[i:i+size, j:j+size])
                    counter += 1




###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 1:
        sys.exit()
    main()
    print time.time() - start_time
    sys.exit()