import logging
import sys
import os
# import shutil

FORMAT = '%(asctime)-20s %(name)-5s %(levelname)-10s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("make_bioc")

'''
output format:

<?xml version='1.0' encoding='utf-8' standalone='yes'?>
<collection>
  <source></source>
  <date></date>
  <key></key>
  <document>
    <id>1_9</id>
    <passage>
      <offset>0</offset>
      <annotation id="591">
        <infon key="type">SSLIF</infon>
        <location length="6" offset="3589"/>
        <text>fevers</text>
      </annotation>
      <relation id="102">
        <infon key="type">reason</infon>
        <node refid="631" role="annotation 1"/>
        <node refid="629" role="annotation 2"/>
      </relation>
    </passage>
  </document>
</collection>
'''

def make_xml_body_head(file_id):
    return """<?xml version='1.0' encoding='utf-8' standalone='yes'?>
<collection>
  <source></source>
  <date></date>
  <key></key>
  <document>
    <id>%s</id>
    <passage>
      <offset>0</offset>"""%file_id


def make_xml_body_tail():
    return"""
    </passage>
  </document>
</collection>"""


def make_xml_annotation(wid, tag, length, offset, text):
    return """
      <annotation id="%d">
        <infon key="type">%s</infon>
        <location length="%d" offset="%d"/>
        <text>%s</text>
      </annotation>"""%(wid, tag, length, offset, text)


def make_xml_relation():
    return """"""


def merge_tagged_map_files(tagged_file, map_file, dm):
    tagged_sents = []
    map_sents = []
    with open(tagged_file, "r") as ft, open(map_file) as fm:
        #process tagged file
        '''
            output as
            [[(w1, tag), (w2, tag), (w3, tag)...],...]
        '''
        for line in ft:
            tagged_sent = []
            words = line[:-1].split(" ")

            for each in words:
                word_tag = each.split(dm)
                tagged_sent.append((word_tag[0], word_tag[-1]))
            tagged_sents.append(tagged_sent)

        # logger.info(tagged_sents)

        #processmap_file, assign each word its position in original txt file
        '''
            output as
            [[(w1, s, e), (w2, s, e), (w3, s. e)...],...]
        '''
        map_sent = []
        for line in fm:
            line_content  = line[:-1].split('\t')

            if len(line) < 2:
                #this is the empty line used to seperate the lines in the text file
                map_sents.append(map_sent)
                map_sent=[]
            else:
                map_sent.append(tuple(line_content))

        # logger.info(map_sents)

    #merge the two lists into by matching each word in each sentence
    merged_sents = []
    for s_bio, s_tag in zip(map_sents, tagged_sents):
        n_sent = []
        if len(s_bio) != len(s_tag):
            logger.error("two sentences are not the same length")
            logger.info(" ".join(s_bio))
            logger.info(" ".join(s_tag))
            sys.exit(1)
        for w_bio, w_tag in zip(s_bio, s_tag):
            if w_bio[0] == w_tag[0]:
                n_sent.append(tuple([each for each in w_bio] + [w_tag[-1]]))
            else:
                logger.error("words in two sentendces are not same")
                logger.info(w_bio)
                logger.info(w_tag)
                sys.exit(1)    
        merged_sents.append(n_sent)

    # logger.info(merged_sents)
    return merged_sents

