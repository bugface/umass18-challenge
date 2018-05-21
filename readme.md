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

