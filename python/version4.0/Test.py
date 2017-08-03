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

    id = identification.Identification(image_path=args.image_path, label_path=args.label_path,
                                           species=args.species, scan_size=args.scan_size)
    id.get_image_matrix()

    # Import classifier
    model = load_model(args.classifier_path)

    # Run classification
    id.predict(model)

    recombination = 'median'
    id.summarize_predictions(recombination)
    pickle.dump(id.prediction_matrix, open("{0}.{1}.p".format(args.prediction_prefix, recombination), "wb"))

    # Assess classification
    id.assess()
    id.save_results(args.prediction_prefix, recombination)



if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument("classifier_path", help="Path to model to use")
    parser.add_argument("image_path", help="Path to image to classify")
    parser.add_argument("label_path", help="Path to labels of image")
    parser.add_argument("species", help="Species of ant")
    parser.add_argument("scan_size", help="Size of scanning boxes")
    parser.add_argument("prediction_prefix", help="Location for output files")

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