def gen_bioc(src_dir, dst_dir, dm):
    global_id = 1
    out_files = []
    map_files = []
    tagged_files = []

    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)
    
    for in_file in os.listdir(src_dir):
        file_type = in_file.split(".")[1]
        if file_type == "tagged":
            tagged_files.append(in_file)
        elif file_type == "wmap":
            map_files.append(in_file)
        else:
            out_files.append(in_file.split(".")[0] + ".bioc.xml")

    out_files.sort()
    map_files.sort()
    tagged_files.sort()

    # logger.info(out_files)
    # logger.info(map_files)
    # logger.info(tagged_files)

    for file_pair in zip(tagged_files, map_files, out_files):
        assert file_pair[0].split(".")[0] == file_pair[1].split(".")[0] == file_pair[2].split(".")[0], "files must have the same id, check files list order"
        file_id = file_pair[0].split(".")[0]

        tagged_file = src_dir + "/" + file_pair[0]
        map_file = src_dir + "/" + file_pair[1]
        output_file = dst_dir + "/" + file_pair[2]

        merged_sents = merge_tagged_map_files(tagged_file, map_file, dm)
        logger.info("processing file with id as %s"%file_pair[0].split(".")[0])    

        #combined annotations
        ann = ""
        
        #process the start and end position to length and offset
        #remove BIO to convert into terms with entity tag
        # index = 0
        terms, offset, tag, prev_tag, cur_term, entity_end = "", 0, "", "O", "", 0

        for i, sent in enumerate(merged_sents):
            # ''' e.g. 
            #     ('Hospital', '0', '8', '4', '12', 'O')
            #     ('mantle', '433', '439', '664', '670', 'B-Indication')
            #     ('cell', '440', '444', '671', '675', 'I-Indication')
            # '''
            for word in sent:
                cur_tag = word[-1]
                start = int(word[-3])
                end = int(word[-2])
                
                #replace '<' and '>' with '&lt;' and '&gt;'
                if word[0] == "<":
                    cur_term = "&lt;"
                elif word[0] == ">":
                    cur_term = "&gt;"
                else:
                    cur_term = word[0]

                if cur_tag == "O":
                    if prev_tag != "O":
                        '''
                        <annotation id="%d">
                            <infon key="type">%s</infon>
                            <location length="%d" offset="%d"/>
                            <text>%s</text>
                        </annotation>"""%(wid, tag, length, offset, text)
                        '''
                        ann += make_xml_annotation(global_id, tag, entity_end-offset, offset, terms.rstrip())
                        global_id += 1
                        terms, offset, tag = "", 0, ""
                else:
                    label = cur_tag.split("-")[0]
                    entity = cur_tag.split("-")[1]
                    if label == 'B':
                        if prev_tag == "O":
                            #assign current end to entity end
                            entity_end = end
                            #assgin cur entity to tag
                            tag = entity
                            #record the offset
                            offset = start
                            #add term into terms
                            terms += (cur_term + " ")
                        else:
                            '''
                                in case as (B-tag1 I-tag1 B-tag2 or B-tag1 B-tag2)
                                we need to first write tag1 into annotation
                                then reassign all tag2 information to vars
                            '''
                            ann += make_xml_annotation(global_id, tag, entity_end-offset, offset, terms.rstrip())
                            global_id += 1
                            terms, offset, tag= "", 0, ""
                            
                            #assign current end to entity end
                            entity_end = end
                            #assgin cur entity to tag
                            tag = entity
                            #record the offset
                            offset = start
                            #add term into terms
                            terms += (cur_term + " ")
                    elif label == "I":
                        #check BIO seq (I-tag must follow B-tag or I-tag)
                        # assert prev_tag != "O", "The previous tag of I-tag cannot be 'O': %s"%sent
                        #check BIO tag kind (I-tag must have the same tag type with its leading B-tag)
                        # assert entity == tag, "The current entity is not the same as leading B-tag entity: %s"%sent
                        if entity == tag:
                            #assign current end to entity end
                            entity_end = end
                            terms += (cur_term + " ")
                        else:
                            ann += make_xml_annotation(global_id, tag, entity_end-offset, offset, terms.rstrip())
                            global_id += 1
                            terms, offset, tag= "", 0, ""

                            #assign current end to entity end
                            entity_end = end
                            #assgin cur entity to tag
                            tag = entity
                            #record the offset
                            offset = start
                            #add term into terms
                            terms += (cur_term + " ")
                
                #reset prev_tag to cur_tag
                prev_tag = cur_tag

        #output the .bioc format
        head = make_xml_body_head(file_id)
        tail = make_xml_body_tail()

        with open(output_file, "w") as fw:
            fw.write(head + ann + tail)


def test():
    x = make_xml_body_head("1_1")
    y = make_xml_body_tail()
    z = make_xml_annotation(1, "treat", 10, 1220, "kill cancer")
    logger.info(x + z + y)

    # merge_tagged_map_files("ref_for_test/corpus_sent/1_9.tagged.txt", "ref_for_test/corpus_sent/1_9.wmap.txt", "^")
    gen_bioc("ref_for_test/test_sent/", "ref_for_test/test_eval", "^")

    '''
    in 13_95 provided by umass
     <annotation id="10325">
        <infon key="type">SSLIF</infon>
        <location length="27" offset="2503"/>
        <text>decrease \nsensation to LLE</text>
      </annotation>

    I think it is wrong to have \n there inside the text
    '''

if __name__ == '__main__':
    test()