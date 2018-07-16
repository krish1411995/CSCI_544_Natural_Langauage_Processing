# Overview
A naive Bayes classifier to identify hotel reviews as either true or fake, and either positive or negative. I have used the word tokens as features for classification.
I have extracted features by removing the stop-words, used smoothing techniques and removed punctuation with lowering the cases so that it does not create discrepency.

## Data
A set of training and development data will be made available as a compressed ZIP. The uncompressed archive will have the following files:

- One file train-labeled.txt containing labeled training data with a single training instance (hotel review) per line (total 960 lines). The first 3 tokens in each line are:
  * a unique 7-character alphanumeric identifier
  * a label True or Fake
  * a label Pos or Neg
These are followed by the text of the review.
- One file dev-text.txt with unlabeled development data, containing just the unique identifier followed by the text of the review (total 320 lines).
- One file dev-key.txt with the corresponding labels for the development data, to serve as an answer key.
- Readme and license files.

## Programs
I have two programs: nblearn.py will learn a naive Bayes model from the training data, and nbclassify.py will use the model to classify new data. The learning program will be invoked in the following way:

```
> python nblearn.py /path/to/input
```

The argument is a single file containing the training data; the program will learn a naive Bayes model, and write the model parameters to a file called nbmodel.txt.

- The model file will contain sufficient information for nbclassify.py to successfully label new data.
- The model file will be human-readable, so that model parameters can be easily understood by visual inspection of the file.
- The classification program will be invoked in the following way:

```
> python nbclassify.py /path/to/input
```

The argument is a single file containing the test data file; the program will read the parameters of a naive Bayes model from the file nbmodel.txt, classify each entry in the test data, and write the results to a text file called nboutput.txt in the same format as the answer key.
