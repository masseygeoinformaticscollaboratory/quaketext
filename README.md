# Pipeline for Impact NER training and texting

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
