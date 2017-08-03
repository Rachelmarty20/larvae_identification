import os
import mahotas as mh
import numpy as np
import pickle
import theano
import theano.tensor as T
import lasagne
from sklearn.model_selection import train_test_split
import sklearn
import sys
import time
import pandas as pd


# initalize
species = 'cfellah'
size = 100
directory = '/cellar/users/ramarty/Data/ants/version3.0/training/{0}/{1}'.format(species, size)


def main(learning_rate, batch_size):

    # Import and format the data
    # TODO: May need to split these out and not upload them all at the same time???
    X = get_features(14000)
    y = get_targets(14000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    data = [(X_train, y_train),  (X_test, y_test)]
    subsets = ['train', 'test']
    dataset = {}
    for (subset_data, subset_labels), subset_name in zip(data, subsets):
        # The data is provided in the shape (n_examples, 784)
        # where 784 = width*height = 28*28
        # We need to reshape for convolutional layer shape conventions - explained below!
        subset_data = subset_data.reshape(
        (subset_data.shape[0], 1, 100, 100))
        dataset[subset_name] = {
        # We need to use data matrices of dtype theano.config.floatX
        'X': subset_data.astype(theano.config.floatX),
        # Labels are integers
        'y': subset_labels.astype(theano.config.floatX)}

    # Build network
    input_shape = dataset['train']['X'][0].shape
    l_in = lasagne.layers.InputLayer(
        shape=(None, input_shape[0], input_shape[1], input_shape[2]))
    l_conv = lasagne.layers.Conv2DLayer(
         l_in,
         num_filters=50, filter_size=(5, 5),
         nonlinearity=lasagne.nonlinearities.rectify,
         W=lasagne.init.HeNormal(gain='relu'))
    l_deconv = lasagne.layers.TransposedConv2DLayer(l_conv, num_filters=l_conv.input_shape[1],
         filter_size=l_conv.filter_size,
         nonlinearity=lasagne.nonlinearities.rectify)
    l_output = lasagne.layers.NINLayer(
         l_deconv,
         num_units=1,
         nonlinearity=lasagne.nonlinearities.sigmoid)

    # Loss function
    predictions = lasagne.layers.get_output(l_output)
    targets = T.tensor3('true_output') # unsure if this is right
    loss = lasagne.objectives.squared_error(predictions, targets)
    loss = lasagne.objectives.aggregate(loss, mode='mean')

    # Train function
    all_params = lasagne.layers.get_all_params(l_output, trainable=True)
    updates = lasagne.updates.sgd(loss, all_params, learning_rate=learning_rate)
    train = theano.function([l_in.input_var, targets], loss, updates=updates, allow_input_downcast=True, name='Training')
    get_output = theano.function([l_in.input_var], predictions, name='get_output')

    # Test
    BATCH_SIZE = batch_size
    # TODO: update!!!
    N_EPOCHS = 300
    batch_idx = 0
    epoch = 0
    results = []
    while epoch < N_EPOCHS:
        train(dataset['train']['X'][batch_idx:batch_idx + BATCH_SIZE],
        dataset['train']['y'][batch_idx:batch_idx + BATCH_SIZE])
        batch_idx += BATCH_SIZE
        if batch_idx >= dataset['train']['X'].shape[0]:
            batch_idx = 0
            epoch += 1
            val_predictions = get_output(dataset['test']['X'])
            accuracy = np.mean(val_predictions == dataset['test']['y'])
            results.append([epoch, accuracy])


    df = pd.DataFrame(results)
    df.columns = ['Iteration', 'Accuracy']
    df.to_csv('/cellar/users/ramarty/Data/ants/version3.0/data/parameter_sweep.in_conv_dconv_out.{0}_{1}.csv'.format(learning_rate, batch_size))

# TODO: Add an outcome of FPR and TPR
    cutoff = 0.25
    precisions, recalls = [], []
    for x in range(200):
        TP, FP, FN = 0, 0, 0
        for i in range(100):
            for j in range(100):
                # val_predictions should == 1 for TP and FP
                if (dataset['test']['y'][x][i][j] > cutoff) & (val_predictions[x][0][i][j] > cutoff):
                    TP += 1
                elif (dataset['test']['y'][x][i][j] <= cutoff) & (val_predictions[x][0][i][j] > cutoff):
                    FP += 1
                elif (dataset['test']['y'][x][i][j] > cutoff) & (val_predictions[x][0][i][j] <= cutoff):
                    FN += 1
        if TP + FP > 0: # & TP + FN > 0:
            precision = TP/float(TP+FP)
            recall = TP/float(TP+FN)
            precisions.append(precision)
            recalls.append(recall)
            print x, precision, recall, dataset['test']['y'][x].sum(), val_predictions[x][0].sum()
            #print val_predictions[x][0].sum(), val_predictions[x][0].max(), val_predictions[x][0].min()
        else:
            print x, "No positives"
            #print val_predictions[x][0].sum(), val_predictions[x][0].max(), val_predictions[x][0].min()

    with open('/cellar/users/ramarty/Data/ants/version3.0/data/results.in_conv_dconv_out.{0}_{1}.csv'.format(learning_rate, batch_size)) as outfile:
        outfile.write('Precision: {0}\n'.format(np.mean(precisions)))
        outfile.write('Recall: {0}\n'.format(np.mean(recalls)))

def get_features(number_of_images):
    features = []
    for i in range(number_of_images):
        features.append(mh.imread('{0}/images/{1}.pgm'.format(directory, i)))
    return np.array(features)

def get_targets(number_of_targets):
    targets = []
    for i in range(number_of_targets):
        targets.append(np.load('{0}/targets/{1}.npy'.format(directory, i)))
    return np.array(targets)



###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 3:
        sys.exit()
    main(float(sys.argv[1]), int(sys.argv[2]))
    print time.time() - start_time
    sys.exit()