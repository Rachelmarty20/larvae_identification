import os
import sys
import time
import mahotas as mh
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import ensemble, cross_validation
from sklearn.externals import joblib


# Input: Training images
# Output: joblib classifier object file name

def main(species, image_size):

    larvae_files = os.listdir('/cellar/users/ramarty/Data/ants/gold_standard/training/{0}/size_{1}/larvae'.format(species, image_size))
    pupae_files = os.listdir('/cellar/users/ramarty/Data/ants/gold_standard/training/{0}/size_{1}/pupae'.format(species, image_size))
    other_files = os.listdir('/cellar/users/ramarty/Data/ants/gold_standard/training/{0}/size_{1}/other'.format(species, image_size))

    larvae_images = [mh.imread('/cellar/users/ramarty/Data/ants/gold_standard/training/{0}/size_{1}/larvae/{2}'.format(species, image_size, x)) for x in larvae_files] + [mh.imread('/cellar/users/ramarty/Data/ants/gold_standard/training/{0}/size_{1}/pupae/{2}'.format(species, image_size, x)) for x in pupae_files]
    other_images = [mh.imread('/cellar/users/ramarty/Data/ants/gold_standard/training/{0}/size_{1}/other/{2}'.format(species, image_size, x)) for x in other_files]

    images = larvae_images + other_images
    classifications = ['larvae' for x in larvae_images] + ['other' for x in other_images]

    features = [mh.features.haralick(x, return_mean_ptp=True) for x in images]

    X_train, X_test, y_train, y_test = train_test_split(features, classifications, test_size=0.33, random_state=42)
    clf = ensemble.RandomForestClassifier()

    predictions = cross_validation.cross_val_predict(clf, X_train, y_train)
    acc = np.mean(predictions == y_train)

    with open('/cellar/users/ramarty/Data/ants/gold_standard/classifiers/{0}/CV_accuracy.random_forest.size_{1}.txt'.format(species, image_size) , 'w') as outfile:
        outfile.write("Accuracy: {:.2%}".format(acc))

    clf.fit(X_train, y_train)

    joblib.dump(clf, '/cellar/users/ramarty/Data/ants/gold_standard/classifiers/{0}/random_forest.size_{1}.pkl'.format(species, image_size), compress=9)




###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 3:
        sys.exit()
    main(sys.argv[1], sys.argv[2])
    print time.time() - start_time
    sys.exit()