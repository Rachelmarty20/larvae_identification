import os
import sys
import time
import mahotas as mh
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import ensemble, cross_validation
from sklearn.externals import joblib
from sklearn import metrics



# Input: Training images
# Output: joblib classifier object file name

def main(species, image_size):

    files = os.listdir('/cellar/users/ramarty/Data/ants/gold_standard/training/{0}/cont_size_{1}/'.format(species, image_size))

    images, percentages = [], []
    for f in files:
        images.append(mh.imread('/cellar/users/ramarty/Data/ants/gold_standard/training/{0}/cont_size_{1}/{2}'.format(species, image_size, f)))
        percentages.append(float(f.split('.')[0]) / (int(image_size) * int(image_size)))

    features = [mh.features.haralick(x, return_mean_ptp=True) for x in images]

    X_train, X_test, y_train, y_test = train_test_split(features, percentages, test_size=0.33, random_state=42)
    clf = ensemble.GradientBoostingRegressor()

    clf.fit(X_train, y_train)

    mse = metrics.mean_squared_error(y_test, clf.predict(X_test))

    with open('/cellar/users/ramarty/Data/ants/gold_standard/classifiers/{0}/CV_accuracy.gradientboostingregressor.cont_size_{1}.txt'.format(species, image_size) , 'w') as outfile:
        outfile.write("MSE: {:.2%}".format(mse))

    joblib.dump(clf, '/cellar/users/ramarty/Data/ants/gold_standard/classifiers/{0}/gradientboostingregressor.size_{1}.pkl'.format(species, image_size), compress=9)



###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 3:
        sys.exit()
    main(sys.argv[1], sys.argv[2])
    print time.time() - start_time
    sys.exit()