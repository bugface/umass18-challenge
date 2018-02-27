# NLP Challenges for Detecting Medication and Adverse Drug Events from Electronic Health Records (MADE1.0)

## System
> Named entity recognition (NER): develop systems to automatically detect mentions of medication name and its attributes (dosage, frequency, route, duration), as well as mentions of ADEs, indications, other signs & symptoms.

## environment
- python 2.7

## How to run the system
- install all the packages required
```sh
pip install -r requirements.txt
```

- change the umass18_config file content to reflect the data location for system input and output
```python
CORPUS_DIR = "the chanllenge original corpus files directory" 
PREPROCESSED_CORPUS_DIR = "the direcoty containing output sentence-tokenized files and words-position-map files"
EVALUATION_DIR = "the directory containing output .bioc files for evaluation"
PRE_TRAINED_MODEL = "the directory containing the pre-trained model"
```

- run umass18_pipeline, the necessary information about the process will be logged in the console or termial
```sh
#not using gpu for tagging(linux) (extremely slow!!!)
python umass18_pipeline.py

#not using gpu but with mkl for tagging(linux, miniconda2-latest)
conda install mkl-service 
python umass18_pipeline.py

#using gpu for tagging (linux, miniconda2-latest)
conda install mkl-service
export MKL_THREADING_LAYER=GNU
export THEANO_FLAGS=device=cuda0
python umass18_pipeline.py
```

- run evaluation script on generated data (This evaluation must be run using python3 because the evaluation script provided by chanllenge organizer was written in python3)
```sh
pip install bioc
python3 bioc_evaluation.py <ground truth .bioc files directory> <predicted .bioc files directory> <corpus files directory>
```

## Authors
>Yonghui Wu Ph.D.*, Xi Yang Ph.D.
