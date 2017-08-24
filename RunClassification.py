#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module Docstring
"""

__author__ = "Rachel Marty"
__version__ = "0.1.0"
__license__ = "UCSD"

import argparse
import developement.claication as claication
from sklearn.externals import joblib
import cPickle as pickle
import warnings
warnings.filterwarnings('ignore')

def main(args):

    # Upload image
    cla = claication.claication(image_path=args.image_path, square_size=args.square_size,
                                       filter1=args.filter1, kernel_size=args.kernel_size,
                                       filter2=args.filter2, sample_name=args.sample_name)
    cla.get_image_matrix()
    print("Image loaded.")

    # Import claier
    model = joblib.load(args.claier_path)
    print("Model loaded.")

    # Run claication
    print("Predicting...")
    cla.predict(model)
    cla.summarize_predictions()
    print("Predictions made.")

    # Perform filtering
    print("Filtering...")
    cla.filter()
    print("Filtering done.")

    # Save image and data file
    cla.save_results(args.output_direcotry)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("This program is used to claentify the position of brood in an image.")

    # required arguements
    parser.add_argument("claier_path", help="Path to model")
    parser.add_argument("image_path", help="Path to image to clay (pgm)")
    parser.add_argument("output_directory", help="Path for results directory")

    # optional arguments
    parser.add_argument('-s', action="store", type=int, dest="square_size", help="Size of scanning boxes", default=50)
    parser.add_argument('-f1', action="store", type=float, dest="filter1", help="First filter threshold", default=0.4)
    parser.add_argument('-k', action="store", type=float, dest="kernel_size", help="Kernel size", default=20)
    parser.add_argument('-f2', action="store", type=float, dest="filter2", help="Second filter threshold", default=0.4)
    parser.add_argument('-n', action="store", type=str, dest="sample_name", help="Name for sample", default='sample')

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