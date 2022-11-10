# QuakeText project work

Semester 2 2022
Sophie Francis

# Pipeline for Impact NER training and testing

## CSVtoJSONcode

These file involves the code for transformation from raw annotation data to the finaltags.json format that is used for processing.

### Mechanical Turk

**convertCSVtoJSON.py** is the first step for converting the raw data from MT to a basic json format.
**extract_tags.py** produces the JSON outputs and some csv outputs for analysis.
Functions to check for overlapping tags and extra whitespace, the program first writes to the all workers and tag count CSV files. The tagcount.csv is then read from to extract only the tags that have above the minimum threshold to create a new dictionary for the finaltags.json file

**review_tags_for_approvalMT.py** is a helper program to visually represent the tags that are in MT when reviewing jobs. This takes the start and end indexes and prints the word that was tagged in a csv file.

### Light Tag

**lighttag_json_reformat.py** The output from lightTag is in JSON, to remove the extra metadata, this program outputs a lighttag_finaltags.json that is formatted in the same way as the Mechanical Turk data previously. Outputs a light_tag_results.csv for visual inspection.
Also contains the function to create a new joined CSV file for both the light tag and MTurk data to combine the datasets in one place.

## Spacy

Commands to train the spacy pipeline:

### Building files

getting data from finaltags MT and lighttag to create .spacy files to train and test on
python NER_spacy_training.py

### Fill config (if it doesn't exist)

fill config file up - get base config details from https://spacy.io/usage/training
python -m spacy init fill-config base_config.cfg config.cfg

### Training

python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./dev.spacy

### Evaluation

create evaluation of training pipeline and html output of samples default number is 25 but can increase this with --displacy-limit https://spacy.io/api/cli#evaluate

python -m spacy evaluate output\model-last dev.spacy --output .\eval.json --displacy-path .

use model-best for best validation scores
python -m spacy evaluate output\model-best dev.spacy --output .\eval.json --displacy-path .

C:\QuakeText_code\NER_spacy>python -m spacy train config.cfg --output ./none-ex/output_5 --paths.train ./training-none-ex/train_5.spacy --paths.dev ./testing-none-ex/dev_5.spacy
