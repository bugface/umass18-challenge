# umass2017
# MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda0 python train.py -T umass2017/umass_ntrain_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -z 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.01 -F 0.1 -E 10
# MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda1 python train.py -T umass2017/umass_ntrain_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -z 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.001 -F 0.1 -E 10
# MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass_ntrain_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -z 1 -c 25 -C 50 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.005 -F 0.1 -E 10
# MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda1 python train.py -T umass2017/umass_ntrain_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -z 1 -c 25 -C 25 -b 1 -w 200 -W 300 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.005 -F 0.1 -E 10
# MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass_ntrain_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -z 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.005 -F 0.01 -E 10

#using combined data set
#MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda1 python train.py -T umass2017/umass_ncmb_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -z 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.005 -F 0.1 -E 10 -S 1 -N 32

#using new data with DOCSTART
#based on best testing performance
#MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass_ntrain_modified.txt -d umass2017/umass_ntest.bio.txt -t umass2017/umass_ntest.bio.txt -l 1 -z 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.01 -F 0.1 -E 10

#not relace digits with 0
#MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass_ntrain_modified.txt -d umass2017/umass_ntest.bio.txt -t umass2017/umass_ntest.bio.txt -l 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.01 -F 0.1 -E 10

#not relace digits with 0, no lower case
#MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass_ntrain_modified.txt -d umass2017/umass_ntest.bio.txt -t umass2017/umass_ntest.bio.txt -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.01 -F 0.1 -E 10

#using 32 epoches
#MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass18.bio.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -z 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.01 -F 0.5 -E 30 -S 1 -N 33

#try to get the best model
MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass_ntrain_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -z 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.005 -F 0.1 -E 15
MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass_ntrain_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -z 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.005 -F 0.1 -E 15
MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass_ntrain_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.005 -F 0.1 -E 10
MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass_ntrain_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.005 -F 0.1 -E 10
MKL_THREADING_LAYER=GNU THEANO_FLAGS=device=cuda2 python train.py -T umass2017/umass_ntrain_plain.txt -d umass2017/umass_ntest_plain.txt -t umass2017/umass_ntest_plain.txt -l 1 -z 1 -c 25 -C 25 -b 1 -w 200 -W 200 -B 1 -p umass2017/umass_emb.txt -f 1 -D 0.5 -s iob -L sgd-lr_.001 -F 0.1 -E 15d