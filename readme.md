# NLP Challenges for Detecting Medication and Adverse Drug Events from Electronic Health Records (MADE1.0)

## System
> Named entity recognition (NER): develop systems to automatically detect mentions of medication name and its attributes (dosage, frequency, route, duration), as well as mentions of ADEs, indications, other signs & symptoms.

## environment
- python 2.7

## How to run the system
- change the umass18_config file content to reflect the data location for system input and output
```python
CORPUS_DIR = "the chanllenge original corpus files directory" 
PREPROCESSED_CORPUS_DIR = "the direcoty containing output sentence-tokenized files and words-position-map files"
EVALUATION_DIR = "the directory containing output .bioc files for evaluation"
PRE_TRAINED_MODEL = "the directory containing the pre-trained model"
```

- run umass18_pipeline, the necessary information about the process will be logged in the console or termial
```sh
pip install -r requirements.txt

#On windows machine: pre-installed anaconda2 
conda install mkl-service
conda install m2w64-toolchain
python umass18_pipeline.py

#On unix system preinstalled miniconda2-latest
conda install mkl-service
export MKL_THREADING_LAYER=GNU
THEANO_FLAGS=device=cuda2(when you using GPU for tagging task)
python umass18_pipeline.py
```

- run evaluation script on generated data, using the newly generated eval directory which contains all the predicted .bioc files as evaluation predicted directory (This evaluation must be run using python3 because the evaluation script provided by chanllenge organizer was written in python3)
```sh
pip install bioc future
python3 bioc_evaluation.py <ground truth .bioc files directory> <predicted .bioc files directory> <corpus files directory>
```

## Authors
>Yonghui Wu Ph.D.*, Xi Yang Ph.D.

## contact
> the model was encrypted, if you need password, please contact alexgre@ufl.edu
