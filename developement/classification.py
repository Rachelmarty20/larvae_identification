import mahotas as mh
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns
import pickle
from scipy import signal

import warnings
warnings.filterwarnings('ignore')

class Classification(object):
    '''
    An image for classification. Images have the following properties:
    '''

    def __init__(self, image_path, square_size, filter1, kernel_size, filter2, sample_name):
        self.image_path = image_path
        self.square_size = square_size
        self.step = 20
        self.filter1 = filter1
        self.kernel_size = kernel_size
        self.filter2 = filter2
        self.name = sample_name

    def get_image_matrix(self):
        '''
        Trade in path for numpy matrix
        :return: None
        '''
        self.image = mh.imread(self.image_path)

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

    def summarize_predictions(self, percentile=35):
        x_total, y_total = self.image.shape[1], self.image.shape[0]
        summary_matrix = [[0 for k in range(x_total)] for l in range(y_total)]
        for i_index, i in enumerate(range(y_total)):
            for j_index, j in enumerate(range(x_total)):
                summary_matrix[i_index][j_index] = np.median(self.all_predictions[i_index][j_index])
        prediction_matrix_np = np.matrix(summary_matrix)
        self.prediction_matrix = np.nan_to_num(prediction_matrix_np)

    def filter(self):
        # filter 1
        self.prediction_matrix[self.prediction_matrix < self.filter1] = 0
        # kernel
        kernel = np.array([[1 for x in range(self.kernel_size)] for y in range(self.kernel_size)])
        self.prediction_matrix = signal.convolve2d(self.prediction_matrix, kernel, boundary='wrap', mode='same')/kernel.sum()
        # filter 2
        self.prediction_matrix[self.prediction_matrix < self.filter2] = 0
        self.prediction_matrix[self.prediction_matrix > 0] = 1

    def save_results(self, location):
        # Save matrix to a file
        pickle.dump(self.prediction_matrix, open("{0}/{1}.p".format(location, self.name), "wb"))

        # Save images to a file
        plt.figure(figsize=(6,8))
        sns.heatmap(self.prediction_matrix, cmap=sns.cubehelix_palette(100))
        plt.savefig("{0}/{1}.png".format(location, self.name))