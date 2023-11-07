# -*- coding: utf-8 -*-
"""Local Alignment with Scoring Matrix.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PNgDzDvea70MNeO4kw98JJdEZw09ug7q
"""

PAM250 = [  # Substitution penalty PAM250
	[  2,  -2,   0,   0,  -3,   1,  -1,  -1,  -1,  -2,  -1,   0,   1,   0,  -2,   1,   1,   0,  -6,  -3],
	[ -2,  12,  -5,  -5,  -4,  -3,  -3,  -2,  -5,  -6,  -5,  -4,  -3,  -5,  -4,   0,  -2,  -2,  -8,   0],
	[  0,  -5,   4,   3,  -6,   1,   1,  -2,   0,  -4,  -3,   2,  -1,   2,  -1,   0,   0,  -2,  -7,  -4],
	[  0,  -5,   3,   4,  -5,   0,   1,  -2,   0,  -3,  -2,   1,  -1,   2,  -1,   0,   0,  -2,  -7,  -4],
	[ -3,  -4,  -6,  -5,   9,  -5,  -2,   1,  -5,   2,   0,  -3,  -5,  -5,  -4,  -3,  -3,  -1,   0,   7],
	[  1,  -3,   1,   0,  -5,   5,  -2,  -3,  -2,  -4,  -3,   0,   0,  -1,  -3,   1,   0,  -1,  -7,  -5],
	[ -1,  -3,   1,   1,  -2,  -2,   6,  -2,   0,  -2,  -2,   2,   0,   3,   2,  -1,  -1,  -2,  -3,   0],
	[ -1,  -2,  -2,  -2,   1,  -3,  -2,   5,  -2,   2,   2,  -2,  -2,  -2,  -2,  -1,   0,   4,  -5,  -1],
	[ -1,  -5,   0,   0,  -5,  -2,   0,  -2,   5,  -3,   0,   1,  -1,   1,   3,   0,   0,  -2,  -3,  -4],
	[ -2,  -6,  -4,  -3,   2,  -4,  -2,   2,  -3,   6,   4,  -3,  -3,  -2,  -3,  -3,  -2,   2,  -2,  -1],
	[ -1,  -5,  -3,  -2,   0,  -3,  -2,   2,   0,   4,   6,  -2,  -2,  -1,   0,  -2,  -1,   2,  -4,  -2],
	[  0,  -4,   2,   1,  -3,   0,   2,  -2,   1,  -3,  -2,   2,   0,   1,   0,   1,   0,  -2,  -4,  -2],
	[  1,  -3,  -1,  -1,  -5,   0,   0,  -2,  -1,  -3,  -2,   0,   6,   0,   0,   1,   0,  -1,  -6,  -5],
	[  0,  -5,   2,   2,  -5,  -1,   3,  -2,   1,  -2,  -1,   1,   0,   4,   1,  -1,  -1,  -2,  -5,  -4],
	[ -2,  -4,  -1,  -1,  -4,  -3,   2,  -2,   3,  -3,   0,   0,   0,   1,   6,   0,  -1,  -2,   2,  -4],
	[  1,   0,   0,   0,  -3,   1,  -1,  -1,   0,  -3,  -2,   1,   1,  -1,   0,   2,   1,  -1,  -2,  -3],
	[  1,  -2,   0,   0,  -3,   0,  -1,   0,   0,  -2,  -1,   0,   0,  -1,  -1,   1,   3,   0,  -5,  -3],
	[  0,  -2,  -2,  -2,  -1,  -1,  -2,   4,  -2,   2,   2,  -2,  -1,  -2,  -2,  -1,   0,   4,  -6,  -2],
	[ -6,  -8,  -7,  -7,   0,  -7,  -3,  -5,  -3,  -2,  -4,  -4,  -6,  -5,   2,  -2,  -5,  -6,  17,   0],
	[ -3,   0,  -4,  -4,   7,  -5,   0,  -1,  -4,  -1,  -2,  -2,  -5,  -4,  -4,  -3,  -3,  -2,   0,  10]
]
PAM250_ENTRIES = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N',
	'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
PAM250_MAP = dict(zip(PAM250_ENTRIES, range(len(PAM250_ENTRIES))))

import numpy as np

all_DNAs = []
last_dna = None

class DNA:
  def __init__(self):
    self.string = ""
  def add_neucleotide(self, to_add):
    self.string += to_add


with open('rosalind_loca.txt', 'r') as file:
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

score_mat = PAM250
score_mat_map = PAM250_MAP
mode = 'max'
func = {'max': max, 'min': min}[mode]
sign = {'max': -1, 'min': 1}[mode]  # When maximizing, negative is for punishment
comp_op = {'max': lambda x, y: x > y, 'min': lambda x, y: x < y}[mode]
# g(k) := alpha + beta * k
# alpha = sign * 11  # Gap initial penalty.
# beta = sign * 1  # Gap continuation penalty.
gamma = sign * 5  # Gap penalty.

D = [[None for _ in range(len(a)+1)] for _ in range(len(b)+1)]
for i in range(len(b)+1):
	D[i][0] = 0
for j in range(len(a)+1):
	D[0][j] = 0

best_val = sign * sys.maxsize
best_i, best_j = None, None
for i in range(1, len(b)+1):
	for j in range(1, len(a)+1):
		match_val = score_mat[score_mat_map[a[j-1]]][score_mat_map[b[i-1]]]
		D[i][j] = func(0, D[i-1][j-1]+match_val, D[i-1][j]+gamma, D[i][j-1]+gamma)
		if comp_op(D[i][j], best_val):
			best_val = D[i][j]
			best_i, best_j = i, j

print(best_val)

a_alig = []
b_alig = []
cur_i, cur_j = best_i, best_j
while comp_op(D[cur_i][cur_j], 0):
	match_val = score_mat[score_mat_map[a[cur_j-1]]][score_mat_map[b[cur_i-1]]]
	if D[cur_i][cur_j] == D[cur_i-1][cur_j-1] + match_val:
		a_alig.append(a[cur_j-1])
		b_alig.append(b[cur_i-1])
		cur_i -= 1
		cur_j -= 1
	elif D[cur_i][cur_j] == D[cur_i-1][cur_j] + gamma:
		b_alig.append(b[cur_i-1])
		cur_i -= 1
	elif D[cur_i][cur_j] == D[cur_i][cur_j-1] + gamma:
		a_alig.append(a[cur_j-1])
		cur_j -= 1
	else:
		raise Exception()

print(''.join(a_alig[::-1]))
print(''.join(b_alig[::-1]))