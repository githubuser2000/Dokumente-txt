#!/usr/bin/env python3

import sys
import csv
import shutil
from textwrap import wrap

def get_terminal_width():
    return shutil.get_terminal_size((80, 20)).columns

def read_column(file_path, col_index):
    col = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if col_index < len(row):
                col.append(row[col_index])
            else:
                col.append('')
    return col

def wrap_lines(text, width):
    return wrap(text, width=width) or ['']

if len(sys.argv) != 5:
    print(f"Usage: {sys.argv[0]} file1.csv file2.csv col1 col2")
    sys.exit(1)

file1, file2 = sys.argv[1], sys.argv[2]
col1_index, col2_index = int(sys.argv[3]), int(sys.argv[4])

col1 = read_column(file1, col1_index)
col2 = read_column(file2, col2_index)

# gleiche Länge
size = max(len(col1), len(col2))
col1 += [''] * (size - len(col1))
col2 += [''] * (size - len(col2))

# Terminalbreite
term_width = get_terminal_width()

width_num = 4  # Zeilennummer immer 4-stellig
width1 = max(len(s) for s in col1)
width2 = max(len(s) for s in col2)

# Falls Spaltenbreite zu groß für Terminal, proportional skalieren
if width_num + 3 + width1 + 3 + width2 > term_width:
    ratio = (term_width - 6) / (width_num + width1 + width2)
    width1 = max(1, int(width1 * ratio))
    width2 = max(1, int(width2 * ratio))

for i in range(size):
    # Zeilennummer
    if i + 1 == 0:
        num_str = ' ' * 4
    else:
        num_str = f"{i+1:04d}"

    lines_num = wrap_lines(num_str, width_num)
    lines1 = wrap_lines(col1[i], width1)
    lines2 = wrap_lines(col2[i], width2)

    max_lines = max(len(lines_num), len(lines1), len(lines2))
    lines_num += [''] * (max_lines - len(lines_num))
    lines1 += [''] * (max_lines - len(lines1))
    lines2 += [''] * (max_lines - len(lines2))

    for j in range(max_lines):
        print(f"{lines_num[j]:<4} | {lines1[j]:<{width1}} | {lines2[j]:<{width2}}")

