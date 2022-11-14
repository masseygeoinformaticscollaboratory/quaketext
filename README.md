# QuakeText project - Impact NER data formatting, training and testing

#### Semester 2 2022

#### Sophie Francis

All folders contain a virtual environment venv to store all import packages specific to each task. Some of these are large and have not been uploaded to GitHub

## ./CSVtoJSONcode

These file involves the code for transformation from raw annotation data to the finaltags.json format that is used for processing.

##### All created csv files use tab delimitation

### Mechanical Turk

#### convertCSVtoJSON.py

The first step for converting the raw data from MT to a basic json format.

#### extract_tags.py

Produces the JSON outputs and some csv outputs for analysis.
Functions to check for overlapping tags and extra whitespace, the program first writes to the all workers and tag count CSV files. The tagcount.csv is then read from to extract only the tags that have above the minimum threshold to create a new dictionary for the finaltags.json file

#### review_tags_for_approvalMT.py

Is a helper program to visually represent the tags that are in MT when reviewing jobs. This takes the start and end indexes and prints the word that was tagged in a csv file.

### Light Tag

#### lighttag_json_reformat.py

The output from lightTag is in JSON, to remove the extra metadata, this program outputs a lighttag_finaltags.json that is formatted in the same way as the Mechanical Turk data previously. Outputs a light_tag_results.csv for visual inspection.
Also contains the function to create a new joined CSV file for both the light tag and MTurk data to combine the datasets in one place.

## ./NER_key_value_pair_list

#### ner_tag_list.py

The original file to calculate the list impacts

#### ner_tag_list_lem.py

Edits to look at the lemmatized and stemming words. Each section can be commented in when switching between.

Both files calculate the metrics at the end, and output to terminal

## ./NER_Spacy

#### NER_spacy_training.py

Contains the training program and data processing steps.

#### output_metrics.py

Takes the metrics results from each 10 fold validation round to a csv file for average calculations

### Commands to train the spacy pipeline:

### Building files

getting data from finaltags MT and lighttag to create .spacy files to train and test on

python NER_spacy_training.py

### Fill config (if it doesn't exist)

fill config file up - get base config details from https://spacy.io/usage/training

python -m spacy init fill-config base_config.cfg config.cfg

### Training

python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./dev.spacy

or use the file paths of the 10 fold validation locations:

example using round 5 of the none-excluded data from the 10 fold validation training
python -m spacy train config.cfg --output ./none-ex/output_5 --paths.train ./training-none-ex/train_5.spacy --paths.dev ./testing-none-ex/dev_5.spacy

### Evaluation

create evaluation of training pipeline and html output of samples default number is 25 but can increase this with --displacy-limit https://spacy.io/api/cli#evaluate

python -m spacy evaluate output\model-last dev.spacy --output .\eval.json --displacy-path .

use model-best for best validation scores
python -m spacy evaluate output\model-best dev.spacy --output .\eval.json --displacy-path .

python -m spacy evaluate none-ex\output_8\model-best testing-none-ex\dev_8.spacy --output .\eval_none_ex_8.json --displacy-path .

## ./NER_BERT_Pytorch

#### bert_create_bio_files.py

Creation of BIO files for BERT processing, uses regex to split up tweets and tags labels with the B and I tag elements. Creates 10 files at 10% increments for testing separation.

## ./BERT_impacts

#### BERT_impacts\bert_tokenizer.py

The program is able to use an AutoTokenizer on the following models:

1. bert-base-cased
2. bert-base-uncased
3. distilbert-base-cased
4. distilbert-base-uncased
5. albert-base-v2
6. roberta-base
7. xlnet-base-cased

The data files require separation in different folders. For each of the training steps there are 10 folder each containing a training and testing seperation of data. For training 0, files 1-9 are used for training and 0 for testing and so on.

Each model has its own csv file for results

The testing output can be viewed using the predict.ipynb through inputting the sentence and the associated model. Results are output into the model_output folder

## ./inter-annotator-agreement

#### lighttag-iaa.py

Calculation for the Cohen's Kappa agreement between the tagging for the common 200 set of data for Light Tag annotation. Prints to terminal.

#### mturk-iaa.py

Calculation for the Cohen's Kappa agreement between the top 2 taggers within the Mechanical Turk annotation. Prints to terminal.

## ./MT_json_review_code

Early files that were used in the review process of Mechanical turk tweet annotations before the python code was adapted to output to a csv for review.
