'''
The functions in this script are designed to processed the annotation file and txt files
'''
import os
from umass18_sentences_tokenization_index import SenTokBound
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
import logging

FORMAT = '%(asctime)-20s %(name)-5s %(levelname)-10s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("preprocess")

def work(fn, idir, odir, cnt):
    sent = SenTokBound()
    #text=file(idir+'/'+fn).read().rstrip()
    text=open(idir+'/'+fn).read().rstrip()
    
    result = sent.sentence(text,-1)
    ofn=odir+'/'+fn+'.sent.txt'
    if not os.path.isdir(odir):
        os.mkdir(odir)
    fo=open(ofn,'w')
    fo.write(result.strip()+'\n')
    ofn=odir+'/'+fn+'.wmap.txt'
    fo=open(ofn,'w')
    #fo.write(sent.get_map()+'\n')
    lines=sent.get_word_map()
    fo.write('\n'.join(lines)+'\n')
    fo.close()
    return "done %s"%fn


def preprocess_data_sent_tokenization_and_position_mapping(idir, odir):
    ct=0
    with ProcessPoolExecutor(max_workers=(cpu_count()-1)) as executor:
        for fnn in os.listdir(idir):
            if fnn.startswith('.'):
                continue
            ct=ct+1
            # logger.info(fnn)
            future_ = executor.submit(work, fnn, idir, odir, ct)
            logger.info(future_.result())

def test():
    idir="corpus"
    odir="corpus_sent"
    rdir = "ref_for_test/corpus_sent"
    preprocess_data_sent_tokenization_and_position_mapping(idir, odir)

    gen = os.listdir(odir)
    ref = os.listdir(rdir)

    assert len(gen) == len(ref), "generated file number are not the same as reference"

    ref = set(ref)
    #logger.info(ref)

    for file in gen:
        #logger.info(file)
        if file not in ref:
            logger.info("generated files are not the same as reference")
        else:
            with open(odir+"/"+file, "r") as f1, open(rdir+"/"+file, "r") as f2:
                for line_pair in zip(f1.read().strip().split("\n"), f2.read().strip().split("\n")):
                    if line_pair[0] != line_pair[1]:
                        logger.info(file)
                        logger.info(line_pair[0])
                        logger.info(line_pair[1])

if __name__ == '__main__':
    test()