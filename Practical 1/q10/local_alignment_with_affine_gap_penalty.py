# -*- coding: utf-8 -*-
"""Local Alignment with Affine Gap Penalty.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A9KvcqZZ_P0ukBCpniGHGGQCt9Dx73re
"""

# MJ Maheronnaghsh
BLOSUM62 = [
	[  4,   0,  -2,  -1,  -2,   0,  -2,  -1,  -1,  -1,  -1,  -2,  -1,  -1,  -1,   1,   0,   0,  -3,  -2],
	[  0,   9,  -3,  -4,  -2,  -3,  -3,  -1,  -3,  -1,  -1,  -3,  -3,  -3,  -3,  -1,  -1,  -1,  -2,  -2],
	[ -2,  -3,   6,   2,  -3,  -1,  -1,  -3,  -1,  -4,  -3,   1,  -1,   0,  -2,   0,  -1,  -3,  -4,  -3],
	[ -1,  -4,   2,   5,  -3,  -2,   0,  -3,   1,  -3,  -2,   0,  -1,   2,   0,   0,  -1,  -2,  -3,  -2],
	[ -2,  -2,  -3,  -3,   6,  -3,  -1,   0,  -3,   0,   0,  -3,  -4,  -3,  -3,  -2,  -2,  -1,   1,   3],
	[  0,  -3,  -1,  -2,  -3,   6,  -2,  -4,  -2,  -4,  -3,   0,  -2,  -2,  -2,   0,  -2,  -3,  -2,  -3],
	[ -2,  -3,  -1,   0,  -1,  -2,   8,  -3,  -1,  -3,  -2,   1,  -2,   0,   0,  -1,  -2,  -3,  -2,   2],
	[ -1,  -1,  -3,  -3,   0,  -4,  -3,   4,  -3,   2,   1,  -3,  -3,  -3,  -3,  -2,  -1,   3,  -3,  -1],
	[ -1,  -3,  -1,   1,  -3,  -2,  -1,  -3,   5,  -2,  -1,   0,  -1,   1,   2,   0,  -1,  -2,  -3,  -2],
	[ -1,  -1,  -4,  -3,   0,  -4,  -3,   2,  -2,   4,   2,  -3,  -3,  -2,  -2,  -2,  -1,   1,  -2,  -1],
	[ -1,  -1,  -3,  -2,   0,  -3,  -2,   1,  -1,   2,   5,  -2,  -2,   0,  -1,  -1,  -1,   1,  -1,  -1],
	[ -2,  -3,   1,   0,  -3,   0,   1,  -3,   0,  -3,  -2,   6,  -2,   0,   0,   1,   0,  -3,  -4,  -2],
	[ -1,  -3,  -1,  -1,  -4,  -2,  -2,  -3,  -1,  -3,  -2,  -2,   7,  -1,  -2,  -1,  -1,  -2,  -4,  -3],
	[ -1,  -3,   0,   2,  -3,  -2,   0,  -3,   1,  -2,   0,   0,  -1,   5,   1,   0,  -1,  -2,  -2,  -1],
	[ -1,  -3,  -2,   0,  -3,  -2,   0,  -3,   2,  -2,  -1,   0,  -2,   1,   5,  -1,  -1,  -3,  -3,  -2],
	[  1,  -1,   0,   0,  -2,   0,  -1,  -2,   0,  -2,  -1,   1,  -1,   0,  -1,   4,   1,  -2,  -3,  -2],
	[  0,  -1,  -1,  -1,  -2,  -2,  -2,  -1,  -1,  -1,  -1,   0,  -1,  -1,  -1,   1,   5,   0,  -2,  -2],
	[  0,  -1,  -3,  -2,  -1,  -3,  -3,   3,  -2,   1,   1,  -3,  -2,  -2,  -3,  -2,   0,   4,  -3,  -1],
	[ -3,  -2,  -4,  -3,   1,  -2,  -2,  -3,  -3,  -2,  -1,  -4,  -4,  -2,  -3,  -3,  -2,  -3,  11,   2],
	[ -2,  -2,  -3,  -2,   3,  -3,   2,  -1,  -2,  -1,  -1,  -2,  -3,  -1,  -2,  -2,  -2,  -1,   2,   7]
]
BLOSUM62_ENTRIES = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
BLOSUM62_MAP = dict(zip(BLOSUM62_ENTRIES, range(len(BLOSUM62_ENTRIES))))

