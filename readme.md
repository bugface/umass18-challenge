# All the code for taking chanllenge of MADE1.0 umass18

## NER is the folder containg all the code for name entity recognition tagging task 1
- the code is only the pipeline using pretrained model to predict the given data
- the training process is not included

## RE is the folder containg all the code for relation extraction task 2 and 3 (e2e)
- two models are used namely SVM and Random Forest
- SVM is based on LibSVM3.22, Random Forest is based on sciki-learn
- the jupyter notebook containing all the functions and experiment results for processing data for training, create models and prediction

## raw data are not provided, but can be obtained later since the MADE team from umass will release the data in the future to public

## the final results are listed below

- NER: f1-score(strict) 0.8322
- RE based on true entities: 0.847 (SVM)
- RE based on predicted entities from NER: 0.612 (SVM)

-please cite out paper:
```sh
@Article{Yang2019,
author="Yang, Xi
and Bian, Jiang
and Gong, Yan
and Hogan, William R.
and Wu, Yonghui",
title="MADEx: A System for Detecting Medications, Adverse Drug Events, and Their Relations from Clinical Notes",
journal="Drug Safety",
year="2019",
month="Jan",
day="02",
abstract="Early detection of adverse drug events (ADEs) from electronic health records is an important, challenging task to support pharmacovigilance and drug safety surveillance. A well-known challenge to use clinical text for detection of ADEs is that much of the detailed information is documented in a narrative manner. Clinical natural language processing (NLP) is the key technology to extract information from unstructured clinical text.",
issn="1179-1942",
doi="10.1007/s40264-018-0761-0",
url="https://doi.org/10.1007/s40264-018-0761-0"
}
```
