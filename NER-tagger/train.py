#!/usr/bin/env python
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

import os
import sys
import numpy as np
import optparse
import itertools
from collections import OrderedDict
from utils import create_input
import loader

from utils import models_path, evaluate, eval_script, eval_temp
from loader import word_mapping, char_mapping, tag_mapping
from loader import update_tag_scheme, prepare_dataset
from loader import augment_with_pretrained
from model import Model

# Read parameters from command line
optparser = optparse.OptionParser()
optparser.add_option(
    "-T", "--train", default="",
    help="Train set location"
)
optparser.add_option(
    "-d", "--dev", default="",
    help="Dev set location"
)
optparser.add_option(
    "-t", "--test", default="",
    help="Test set location"
)
optparser.add_option(
    "-s", "--tag_scheme", default="iobes",
    help="Tagging scheme (IOB or IOBES)"
)
optparser.add_option(
    "-l", "--lower", default="0",
    type='int', help="Lowercase words (this will not affect character inputs)"
)
optparser.add_option(
    "-z", "--zeros", default="0",
    type='int', help="Replace digits with 0"
)
optparser.add_option(
    "-c", "--char_dim", default="25",
    type='int', help="Char embedding dimension"
)
optparser.add_option(
    "-C", "--char_lstm_dim", default="25",
    type='int', help="Char LSTM hidden layer size"
)
optparser.add_option(
    "-b", "--char_bidirect", default="1",
    type='int', help="Use a bidirectional LSTM for chars"
)
optparser.add_option(
    "-w", "--word_dim", default="100",
    type='int', help="Token embedding dimension"
)
optparser.add_option(
    "-W", "--word_lstm_dim", default="100",
    type='int', help="Token LSTM hidden layer size"
)
optparser.add_option(
    "-B", "--word_bidirect", default="1",
    type='int', help="Use a bidirectional LSTM for words"
)
optparser.add_option(
    "-p", "--pre_emb", default="",
    help="Location of pretrained embeddings"
)
optparser.add_option(
    "-A", "--all_emb", default="0",
    type='int', help="Load all embeddings"
)
optparser.add_option(
    "-a", "--cap_dim", default="0",
    type='int', help="Capitalization feature dimension (0 to disable)"
)
optparser.add_option(
    "-f", "--crf", default="1",
    type='int', help="Use CRF (0 to disable)"
)
optparser.add_option(
    "-D", "--dropout", default="0.5",
    type='float', help="Droupout on the input (0 = no dropout)"
)
optparser.add_option(
    "-L", "--lr_method", default="sgd-lr_.005",
    help="Learning method (SGD, Adadelta, Adam..)"
)
optparser.add_option(
    "-r", "--reload", default="0",
    type='int', help="Reload the last saved model"
)
optparser.add_option(
    "-F", "--freq", default="0.1",
    type='float', help="The freqency of evaluation: the larger the number, the less the system will evaluate the dev and test datasets (must be between 0 and 1)"
)
optparser.add_option(
    "-E", "--early_stop", default="5",
    type='int', help="Set early stop, after seted number of epchoes, if performance is not inproved, stop the training (default is 5)"
)
optparser.add_option(
    "-N", "--n_epoch", default="100",
    type='int', help="Total number of Epoches used for training if no early stop assigned (default is 100)"
)
optparser.add_option(
    "-S", "--force_save", default="0",
    type='int', help="force to save the model at the end of training (default is 0 as disabled)"
)

opts = optparser.parse_args()[0]

# Parse parameters
parameters = OrderedDict()
parameters['tag_scheme'] = opts.tag_scheme
parameters['lower'] = opts.lower == 1
parameters['zeros'] = opts.zeros == 1
parameters['char_dim'] = opts.char_dim
parameters['char_lstm_dim'] = opts.char_lstm_dim
parameters['char_bidirect'] = opts.char_bidirect == 1
parameters['word_dim'] = opts.word_dim
parameters['word_lstm_dim'] = opts.word_lstm_dim
parameters['word_bidirect'] = opts.word_bidirect == 1
parameters['pre_emb'] = opts.pre_emb
parameters['all_emb'] = opts.all_emb == 1
parameters['cap_dim'] = opts.cap_dim
parameters['crf'] = opts.crf == 1
parameters['dropout'] = opts.dropout
parameters['lr_method'] = opts.lr_method
parameters['freq'] = opts.freq
parameters['early_stop'] = opts.early_stop
parameters['n_epoch'] = opts.n_epoch
parameters['force_save'] = opts.force_save

# Check parameters validity
assert os.path.isfile(opts.train)
assert os.path.isfile(opts.dev)
assert os.path.isfile(opts.test)
assert parameters['char_dim'] > 0 or parameters['word_dim'] > 0
assert 0. <= parameters['dropout'] < 1.0
assert parameters['tag_scheme'] in ['iob', 'iobes']
assert not parameters['all_emb'] or parameters['pre_emb']
assert not parameters['pre_emb'] or parameters['word_dim'] > 0
assert not parameters['pre_emb'] or os.path.isfile(parameters['pre_emb'])

if not parameters['force_save']:
    parameters['force_save'] = 0
else:
    assert parameters['force_save'] > 0

if not parameters['n_epoch']:
    parameters['n_epoch'] = 100
else:
    assert parameters['n_epoch'] > 0

if not parameters['early_stop']:
    parameters['early_stop'] = 5
