#!/usr/bin/env python3

"""
Generate quantized array from quantized table.
Author: laqieer
Email: laqieer@126.com
"""

quantized_table = [0, 1, 4, 9, 16, 25, 36, 49, -64, -49, -36, -25, -16, -9, -4, -1]
quantized_array = []

for d in range(-255, 256):
    quantized_value = 0
    if d >= max(quantized_table):
        quantized_value = quantized_table.index(max(quantized_table))
    elif d <= min(quantized_table):
        quantized_value = quantized_table.index(min(quantized_table))
    else:
        for i in range(len(quantized_table)):
            if i == len(quantized_table) - 1:
                if d >= quantized_table[i] and d < quantized_table[0]:
                    if d - quantized_table[i] > quantized_table[0] - d:
                        quantized_value = 0
                    else:
                        quantized_value = i
                    break
            elif d >= quantized_table[i] and d < quantized_table[i + 1]:
                if d - quantized_table[i] > quantized_table[i + 1] - d:
                    quantized_value = i + 1
                else:
                    quantized_value = i
                break
    quantized_array.append(quantized_value)

print(quantized_array)
