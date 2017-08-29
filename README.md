# Brood Classification

## Introduction

A tool to localize the ant brood of an image. Classifiers for two species (Leptothorax and C.Fellah) are included. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The tool is written in Python and uses the following Python modules: 

* numpy
* scipy
* scikit-learn
* matplotlib
* seaborn
* mahotas

All of the modules can be installed with pip:

```
pip install numpy
pip install scipy
pip install -U scikit-learn
pip install matplotlib
pip install seaborn
pip intall mahotas
```

## Testing

Your installation can be tested by running the following command from main directory:

```
python RunClassification.py classifiers/leptothorax.random_forest.50.pkl test/box61-20140119-1410-00367221.pgm test/results/
```

If the installation is successful, the code should run to completion and the following command should have no output:

```
diff test/results/sample.png	test/results/sample.standard.png
```

## Running 

The following will have to be run from the commandline to produce results:

```
python RunClassification.py [-h] [-s SQUARE_SIZE][-f1 FILTER1] [-k KERNEL_SIZE] [-f2 FILTER2] [-n SAMPLE_NAME] [-v] [--version]
       classifier_path image_path output_directory
```

For help choosing options, run:

```
python RunClassification.py --help
```
To acquire the following option descriptions:

```
 positional arguments:
  classifier_path   Path to model
  image_path        Path to image to classify (pgm)
  output_directory  Path for results directory

optional arguments:
  -h, --help        show this help message and exit
  -s SQUARE_SIZE    Size of scanning boxes (must align {scanning_square_size} in classifier name)
  -f1 FILTER1       First filter threshold
  -k KERNEL_SIZE    Kernel size
  -f2 FILTER2       Second filter threshold
  -n SAMPLE_NAME    Name for sample
  -v, --verbose     Verbosity (-v, -vv, etc)
  --version         show program's version number and exit
```

### Classifiers available

Naming convention

```
classifiers/{species}.{algorithm}.{scanning_square_size}.pkl
```

C. Fellah

```
classifiers/cfellah.random_forest.30.pkl 
classifiers/cfellah.random_forest.50.pkl
```

Leptothorax

```
classifiers/leptothorax.random_forest.30.pkl 
classifiers/leptothorax.random_forest.50.pkl
classifiers/leptothorax.random_forest.100.pkl
```

## Acknowledgements

* Thank you Sean McGregor and Tomas Kay for providing the labeled images!
