#!/usr/bin/env python
#coding=gbk

import os
import h5py
import numpy as np
import pandas as pd
import argparse

import sys
sys.path.append('../')
from models.DanQ import DanQ

SEQ_LENGTH = 1000      # sequence length accepted by DanQ model

# to one-hot encode sequence features according to DanQ's input
def one_hot(x):
    arr = np.array(list(x))
    a = (arr == 'A')
    g = (arr == 'G')
    c = (arr == 'C')
    t = (arr == 'T')

    return np.vstack([a, g, c, t]).T

# read and format sequence
def get_sequence(filename):
    with open(filename, 'r') as f:
        seq = f.read()
        
    seq = seq.split('\n')[0:]
    seq = list(map(one_hot, seq))
    seq = np.array(seq).astype('uint8')
    return seq

# get 919 features from DanQ model
def prepare_sequence(model, args, type='ref'):
    dataset_filename = os.path.join(args.path, f'Testing1_Label_700pos_486neg_start-lost_hg38_1001bp_kmer_random_{type}-seq.fasta')
    
    dataset_seq = get_sequence(dataset_filename)

    seq = np.array(dataset_seq)[:, :SEQ_LENGTH]

    return model.predict(seq)
    
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Arguments for preparing features.'
    )
    parser.add_argument(
        '--path', default='./', type=str, help='path for input data'
    )
    args = parser.parse_args()


    # prepare input features
    danQ = DanQ(name='DanQ')

    print('Process ref:')    
    ref = prepare_sequence(danQ, args, type='ref')
    
    print('Process alt:')
    alt = prepare_sequence(danQ, args, type='alt')


    # save everything in one h5 file
    file_path = os.path.join(args.path, 'test.h5')
    hf = h5py.File(file_path, 'w')
    hf.create_dataset('feat_ref', data=ref)
    hf.create_dataset('feat_alt', data=alt)
    hf.close()
