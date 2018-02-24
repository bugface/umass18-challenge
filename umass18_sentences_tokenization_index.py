import sys
import os
import re
import logging

FORMAT = '%(asctime)-20s %(name)-5s %(levelname)-10s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("SenTokBound")

class SenTokBound:
    def __init__(self):
        self.tok_sent=None
        self.sent_txt=""
        self.pos_map={}
        self.otxt=""
        self.cur_sent_len=0
        
        self.__stop_symbol = set(['.', '\n']) 
        self.__stop_list = []

        #find CNLP_home
        path = os.path.abspath(__file__)
        #logger.info('file path %s' % path)

        pos = path.rfind('/')
        path = path[:pos]
        self.__VCNLP_home = ""#os.path.abspath(path + '/../..')
        ##logger.info 'CNLP_TK_home: ', self.__VCNLP_home
        self.__abbr_dir = self.__VCNLP_home + 'resource/abbr.txt'
        self.__english_dir = self.__VCNLP_home + 'resource/word.txt'

        #self.__abbr = file(self.__abbr_dir).read().strip().split('\n')
        self.__abbr = open(self.__abbr_dir).read().strip().split('\n')
        self.__abbr = set(map(lambda  x: x.strip().lower(), self.__abbr))
        
        #self.__english = file(self.__english_dir).read().strip().split('\n')
        self.__english = open(self.__english_dir).read().strip().split('\n')
        self.__english = set(map(lambda x: x.strip().lower(), self.__english))

        self.__abbr = self.__abbr - self.__english

        #logger.info ('Load abbrs: ', self.__abbr_dir, len(self.__abbr))
        #logger.info ('Load english: ', self.__english_dir, len(self.__english))

        self.__sep_symbol = set([',', '?', '!', ':', '\'', '"', '(', ')', '[', ']', '{', '}', '<', '>','+','-']) # these symbols will be seperated with words

        #
        #The prep and det are borrowed from Josh's perl edition.  These words are posiblely not a sentence boundary
    
        self.__prep = set(['about','above','across','after','against','aka','along','and','anti','apart','around','as','astride','at','away','because','before','behind','below','beneath','beside','between','beyond','but','by','contra','down','due to','during','ex','except','excluding','following','for','from','given','in','including','inside','into','like','near','nearby','neath','of','off','on','onto','or','out','over','past','per','plus','since','so','than','though','through','til','to','toward','towards','under','underneath','versus','via','where','while','with','within','without', 'also'])

        self.__det = set(['a', 'an', 'the'])

        self.__non_stop_punct = set([',', ';'])

        self.__sentence_word = set(['we','us','patient','denies','reveals','no','none','he','she','his','her','they','them','is','was','who','when','where','which','are','be','have','had','has','this','will','that','the','to','in','with','for','an','and','but','or','as','at','of','have','it','that','by','from','on','include'])

        self.__units = set(['mg','lb','kg','mm','cm','m','doz', 'am', 'pm', 'mph', 'oz', 'ml', 'l', 'mb'])

        #logger.info ('Sentence segment initiate over')
    

    def __is_num_list(self, word):
        if re.match(r'\d+\.$', word): #num list
            return True
        return False
    
    #
    #Return the position of '.' in a word. -1 denote there are no '.' appeared
    def __has_dot(self, word):
        i = 0
        lenn = len(word)
        while i < lenn:
            if word[i] == '.':
                ##logger.info 'has_dot: ', i
                return i
            i = i + 1

        return - 1

    #return the number of dot in word
    def __num_dot(self, word):
        i = 0
        for w in word:
            if w == '.':
                i = i + 1
        return i


    def __is_stop_punct(self, w):
        if w == '?' or w == '!' or w == '.': 
            return True
        else:
            return False

    #Identify all numbers
    def __is_digit(self, word):
        if re.match(r'[+-]?\d*[.]?\d+$', word): #all number
            return True
        return False

    def __clean(self, text):
        result = re.sub('\t|_{4,}|-{4,}', ' ', text)

        return result

    def __preprocess(self, text):
        lines = text.strip().split('\n')
        lines = map(lambda x: x.strip(), lines)
        result = []
        for line in lines:
            if len(line) == 0:
                continue
            nline = ''
            line = self.__clean(line)
            for w in line:
                if w in self.__sep_symbol:
                    nline = nline + ' ' + w + ' '
                else:
                    nline = nline + w
            nline = re.sub('[ ]{2,}', ' ', nline)
            nline = nline.strip()
            if len(nline) > 0: 
                result.append(nline)
       
        return result

    # the public function to judge whether the letter 'w' is a puncutation
    def is_punct(self,w):
        if w == ',' or w =='?' or w == '!' or w == ',' or w == ';' or w == '-' or w == '(' or w == ')' or w== ':' or w=='/':
            return True

        return False

    def is_sep(self,c):
        flag=False
        if c==' ' or c=='\n' or self.is_punct(c):
            flag=True
        return flag

    def tok(self):
        txt=self.otxt
        llen=len(txt)
        #logger.info ('llen %d'%llen)
        cur_pos=0
        while cur_pos<llen and (txt[cur_pos] ==' ' or txt[cur_pos]=='\n' or txt[cur_pos]=='\r'):
            cur_pos=cur_pos+1
        self.tok_sent=[]
        tsent=[]
        pre_pos=cur_pos
        while cur_pos<llen :
            ch=txt[cur_pos]
            if not self.is_sep(ch):
                cur_pos=cur_pos+1
            else:
                if cur_pos> pre_pos:
                    ##logger.info [pre_pos,cur_pos]
                    tsent.append([pre_pos,cur_pos])
                if ch == '\n':
                    if len(tsent)>0:
                        self.tok_sent.append(tsent)
                    tsent=[]
                    
                if self.is_punct(ch):
                    tsent.append([cur_pos,cur_pos+1])
                cur_pos=cur_pos+1
                while cur_pos<llen and (txt[cur_pos] ==' '):
                    cur_pos=cur_pos+1
                pre_pos=cur_pos


    def get_map(self):
        stt=""
        lt=[]
        for k,v in self.pos_map.iteritems():
            lt.append([k,v])
        indices=range(len(lt))
        #indices.sort(lambda x,y: cmp(lt[x][0],lt[y][0])) # cmp is deprecated in the python3
        indices.sort(lambda x,y: (lt[x][0]>lt[y][0])-(lt[x][0]<lt[y][0]))
        for i in range(len(indices)):
            stt=stt+str(lt[indices[i]][0])+'\t'+str(lt[indices[i]][1])+'\n'
        return stt

    def get_word_map(self):
        lt=[]
        lines=self.sent_txt.split('\n')
        spos=0
        epos=0
        for line in lines:
            stt=""
            words=line.strip().split(None)
            for word in words:
                ##logger.info 'spos ',spos
                epos=spos+len(word)
                ##logger.info 'epos ',epos
                ##logger.info spos,epos,word
                stt=stt+word+'\t'+str(spos)+'\t'+str(epos)+'\t'+str(self.pos_map[spos])+'\t'+str(self.pos_map[epos])+'\n'
                spos=epos+1
            lt.append(stt)
        return lt
    
    def add_tok(self,tok):
        if len(self.sent_txt)==0 or self.sent_txt.endswith('\n'):
            spos=len(self.sent_txt)
            self.sent_txt=self.sent_txt+self.otxt[tok[0]:tok[1]]
            self.cur_sent_len=self.cur_sent_len+tok[1]-tok[0]  
            epos=len(self.sent_txt)
        else:
            spos=len(self.sent_txt)+1
            self.sent_txt=self.sent_txt+' '+self.otxt[tok[0]:tok[1]]
            self.cur_sent_len=self.cur_sent_len+tok[1]-tok[0]+1
            epos=len(self.sent_txt)
        self.pos_map[spos]=tok[0]
        self.pos_map[epos]=tok[1]
        self.last_tok=tok

    def add_tok_cr(self):
        self.sent_txt = self.sent_txt + '\n'
        self.cur_sent_len=0

