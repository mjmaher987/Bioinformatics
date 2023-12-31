# -*- coding: utf-8 -*-
"""ACTG Ratio Problem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gs068BZXHGFCbPh8Ve_9p2my5gJ3hARw
"""

class DNA:
  def __init__(self, id):
    self.id = id
    self.count = 0
    self.all = 0

all_genes = list()
last_gene = None
import os
os.chdir('c:/Users/mjmah/OneDrive/Desktop/everything/Main/term7/bio/HWs/HW1/q1')


with open('rosalind_gc-q1.txt', 'r') as file:
    for line in file:
        if line.startswith('>'):
          id = line[10:]
          last_gene = DNA(id)
          all_genes.append(last_gene)
        else:
          last_gene.count += line.count('C') + line.count('G')
          last_gene.all += line.count('C') + line.count('G') + line.count('A') + line.count('T')

max_v = 0.0
max_id = ""
for gene in all_genes:
  ratio = gene.count / gene.all
  if ratio > max_v:
    max_v = ratio
    max_id = gene.id

print("Rosalind_" + max_id, end='')
print("{:.5f}".format(max_v * 100))