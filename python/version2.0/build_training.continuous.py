import os
import sys
import time
import mahotas as mh

# group the larvae and pupae together for now; exclude the eggs

def main(species, image_size):

    if species == 'cfellah':
        files = list(set([x.split('.')[0] for x in os.listdir('/cellar/users/ramarty/Data/ants/gold_standard/photos/') if ('2017' in x) or ('2016' in x)]))
    else: # species == 'leptothorax':
        files = list(set([x.split('.')[0] for x in os.listdir('/cellar/users/ramarty/Data/ants/gold_standard/photos/') if ('2014' in x) or ('box101' in x)]))

    directory = '/cellar/users/ramarty/Data/ants/gold_standard/photos/'

    counter = 0
    # maybe a more sophisticated way of removing training
    for f in files[:-5]:
        im_ann = mh.imread('{0}{1}.png'.format(directory, f))
        im_org = mh.imread('{0}{1}.pgm'.format(directory, f))

        if species == 'cfellah':
            y_total, x_total = im_ann.shape[0], 2800
        else: # species == 'leptothorax':
            y_total, x_total = im_ann.shape[0], im_ann.shape[1]

        for i in range(0, y_total-image_size, int(image_size/float(2))):
            for j in range(0, x_total-image_size, int(image_size/float(2))):
                # check colors from annotated - split for species
                larvae_pupae = 0
                for m in range(image_size):
                    for n in range(image_size):
                        values = im_ann[i:i+image_size, j:j+image_size][m][n]
                        # larvae or pupae -- currently counted as the same
                        if ((values[0] == 246) & (values[1] == 255) & (values[2] == 0)) | ((values[0] == 169) & (values[1] == 206) & (values[2] == 114)) | ((values[0] == 251) & (values[1] == 175) & (values[2] == 93)):
                            larvae_pupae += 1

                if larvae_pupae == 0:
                    if counter % 10 == 0:
                        mh.imsave('/cellar/users/ramarty/Data/ants/gold_standard/training/{0}/cont_size_{1}/{2}.i{3}.pgm'.format(species, image_size, str(larvae_pupae), str(counter)),
                              im_org[i:i+image_size, j:j+image_size])
                else:
                    mh.imsave('/cellar/users/ramarty/Data/ants/gold_standard/training/{0}/cont_size_{1}/{2}.i{3}.pgm'.format(species, image_size, str(larvae_pupae), str(counter)),
                          im_org[i:i+image_size, j:j+image_size])

                counter += 1
                if counter % 100 == 0:
                    print counter



###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 3:
        sys.exit()
    main(sys.argv[1], int(sys.argv[2]))
    print time.time() - start_time
    sys.exit()