#This is the main procedure to process a string 'text;.
#Each line of the file is processed sequencially.
#For each line, first handle all the word with '.'; then handle the end of a line.
#If a '.' or the end of current line is a sentence boundary, insert a '\n' after them.

    def sentence(self, text, min_len):
        if not text.endswith('\n'):
            text=text+'\n'
        self.otxt=re.sub('\[\*\*|\*\*\]','   ',text)
        self.otxt=re.sub('\t',' ',self.otxt)
        ##logger.info self.otxt
        self.tok()
        #logger.info ('self.tok_sent')
        #logger.info (self.tok_sent)
        
        i = 0
        while i <  len(self.tok_sent):
            if min_len > 0: 
                if len(self.tok_sent[i]) <= min_len: #do not merge very short lines
                    for tok in self.tok_sent[i]:
                        self.add_tok(tok)
                    self.add_tok_cr()
                    i = i + 1
                    continue

            j = 0
            toks=self.tok_sent[i]
            while j < len(toks):
                tok=toks[j]
                word = text[tok[0]:tok[1]]
                pos = self.__has_dot(word)

                if j + 1 < len(toks):
                    next_word = text[toks[j+1][0]:toks[j+1][1]]
                else:
                    next_word = ''

                if pos >= 0:
                    dot_num = self.__num_dot(word)
                    if dot_num == 1:
                        if self.__is_digit(word):
                            self.add_tok(tok)
                        elif self.__is_stop_punct(word):  #single dot
                            self.add_tok(tok)
                            self.add_tok_cr()
                        elif pos == 0: #'.' on the begining, keep it original,  do not change
                            self.add_tok(tok)
                        elif pos == len(word) - 1: # on the end of word
                            if self.__is_num_list(word):
                                ##logger.info 'num list: ', word
                                if j == 0 and next_word.lower() not in self.__sentence_word: #1. Percocet 5/325 one p.o.
                                    self.add_tok(tok)
                                else: #postoperative day 3.
                                    ntok=[tok[0],tok[1]-1]
                                    self.add_tok(ntok)
                                    ntok=[tok[1]-1,tok[1]]
                                    self.add_tok(ntok)
                                    self.add_tok_cr()
                            # afebrile .
                            elif word[:-1].lower() not in self.__abbr and word.lower() not in self.__abbr:
                                ##logger.info 'english: ', word
                                ntok=[tok[0],tok[1]-1]
                                self.add_tok(ntok)
                                ntok=[tok[1]-1,tok[1]]
                                self.add_tok(ntok)
                                self.add_tok_cr()
                            else: #abbreviations
                                ##logger.info 'abbr: ', word
                                if j + 1 < len(toks):
                                    next_word = text[toks[j+1][0]:toks[j+1][1]]
                                else:
                                    next_word = ''
                                ##handling exceptiong for unit: 3 cm. should be broken into 3 cm .  0.5cm.  
                                lword = word[:-1]

                                if j == len(toks)-1: # the last word
                                    ntok=[tok[0],tok[1]-1]
                                    self.add_tok(ntok)
                                    ntok=[tok[1]-1,tok[1]]
                                    self.add_tok(ntok)
                                    self.add_tok_cr()
                                elif lword in self.__units:
                                    ntok=[tok[0],tok[1]-1]
                                    self.add_tok(ntok)
                                    ntok=[tok[1]-1,tok[1]]
                                    self.add_tok(ntok)
                                    self.sent_txt = self.sent_txt + '\n'
                                #elevation MI. The patient was
                                elif len(next_word) > 0 and next_word[0].isupper():
                                    ##logger.info 'abbr add enter'
                                    ntok=[tok[0],tok[1]-1]
                                    self.add_tok(ntok)
                                    ntok=[tok[1]-1,tok[1]]
                                    self.add_tok(ntok)
                                    self.add_tok_cr()
                                else:
                                    self.add_tok(tok)
                            ##logger.info 'after end dot: ', tmp
                        else: #'.' is on the center of a word. Do not handle this now. If the corpus contians too much
                            # go.The,  we have to handle this.
                            # the token has a '.' in the center.

                            words_center = word.split('.')
                            right_word = words_center[1]

                            if right_word[0].isupper() and ((right_word in self.__sentence_word) or( right_word.lower() in self.__english) ):
                                tlen=len(right_word)
                                ntok=[tok[0],tok[1]-tlen-1]
                                self.add_tok(ntok)
                                ntok=[tok[1]-tlen-1,tok[1]-tlen ]
                                self.add_tok(ntok)
                                self.add_tok_cr()
                                ntok=[tok[1]-tlen,tok[1]]
                                self.add_tok(ntok)
                            else:
                                self.add_tok(tok)
                            ##logger.info 'tmp: ', tmp
                    else: # for the dot_num > 1, almost all of them are abbreviations.
                        #Handle:  CK-MB of 9.1. His post
                        if j + 1 < len(toks):
                            next_word = text[toks[j+1][0]:toks[j+1][1]]
                        else:
                            next_word = ''

                        if re.match('[a-zA-Z0-9]+\.{2,}',word):
                            pos=word.find('.')
                            ntok=[tok[0],tok[0]+pos]
                            self.add_tok(ntok)
                            ntok=[tok[0]+pos,tok[1]]
                            self.add_tok(ntok)
                        elif word[-1] == '.':
                            lword = word[:-1]
                            if self.__is_digit(word[:-1]):
                                ntok=[tok[0],tok[1]-1]
                                self.add_tok(ntok)
                                ntok=[tok[1]-1,tok[1]]
                                self.add_tok(ntok)
                                self.add_tok_cr()

                            elif re.match(r'\d*[.]?\d+[a-zA-Z]+$', lword) or re.match(r'\d{1,2}:\d{1,2}[a-zA-Z]+$', lword):
                                pos = 0
                                while pos < len(lword) and (lword[pos].isdigit() or lword[pos] == '.' or lword[pos] == ':'):
                                    pos = pos + 1
                                w1 = lword[:pos]
                                w2 = lword[pos:]
                                if w2 in self.__units:
                                    ntok=[tok[0],tok[0]+pos]
                                    self.add_tok(ntok)
                                    ntok=[tok[0]+pos,tok[1]-1 ]
                                    self.add_tok(ntok)
                                    ntok=[tok[1]-1,tok[1]]
                                    self.add_tok(ntok)
                                    self.add_tok_cr()
                                elif len(next_word) > 0 and next_word[0].isupper():
                                    ntok=[tok[0],tok[1]-1]
                                    self.add_tok(ntok)
                                    ntok=[tok[1]-1,tok[1]]
                                    self.add_tok(ntok)
                                    self.add_tok_cr()
                                else:
                                    self.add_tok(tok)

                            else:
                                #Handle: condition without the need for O.T. or P.T.  He is being
                                ##logger.info 'multi dot: ', word


                                if len(next_word) > 0 and next_word[0].isupper() and next_word.lower() in self.__sentence_word:
                                    ##logger.info 'multi dot add enter'
                                    self.add_tok(tok)
                                    self.add_tok_cr()
                                else:
                                    self.add_tok(tok)

                        else:
                            self.add_tok(tok)
                else: # normal words,  just add it
                    self.add_tok(tok)

                j = j + 1

            ##logger.info 'before handle end: ', tmp
            #handle the '\n' end of line
            #get the first word of next line
            
            if i + 1 < len(self.tok_sent):
                len_next_line = len(self.tok_sent[i+1])
                ##logger.info 'self.tok_sent[i+1][0] ',self.tok_sent[i+1]
                next_word = text[self.tok_sent[i+1][0][0]:self.tok_sent[i+1][0][1]]
                last_word = text[self.last_tok[0]:self.last_tok[1]]

                if self.sent_txt[-1] == '.':
                    ##logger.info 'end with dot, the dot is part of abbreviation: e.g.,  Dr.'
                    if len(self.sent_txt) >= 2 and self.sent_txt[-2] !=  ' ' and ( not next_word == '-') and ( not next_word == '----')\
                       and (not self.__is_num_list(next_word)) and ( not next_word[0].isupper()):
                        pass
                    else: #lesion ., or next line could not be merged
                        if not self.sent_txt.endswith('\n'):
                            self.add_tok_cr()

                elif self.sent_txt[-1] != '.' and self.sent_txt[-1] != ':':
                    #handle exceptions when the senctence is ended with words in prep, det and non_stop_punct
                    last_word_lower = last_word.lower()
                    #handle short lines
                    if min_len > 0 and len_next_line <= min_len:
                        self.add_tok_cr()
                    elif next_word.lower() in self.__units:
                        pass
                    elif not next_word[0].isalpha() and not last_word.lower() in self.__prep:
                        if not self.sent_txt.endswith('\n'):
                            self.add_tok_cr()
                    elif last_word_lower in self.__prep or last_word_lower in self.__det or last_word_lower in self.__non_stop_punct:
                        pass
                    elif ( not next_word == '-') and ( not next_word == '----') and (not self.__is_num_list(next_word)) and ( not next_word[0].isupper()) and (not next_word.lower() in self.__english): #
                        pass
                    elif   next_word.lower() in self.__english:
                        pass
                    else:
                        if not self.sent_txt.endswith('\n'):
                            self.add_tok_cr()

                else:
                    ##logger.info 'add enter'
                    self.add_tok_cr()
            else: # the last line
                ##logger.info 'lastline'
                self.add_tok_cr()
            i = i + 1


        return self.sent_txt