else:
    assert parameters['early_stop'] > 0

if not parameters['freq']:
    parameters['freq'] = 0.1
else:
    assert 0. < parameters['freq'] < 1.0

# Check evaluation script / folders
if not os.path.isfile(eval_script):
    raise Exception('CoNLL evaluation script not found at "%s"' % eval_script)
if not os.path.exists(eval_temp):
    os.makedirs(eval_temp)
if not os.path.exists(models_path):
    os.makedirs(models_path)

# Initialize model
model = Model(parameters=parameters, models_path=models_path)
print "Model location: %s" % model.model_path

# Data parameters
lower = parameters['lower']
zeros = parameters['zeros']
tag_scheme = parameters['tag_scheme']

# Load sentences
train_sentences = loader.load_sentences(opts.train, lower, zeros)
dev_sentences = loader.load_sentences(opts.dev, lower, zeros)
test_sentences = loader.load_sentences(opts.test, lower, zeros)

# Use selected tagging scheme (IOB / IOBES)
update_tag_scheme(train_sentences, tag_scheme)
update_tag_scheme(dev_sentences, tag_scheme)
update_tag_scheme(test_sentences, tag_scheme)

# Create a dictionary / mapping of words
# If we use pretrained embeddings, we add them to the dictionary.
if parameters['pre_emb']:
    dico_words_train = word_mapping(train_sentences, lower)[0]
    dico_words, word_to_id, id_to_word = augment_with_pretrained(
        dico_words_train.copy(),
        parameters['pre_emb'],
        list(itertools.chain.from_iterable(
            [[w[0] for w in s] for s in dev_sentences + test_sentences])
        ) if not parameters['all_emb'] else None
    )
else:
    dico_words, word_to_id, id_to_word = word_mapping(train_sentences, lower)
    dico_words_train = dico_words

# Create a dictionary and a mapping for words / POS tags / tags
dico_chars, char_to_id, id_to_char = char_mapping(train_sentences)
dico_tags, tag_to_id, id_to_tag = tag_mapping(train_sentences)

# Index data
train_data = prepare_dataset(
    train_sentences, word_to_id, char_to_id, tag_to_id, lower
)
dev_data = prepare_dataset(
    dev_sentences, word_to_id, char_to_id, tag_to_id, lower
)
test_data = prepare_dataset(
    test_sentences, word_to_id, char_to_id, tag_to_id, lower
)

print "%i / %i / %i sentences in train / dev / test." % (
    len(train_data), len(dev_data), len(test_data))

# Save the mappings to disk
print 'Saving the mappings to disk...'
model.save_mappings(id_to_word, id_to_char, id_to_tag)

# Build the model
f_train, f_eval = model.build(**parameters)

# Reload previous model values
if opts.reload:
    print 'Reloading previous model...'
    model.reload()

#
# Train network
#
singletons = set([word_to_id[k] for k, v
                  in dico_words_train.items() if v == 1])
n_epochs = parameters['n_epoch']  # number of epochs over the training set

#using freq parameter to determine freq_eval
freq_eval = int(parameters['freq']*len(train_data))
logger.info("evaluation freq: %i" % freq_eval)

#freq_eval = 1000  # evaluate on dev every freq_eval steps
best_dev = -np.inf
best_test = -np.inf
count = 0
mp = model.get_model_path()
auto_results_file = os.path.join(mp, 'results.txt')
stop_flag = parameters['early_stop']
with open(auto_results_file, "w") as f:
    f.write("The best restricted evaluation result: \n".encode("utf-8"))
for epoch in xrange(n_epochs):
    #early stop
    if not stop_flag:
        print "no performance improvement after %i epchoes, the system early stops the training" % parameters['early_stop']
        sys.exit(0)

    epoch_costs = []
    print "Starting epoch %i..." % epoch
    logger.info(len(np.random.permutation(len(train_data))))
    for i, index in enumerate(np.random.permutation(len(train_data))):
        count += 1
        input = create_input(train_data[index], parameters, True, singletons)
        new_cost = f_train(*input)
        epoch_costs.append(new_cost)
        if i % 50 == 0 and i > 0 == 0:
            print "%i, cost average: %f" % (i, np.mean(epoch_costs[-50:]))
        if count % freq_eval == 0:
            dev_score, dev_prf = evaluate(parameters, f_eval, dev_sentences,
                                 dev_data, id_to_tag, dico_tags)
            # test_score, test_prf = evaluate(parameters, f_eval, test_sentences,
            #                       test_data, id_to_tag, dico_tags)
            print "Score on dev: %.2f" % dev_score
            # print "Score on test: %.2f" % test_score
            if dev_score > best_dev:
                best_dev = dev_score
                print "New best score on dev."
                print "Saving model to disk..."
                model.save()
                stop_flag = parameters['early_stop']
            # if test_score > best_test:
            #     best_test = test_score
            #     print "New best score on test."
                with open(auto_results_file, "a") as f:
                    f.write(("Epoch: %i step: %i" % (epoch, count) + dev_prf + "\n").encode("utf-8"))

    print "Epoch %i done. Average cost: %f" % (epoch, np.mean(epoch_costs))
    with open(auto_results_file, "a") as f:
        f.write(("Epoch: %i; avg cost: %f" % (epoch, np.mean(epoch_costs)) + "\n").encode("utf-8"))
    stop_flag -= 1

if parameters['force_save']:
    model.save()




