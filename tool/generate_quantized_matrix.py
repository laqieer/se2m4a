#!/usr/bin/env python3

"""
Generate quantized matrix from quantized table.
Author: laqieer
Email: laqieer@126.com
"""

quantized_table = [0, 1, 4, 9, 16, 25, 36, 49, -64, -49, -36, -25, -16, -9, -4, -1]
quantized_matrix = []

for d in range(-255, 256):
    quantized_value = 0
    if d == 0:
        quantized_matrix.append([0, 1, 15])
    elif d == -1:
        quantized_matrix.append([0, 15])
    elif d >= max(quantized_table):
        quantized_matrix.append([quantized_table.index(max(quantized_table))])
    elif d <= min(quantized_table):
        quantized_matrix.append([quantized_table.index(min(quantized_table))])
    else:
        for i in range(len(quantized_table)):
            if d == quantized_table[i]:
                if d > 0:
                    quantized_matrix.append([i, i - 1])
                else:
                    quantized_matrix.append([i, i + 1])
                break
            elif d > quantized_table[i] and d < quantized_table[i + 1]:
                quantized_matrix.append([i, i + 1])
                break

print(quantized_matrix)
