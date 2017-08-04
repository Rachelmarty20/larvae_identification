import mahotas as mh
import numpy as np
from matplotlib import pyplot as plt
import PIL.Image as Image
import seaborn as sns
import mahotas as mh

class Identification(object):
    '''
    An image for classification. Images have the following properties:

    Attributes:
        image: name of the image to be classified
        labels: the image with labels
        size: size of the image
    '''

    def __init__(self, image_path, square_size):
        self.image_path = image_path + '.pgm'
        self.label_path = image_path + '.png'
        self.image_name = image_path.split('/')[-1]
        self.square_size = square_size
        self.step = 20
        # Maybe some of the gets can be put in the initialization??


    def get_image_matrix(self):
        '''
        Trade in path for numpy matrix
        :return: None
        '''
        self.image = np.expand_dims(Image.open(self.image_path), axis=2)


    def get_label_matrix(self):
        '''
        Trade in path for numpy matrix
        :return: numpy matrix
        '''
        gold_standard = mh.imread(self.label_path)
        gs_binary = np.arange(len(gold_standard)*len(gold_standard[0])).reshape(len(gold_standard), len(gold_standard[0]))
        for row in range(len(gold_standard)):
            for col in range(len(gold_standard[0])):
                gs_binary[row][col] = f(gold_standard[row][col])
        self.labels = gs_binary

    def predict(self, model):
        '''
        Create predictions using model
        :param classifier: model
        :return: None
        '''
        x_total, y_total = self.image.shape[1], self.image.shape[0]
        prediction_matrix = [[[] for k in range(x_total)] for l in range(y_total)]
        for i_index, i in enumerate(range(0, y_total-(self.square_size), self.step)):
            for j_index, j in enumerate(range(0, x_total-(self.square_size), self.step)):
                test_features = mh.features.haralick(self.image[i:i+self.square_size, j:j+self.square_size], return_mean_ptp=True)
                prediction = model.predict_proba(test_features)[0][0]
                for i_single in range(i, i+self.square_size):
                    for j_single in range(j, j+self.square_size):
                        try:
                            prediction_matrix[i_single][j_single].append(prediction)
                        except:
                            None
        self.all_predictions = prediction_matrix

    def summarize_predictions(self, recombination, percentile=35):
        x_total, y_total = self.image.shape[1], self.image.shape[0]
        summary_matrix = [[0 for k in range(x_total)] for l in range(y_total)]
        for i_index, i in enumerate(range(y_total)):
            for j_index, j in enumerate(range(x_total)):
                if recombination == 'percentile':
                    summary_matrix[i_index][j_index] = np.percentile(self.all_predictions[i_index][j_index], percentile)
                elif recombination == 'median':
                    summary_matrix[i_index][j_index] = np.median(self.all_predictions[i_index][j_index])
                else: # mean
                    summary_matrix[i_index][j_index] = np.mean(self.all_predictions[i_index][j_index])

        prediction_matrix_np = np.matrix(summary_matrix)
        self.prediction_matrix = np.nan_to_num(prediction_matrix_np)

    def assess(self, cutoff=0.5):
        TP, FP, FN = 0, 0, 0
        for i in range(self.image.shape[1]):
            for j in range(self.image.shape[0]):
                # val_predictions should == 1 for TP and FP
                if (self.labels[i][j] > cutoff) & (self.prediction_matrix[i][j] > cutoff):
                    TP += 1
                elif (self.labels[i][j] <= cutoff) & (self.prediction_matrix[i][j] > cutoff):
                    FP += 1
                elif (self.labels[i][j] > cutoff) & (self.prediction_matrix[i][j] <= cutoff):
                    FN += 1
        self.TP = TP
        self.FP = FP
        self.FN = FN

    def create_out_path(self, prediction_path, classifier_path):
        #prediction_path = '/cellar/users/ramarty/Data/ants/version4.0/predictions/'
        classifier = classifier_path.split('/')[-1]
        species = classifier_path.split('/')[-2]
        out_path = '{0}{1}/{2}.{3}'.format(prediction_path, species, classifier, self.image_name)
        return out_path

    def save_results(self, location):
        # Save results to a text file
        with open("{0}.txt".format(location), 'w') as outfile:
            if (self.TP + self.FP > 0) & (self.TP + self.FN > 0):
                precision = self.TP/float(self.TP+self.FP)
                recall = self.TP/float(self.TP+self.FN)
                outfile.write('Precision: {0}\n'.format(precision))
                outfile.write('Recall: {0}\n'.format(recall))
            else:
                outfile.write('TP: {0}\n'.format(self.TP))
                outfile.write('FP: {0}\n'.format(self.FP))
                outfile.write('FN: {0}\n'.format(self.FN))

        # Save images to a file
        plt.figure(figsize=(6,8))
        sns.heatmap(self.prediction_matrix)
        plt.savefig("{0}.png".format(location))


def f(x):
    if ((x[0] == 246) & (x[1] == 255) & (x[2] == 0)) | ((x[0] == 169) & (x[1] == 206) & (x[2] == 114)) | ((x[0] == 251) & (x[1] == 175) & (x[2] == 93)):
        return 1
    else:
        return 0