class DNA:
  def __init__(self):
    self.string = ""
  def add_neucleotide(self, to_add):
    self.string += to_add

import numpy as np
all_DNAs = []
last_dna = None
with open('rosalind_loca-2.txt', 'r') as file:
  for dna in file:
    dna = dna.strip()
    if dna.startswith('>'):
      last_dna = DNA()
      all_DNAs.append(last_dna)
    else:
      last_dna.add_neucleotide(dna)


all_DNAs[0].string.replace('\n', '')
all_DNAs[1].string.replace('\n', '')

a = all_DNAs[0].string
b = all_DNAs[1].string
GAP_OPENING_PENALTY = -1 * 11
GAP_EXTENTION_PENALTY = -1 * 1

D = [[None for j in range(len(a)+1)] for i in range(len(b)+1)]
P = [[None for j in range(len(a)+1)] for i in range(len(b)+1)]
Q = [[None for j in range(len(a)+1)] for i in range(len(b)+1)]
for i in range(len(b)+1):
	D[i][0] = 0
	Q[i][0] = -1 * 100000
for j in range(len(a)+1):
	D[0][j] = 0
	P[0][j] = -1 * 100000
P[0][0], Q[0][0] = 0, 0

best_val = -1 * 100000
best_i, best_j = None, None
for i in range(1, len(b)+1):
	for j in range(1, len(a)+1):
		P[i][j] = max(D[i-1][j] + GAP_OPENING_PENALTY, P[i-1][j] + GAP_EXTENTION_PENALTY)
		Q[i][j] = max(D[i][j-1] + GAP_OPENING_PENALTY, Q[i][j-1] + GAP_EXTENTION_PENALTY)
		match_score = D[i-1][j-1] + BLOSUM62[BLOSUM62_MAP[a[j-1]]][BLOSUM62_MAP[b[i-1]]]
		D[i][j] = max(0, match_score, P[i][j], Q[i][j])
		if D[i][j] > best_val:
			best_val = D[i][j]
			best_i, best_j = i, j

print(best_val)

a_alig = []
b_alig = []
cur_i, cur_j = best_i, best_j
cur_mat = 'D'
while D[cur_i][cur_j] > 0:
	if cur_mat == 'D':
		match_score = D[cur_i-1][cur_j-1] + BLOSUM62[BLOSUM62_MAP[a[cur_j-1]]][BLOSUM62_MAP[b[cur_i-1]]]
		if D[cur_i][cur_j] ==  match_score:
			a_alig.append(a[cur_j-1])
			b_alig.append(b[cur_i-1])
			cur_i -= 1
			cur_j -= 1
		elif D[cur_i][cur_j] == P[cur_i][cur_j]:
			cur_mat = 'P'
		elif D[cur_i][cur_j] == Q[cur_i][cur_j]:
			cur_mat = 'Q'
		else:
			raise Exception()
	elif cur_mat == 'P':
		if P[cur_i][cur_j] != P[cur_i-1][cur_j] + GAP_EXTENTION_PENALTY:
			cur_mat = 'D'
		b_alig.append(b[cur_i-1])
		cur_i -= 1
	elif cur_mat == 'Q':
		if Q[cur_i][cur_j] != Q[cur_i][cur_j-1] + GAP_EXTENTION_PENALTY:
			cur_mat = 'D'
		a_alig.append(a[cur_j-1])
		cur_j -= 1
	else:
		raise Exception()

print(''.join(a_alig[::-1]))
print(''.join(b_alig[::-1]))