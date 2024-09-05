#!/usr/bin/env python
#coding=gbk

import pandas as pd


csv_file_path = '../data/test.csv'
  

fasta_ref_path = 'test_ref-seq.fasta'
fasta_alt_path = 'test_alt-seq.fasta'
  

df = pd.read_csv(csv_file_path)
  

# 保存REF_seq到文件（无FASTA标识符）  
with open(fasta_ref_path, 'w') as f_ref:  
    for _, row in df.iterrows():  # 使用_来忽略行索引  
        f_ref.write(f'{row["REF_seq"]}\n')
  

# 保存ALT_seq到文件（无FASTA标识符）  
with open(fasta_alt_path, 'w') as f_alt:  
    for _, row in df.iterrows(): 
        f_alt.write(f'{row["ALT_seq"]}\n')