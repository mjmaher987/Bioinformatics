



import os
os.chdir('c:/Users/mjmah/OneDrive/Desktop/everything/Main/term7/bio/HWs/HW1/q7')


class DNA:
  def __init__(self):
    self.string = ""
  def add_neucleotide(self, to_add):
    self.string += to_add



import numpy as np
all_DNAs = []
last_dna = None
with open('rosalind_edta.txt', 'r') as file:
  for dna in file:
    dna = dna.strip()
    if dna.startswith('>'):
      last_dna = DNA()
      all_DNAs.append(last_dna)
    else:
      last_dna.add_neucleotide(dna)


all_DNAs[0].string.replace('\n', '')
all_DNAs[1].string.replace('\n', '')

def edit_Distance(first, second):
    m, n = len(first), len(second)

    matrix = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        matrix[i][0] = i
    for j in range(n + 1):
        matrix[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if first[i - 1] == second[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)

    first_dna_aligned, second_dna_aligned = "", ""
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and matrix[i][j] == matrix[i - 1][j] + 1:
            first_dna_aligned = first[i - 1] + first_dna_aligned
            second_dna_aligned = "-" + second_dna_aligned
            i -= 1
        elif j > 0 and matrix[i][j] == matrix[i][j - 1] + 1:
            first_dna_aligned = "-" + first_dna_aligned
            second_dna_aligned = second[j - 1] + second_dna_aligned
            j -= 1
        else:
            first_dna_aligned = first[i - 1] + first_dna_aligned
            second_dna_aligned = second[j - 1] + second_dna_aligned
            i -= 1
            j -= 1

    edit_distance = matrix[m][n]

    return edit_distance, first_dna_aligned, second_dna_aligned

# print(all_DNAs[0].string)

distance, first_dna_aligned, second_dna_aligned = edit_Distance(all_DNAs[0].string, all_DNAs[1].string)


print(distance)
print(first_dna_aligned)
print(second_dna_aligned)