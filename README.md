# Brood Classification

## Introduction

A tool to localize the ant brood of an image. Classifiers for two species (Leptothorax and C.Fellah) are included. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The tool is written in Python and uses the following Python modules: 

* Sklearn
* cPickle
* seaborn
* mahotas
* numpy
* matplotlib

All of the modules can be installed with pip:

```
pip install numpy
pip install scipy
pip install -U scikit-learn
```

## Testing



## Running 

The following will have to be run from the commandline to produce results:

```
python RunClassification.py
```

For help choosing options, run:

```
python RunClassification.py --help
```

## Acknowledgements

* Thank you Sean McGregor and Tomas Kay for providing the labeled images!
