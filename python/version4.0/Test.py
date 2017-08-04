#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module Docstring
"""

__author__ = "Rachel Marty"
__version__ = "0.1.0"
__license__ = "UCSD"

import argparse
import identification
from keras.models import load_model
import cPickle as pickle


def main(args):

    id = identification.Identification(image_path=args.image_path, square_size=args.square_size)
    id.get_image_matrix()
    print("Image loaded.")

    # Import classifier
    model = load_model(args.classifier_path)
    print("Model loaded.")

    # Run classification
    id.predict(model)
    # maybe cycle through different recombinations?
    id.summarize_predictions(args.recombination)
    pickle.dump(id.prediction_matrix, open("{0}.{1}.p".format(args.out_path, args.recombination), "wb"))
    print("Predictions made.")

    # Assess classification
    id.assess()
    id.save_results(args.out_path, args.recombination)
    print("Results saved.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser("This program is used to test the accuracy of a classifier on an image.")

    # required arguements
    parser.add_argument("classifier_path", help="Path to model to use")
    parser.add_argument("image_path", help="Path to image to classify")
    parser.add_argument("out_path", help="Location for output files")

    # optional arguments
    parser.add_argument('-s', action="store", dest="square_size", help="Size of scanning boxes", default=50)
    parser.add_argument('-r', action="store", dest="recombination", help="Recombination for summary", default='median')


    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)