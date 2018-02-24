'''
The tagging program is written in python2
The pipeline is written in python3
Therefore, the os must have both python2 and python3 
check this in the pipeline.py to make sure we have both envs
'''
import logging
import os
# import execnet
import sys
sys.path.append('NER-tagger')
sys.setrecursionlimit(1000)
from tagger import run_tagging, load_model
# from multiprocessing import cpu_count
# from concurrent.futures import ProcessPoolExecutor

FORMAT = '%(asctime)-20s %(name)-5s %(levelname)-10s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("tagging")

# def call_python_version(Version, Module, Function, ArgumentList):
#     gw      = execnet.makegateway("popen//python=python%s" % Version)
#     channel = gw.remote_exec("""
#         from %s import %s as the_function
#         channel.send(the_function(*channel.receive()))
#     """ % (Module, Function))
#     channel.send(ArgumentList)
#     return channel.receive()

def tagging(idir, dm, model_path):
    # logger.info(os.getcwd())
    assert os.path.isdir(idir), "The directory for input files are not exit!"
    assert os.path.isdir(model_path), "The directory for model files are not exit!"
    #current version is single process implementation
    #TODO: change this function into multiprocess to increate the speed of tagging
    #load pre-trained model
    model, f_eval, parameters, word_to_id, char_to_id, tag_to_id = load_model(model_path)

    # with ProcessPoolExecutor(max_workers=(cpu_count()-1)) as executor:
    for each_file in os.listdir(idir):
        file_info = each_file.split(".")
        file_id = file_info[0]
        file_type = file_info[1]

        #NER_tagger using the sentences for tagging
        if file_type == "sent":
            output_file = idir + "/" + file_id + ".tagged.txt"
            input_file = idir + "/" + each_file
            
            #execnet
            # result = call_python_version("2.7", "tagger", "run_tagging",  
            #                  [model, input_file, output_file, dm]) 
            # logger.info(result) 
            
            #single process
            run_tagging(model, f_eval, parameters, word_to_id, char_to_id, tag_to_id, input_file, output_file, dm)
                
                #multiprocess
                # future_ = executor.submit(run_tagging, model, f_eval, parameters, word_to_id, char_to_id, tag_to_id, input_file, output_file, dm)
                # logger.info(future_.result())

def test():
    test_dir = "ref_for_test/corpus_sent"
    tagging(test_dir, "^", "NER-tagger/production_model/model1")

if __name__ == '__main__':
    test()