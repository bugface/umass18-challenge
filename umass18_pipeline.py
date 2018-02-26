'''
This is a pipeline e2e system for umass18 chanllenge

The pipeline will take the raw txt input files, preprocess, tagging and output bioc annotated files
'''
import os
import logging
from umass18_map_data import preprocess_data_sent_tokenization_and_position_mapping
from umass18_tagging import tagging
from umass18_gen_bioc import gen_bioc
from umass18_config import CORPUS_DIR, PREPROCESSED_CORPUS_DIR, PRE_TRAINED_MODEL, TAG_DILIMITER, EVALUATION_DIR

FORMAT = '%(asctime)-20s %(name)-5s %(levelname)-10s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("pipeline")

def main():
    '''
     umass chanllenge pipeline procedure:
     1. preprocess document using sentence tokenization and map the positions between original files and preprocessed files
     2. submit each sent file for tagging using NER_tagger and best pre_trained model
     3. merged the tagged file with mapping file and write the BIO back to .bioc file
     4. evaluate the results with the evaluate script 
    '''
    logger.info("reading config...")
    logger.info("input corpus data for tagging dir: %s"%CORPUS_DIR)
    assert os.path.isdir(CORPUS_DIR), "Input corpus for tagging directory is not found, check the config"
    logger.info("preprocessed corpus data dir: %s"%PREPROCESSED_CORPUS_DIR)
    if not os.path.isdir(PREPROCESSED_CORPUS_DIR):
        os.mkdir(PREPROCESSED_CORPUS_DIR)
    logger.info("pre-trained model: %s"%PRE_TRAINED_MODEL)
    assert os.path.isdir(PRE_TRAINED_MODEL), "The pre-trained model is not found, check the config"

    logger.info("preprocess...")
    preprocess_data_sent_tokenization_and_position_mapping(CORPUS_DIR, PREPROCESSED_CORPUS_DIR)

    logger.info("tagging...")
    tagging(PREPROCESSED_CORPUS_DIR, TAG_DILIMITER, PRE_TRAINED_MODEL)

    logger.info("generate bioc files...")
    gen_bioc(PREPROCESSED_CORPUS_DIR, EVALUATION_DIR, TAG_DILIMITER)

if __name__ == '__main__':
    main()