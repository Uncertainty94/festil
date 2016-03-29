# -*- coding: utf-8 -*-
# 	bin(( 230 << 3 | 230 >> 5) % 256)
key = int('0b1001011010100010011001100010111010010110111110100011011000101111', 2)


def get_new_key(step):
    return circle(key, step*3, 64) / 2**32


def func(part):
    left = part / 2**16
    right = part % 2**16
    left ^= (2**16 - 1)
    right = circle(right, -11, 16)
    full = bin(left)+bin(right)[2:]
    return int(full, 2)
    # return part ^ 2**32-1


def circle(row, num, bit_count):
    if num > 0:
        return (row << num | row >> (bit_count-num)) % 2**bit_count
    num = -num
    return (row >> num | row << (bit_count-num)) % 2**bit_count


def get_bin_code(symb):
    code = bin(ord(symb))
    code = code[2:len(code)]
    return "0" * (8 - len(code)) + code


def get_str_from_num(num):
    result = []
    for i in range(0, 4):
        result.append(chr(num % 2**8))
        num /= 2**8
    result = result[::-1]
    return ''.join(result)


def get_list_blocks(row):
    result = []
    length = len(row)
    to_end = (8 - length % 8) % 8
    row += to_end * chr(0)
    for i in range(0, len(row), 8):
        result.append(row[i:i + 8])
    return result


def work_with_a_block(part):
    print '~~~~~~~~~~~~~~~~~~~Work with block~~~~~~~~~~~~~~~~~~~~'
    parts = [part[0:len(part) / 2], part[len(part) / 2:len(part)]]
    print parts
    bin_left = ''
    bin_right = ''

    for char in parts[0]:
        bin_left += get_bin_code(char)

    for char in parts[1]:
        bin_right += get_bin_code(char)

    print bin_left, '---', bin_right

    left = int('0b'+bin_left, 2)
    right = int('0b'+bin_right, 2)

    for i in range(1, 17):
        new_right = left ^ get_new_key(i)
        new_left = func(new_right) ^ right
        left = new_left
        right = new_right

    print bin(left), '---', bin(right)
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    return get_str_from_num(left)+get_str_from_num(right)


def work_with_a_block_inverse(part):
    print '~~~~~~~~~~~~~~~~~~~Work with block inverse~~~~~~~~~~~~~~~~~~~~'
    parts = [part[0:len(part) / 2], part[len(part) / 2:len(part)]]
    print parts
    bin_left = ''
    bin_right = ''

    for char in parts[0]:
        bin_left += get_bin_code(char)

    for char in parts[1]:
        bin_right += get_bin_code(char)

    print bin_left, '---', bin_right

    left = int('0b'+bin_left, 2)
    right = int('0b'+bin_right, 2)

    for i in range(16, 0, -1):
        new_left = right ^ get_new_key(i)
        new_right = func(right) ^ left
        left = new_left
        right = new_right

    print bin(left), '---', bin(right)
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    return get_str_from_num(left)+get_str_from_num(right)


input_file = open("input.txt", "r")
output_file = open("encrypted.txt", "w")

line = input_file.read()
blocks = get_list_blocks(line)
print blocks
outstr = ''
for block in blocks:
    outstr = work_with_a_block(block)
    output_file.write(outstr)

input_file.close()
output_file.close()

input_file = open("encrypted.txt", "r")
output_file = open("decrypted.txt", "w")

line = input_file.read()
blocks2 = get_list_blocks(line)
print blocks2
outstr2 = ''
for block in blocks2:
    outstr2 = work_with_a_block_inverse(block)
    output_file.write(outstr2)

input_file.close()
output_file.close()
