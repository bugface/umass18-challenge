# NLP Challenges for Detecting Medication and Adverse Drug Events from Electronic Health Records (MADE1.0)

## System
> Named entity recognition (NER): develop systems to automatically detect mentions of medication name and its attributes (dosage, frequency, route, duration), as well as mentions of ADEs, indications, other signs & symptoms.

## environment
- python 2.7
- theano
- futures
- numpy
- scipy

## How to run the system
- install all the packages required
- change the config files content to reflect the data location for system input and output
- run umass18_pipeline, a eval output will be generated
- run evaluation script on generated data

## Authors
Yonghui Wu* Ph.D., Xi Yang Ph.D.

#remain bugs
1. replace < and > with &lt; and &rt;
2. debug length calculation