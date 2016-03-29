# -*- coding: utf-8 -*-
key = int('0b1001011010100010011001100010111010010110111110100011011000101111', 2)


# Returned new key32 from key64, by cyclic shift for triple steps.
def get_new_key(step):
    return circle(key, step*3, 64) / 2**32


# Function specific to option 1.
def func(part):
    left = part / 2**16
    right = part % 2**16
    left ^= (2**16 - 1)
    right = circle(right, -11, 16)
    full = bin(left)+bin(right)[2:]
    return int(full, 2)


# Method to make cyclic shift.
# num > 0 - circle left, num < 0 - circle right.
# bit_count - the number of bits of the original string.
def circle(row, num, bit_count):
    if num > 0:
        return (row << num | row >> (bit_count-num)) % 2**bit_count
    num = -num
    return (row >> num | row << (bit_count-num)) % 2**bit_count


# Returns string of bin code. Adds '0' before the code to complete it to full byte.
def get_bin_code(symb):
    code = bin(ord(symb))
    code = code[2:len(code)]
    return "0" * (8 - len(code)) + code


# Returns string from binaries32.
def get_str_from_num(num):
    result = []
    for i in range(0, 4):
        result.append(chr(num % 2**8))
        num /= 2**8
    result = result[::-1]
    return ''.join(result)


# Returns list of blocks of 4 chars (=== 32 bits). Adds '0' at the end of row to complete it to full bytes.
def get_list_blocks(row):
    result = []
    length = len(row)
    to_end = (8 - length % 8) % 8
    row += to_end * chr(0)
    for i in range(0, len(row), 8):
        result.append(row[i:i + 8])
    return result


# Encrypting one block.
# Returns string of 4 encrypted chars (=== 32bits).
def encrypting_block(part):
    parts = [part[0:len(part) / 2], part[len(part) / 2:len(part)]]
    # print parts
    bin_left = ''
    bin_right = ''

    for char in parts[0]:
        bin_left += get_bin_code(char)

    for char in parts[1]:
        bin_right += get_bin_code(char)

    # print bin_left, '---', bin_right
    left = int('0b'+bin_left, 2)
    right = int('0b'+bin_right, 2)

    for i in range(1, 17):
        new_right = left ^ get_new_key(i)
        new_left = func(new_right) ^ right
        left = new_left
        right = new_right

    # print bin(left), '---', bin(right)
    return get_str_from_num(left)+get_str_from_num(right)


# Decrypting one block.
# Returns string of 4 decrypted chars (=== 32bits).
def decrypting_block(part):
    parts = [part[0:len(part) / 2], part[len(part) / 2:len(part)]]
    # print parts
    bin_left = ''
    bin_right = ''

    for char in parts[0]:
        bin_left += get_bin_code(char)

    for char in parts[1]:
        bin_right += get_bin_code(char)

    # print bin_left, '---', bin_right
    left = int('0b'+bin_left, 2)
    right = int('0b'+bin_right, 2)

    for i in range(16, 0, -1):
        new_left = right ^ get_new_key(i)
        new_right = func(right) ^ left
        left = new_left
        right = new_right

    # print bin(left), '---', bin(right)
    return get_str_from_num(left)+get_str_from_num(right)


# Start of encrypting.
def encrypt():
    # Init files to encrypt.
    input_file_to_encrypting = open("input.txt", "r")
    output_file_to_encrypting = open("encrypted.txt", "w")

    original_text = input_file_to_encrypting.read()
    original_blocks = get_list_blocks(original_text)

    # String of encrypted block. Needs to CBC.
    encrypted_block = ''
    for block in original_blocks:
        encrypted_block = encrypting_block(block)
        output_file_to_encrypting.write(encrypted_block)

    # Close files.
    input_file_to_encrypting.close()
    output_file_to_encrypting.close()


# Start of decrypting.
def decrypt():
    # Init files to decrypt.
    input_file_to_decrypting = open("encrypted.txt", "r")
    output_file_to_decrypting = open("decrypted.txt", "w")

    encrypted_text = input_file_to_decrypting.read()
    encrypted_blocks = get_list_blocks(encrypted_text)

    # String of decrypted block. Needs to CBC.
    decrypted_block = ''
    for block in encrypted_blocks:
        decrypted_block = decrypting_block(block)
        output_file_to_decrypting.write(decrypted_block)

    # Close files.
    input_file_to_decrypting.close()
    output_file_to_decrypting.close()


encrypt()

decrypt()