import os
import sys
import time
import mahotas as mh
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import ensemble, cross_validation
import PIL.Image as Image
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Conv2D
from keras.optimizers import SGD
from keras import metrics

# Input: Training images
# Output: joblib classifier object file name

def main(species, image_size, batch_size, learning_rate):

    #larvae_files = os.listdir('/cellar/users/ramarty/Data/ants/version2.0/training/{0}/size_{1}/larvae'.format(species, image_size))[:1000]
    pupae_files = os.listdir('/cellar/users/ramarty/Data/ants/version2.0/training/{0}/size_{1}/pupae'.format(species, image_size))[:5000]
    other_files = os.listdir('/cellar/users/ramarty/Data/ants/version2.0/training/{0}/size_{1}/other'.format(species, image_size))[:5000]

    larvae_images = [np.expand_dims(Image.open('/cellar/users/ramarty/Data/ants/version2.0/training/{0}/size_{1}/larvae/{2}'.format(species, image_size, x)), axis=2) for x in pupae_files] #+ [np.expand_dims(Image.open('/cellar/users/ramarty/Data/ants/version2.0/training/{0}/size_{1}/pupae/{2}'.format(species, image_size, x)), axis=2) for x in pupae_files]
    other_images = [np.expand_dims(Image.open('/cellar/users/ramarty/Data/ants/version2.0/training/{0}/size_{1}/other/{2}'.format(species, image_size, x)), axis=2) for x in other_files]

    images = np.array(larvae_images + other_images)
    classifications = [[1,0] for x in larvae_images] + [[0,1] for x in other_images]

    X_train, X_test, y_train, y_test = train_test_split(images, classifications, test_size=0.33, random_state=42)

    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(50, 50, 1)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))

    sgd = SGD(lr=learning_rate, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', metrics=[metrics.categorical_accuracy], optimizer=sgd)

    history_callback = model.fit(X_train, y_train, batch_size=batch_size, epochs=10)
    score = model.evaluate(X_test, y_test, batch_size=32)

    with open('/cellar/users/ramarty/Data/ants/version4.0/classifiers/{0}/CV_accuracy.convnet.size_{1}.b{2}_lr{3}.txt'.format(species, image_size, batch_size, learning_rate) , 'w') as outfile:
        for x in history_callback.history["categorical_accuracy"]:
            outfile.write("{0}\n".format(str(x)))

    model.save('/cellar/users/ramarty/Data/ants/version4.0/classifiers/{0}/convnet.size_{1}.b{2}_lr{3}.h5'.format(species, image_size, batch_size, learning_rate))



###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 5:
        sys.exit()
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]))
    print time.time() - start_time
    sys.exit()