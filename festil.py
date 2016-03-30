# -*- coding: utf-8 -*-
# Random key64 to generate key32.
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


# Returns string of bin code of one char. Adds '0' before the code to complete it to full byte.
def get_bin_code_of_char(symb):
    code = bin(ord(symb))
    code = code[2:]
    return "0" * (8 - len(code)) + code


# Returns int equivalent of bin code of a string.
def get_bin_code_of_string(string):
    bin_form = ''
    for char in string:
        bin_form += get_bin_code_of_char(char)
    return int('0b'+bin_form, 2)


# Returns string from binaries32.
def get_str_from_num_32(num):
    result = []
    for i in range(0, 4):
        result.append(chr(num % 2**8))
        num /= 2**8
    result = result[::-1]
    return ''.join(result)


# Returns string from binaries64.
def get_str_from_num_64(num):
    result = []
    for i in range(0, 8):
        result.append(chr(num % 2**8))
        num /= 2**8
    result = result[::-1]
    return ''.join(result)


# Returns list of blocks of 8 chars (=== 64 bits). Adds '0' at the end of row to complete it to full bytes.
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
def encrypting_block(current_block):
    code_for_encrypting = get_bin_code_of_string(current_block)

    left = code_for_encrypting / 2**32
    right = code_for_encrypting % 2**32

    for i in range(1, 17):
        new_right = left ^ get_new_key(i)
        new_left = func(new_right) ^ right
        left = new_left
        right = new_right

    return get_str_from_num_32(left) + get_str_from_num_32(right)


# Decrypting one block.
# Returns string of 4 decrypted chars (=== 32bits).
def decrypting_block(current_block):
    current_code = get_bin_code_of_string(current_block)

    left = current_code / 2**32
    right = current_code % 2**32
    for i in range(16, 0, -1):
        new_left = right ^ get_new_key(i)
        new_right = func(right) ^ left
        left = new_left
        right = new_right

    return get_str_from_num_32(left) + get_str_from_num_32(right)


# Encrypting one block with CBC.
# Returns string of 4 encrypted chars (=== 32bits).
def encrypting_block_with_cbc(current_block, previous_block):
    previous_code = get_bin_code_of_string(previous_block)
    current_code = get_bin_code_of_string(current_block)

    code_for_encrypting = previous_code ^ current_code
    left = code_for_encrypting / 2**32
    right = code_for_encrypting % 2**32

    for i in range(1, 17):
        new_right = left ^ get_new_key(i)
        new_left = func(new_right) ^ right
        left = new_left
        right = new_right

    return get_str_from_num_32(left) + get_str_from_num_32(right)


# Decrypting one block with CBC.
# Returns string of 4 decrypted chars (=== 32bits).
def decrypting_block_with_cbc(current_block, previous):
    previous_code = get_bin_code_of_string(previous)
    current_code = get_bin_code_of_string(current_block)

    left = current_code / 2**32
    right = current_code % 2**32
    for i in range(16, 0, -1):
        new_left = right ^ get_new_key(i)
        new_right = func(right) ^ left
        left = new_left
        right = new_right

    code_for_decrypting = (left * 2**32) | right
    result = code_for_decrypting ^ previous_code
    return get_str_from_num_64(result)


# Start of encrypting with CBC.
def encrypt_with_cbc(original_text):
    original_blocks = get_list_blocks(original_text)

    result_of_encrypting = ''

    # String's of encrypted block. Needs to CBC.
    previous_encrypted_block = 'qwertyui'
    for block in original_blocks:
        encrypted_block = encrypting_block_with_cbc(block, previous_encrypted_block)
        previous_encrypted_block = encrypted_block
        result_of_encrypting += encrypted_block

    return result_of_encrypting


# Start of decrypting with CBC.
def decrypt_with_cbc(encrypted_text):
    encrypted_blocks = get_list_blocks(encrypted_text)

    result_of_decrypting = ''

    # String's of decrypted block. Needs to CBC.
    previous_encrypted_block = 'qwertyui'
    for block in encrypted_blocks:
        decrypted_block = decrypting_block_with_cbc(block, previous_encrypted_block)
        previous_encrypted_block = block
        result_of_decrypting += decrypted_block

    return result_of_decrypting


# Start of encrypting.
def encrypt(original_text):
    original_blocks = get_list_blocks(original_text)

    result_of_encrypting = ''

    for block in original_blocks:
        encrypted_block = encrypting_block(block)
        result_of_encrypting += encrypted_block

    return result_of_encrypting


# Start of decrypting.
def decrypt(encrypted_text):
    encrypted_blocks = get_list_blocks(encrypted_text)

    result_of_decrypting = ''

    for block in encrypted_blocks:
        decrypted_block = decrypting_block(block)
        result_of_decrypting += decrypted_block

    return result_of_decrypting


# Full programme with CBC.
def start_with_cbc():
    # Init files to encrypt and decrypt.
    input_file_to_encrypting = open("input.txt", "r")
    output_file_to_encrypting = open("encrypted.txt", "w")
    output_file_to_decrypting = open("decrypted.txt", "w")

    print '====================================================='
    print 'Crypto with CBC'
    print '====================================================='

    input_text = input_file_to_encrypting.read()
    print 'Input text: ', input_text, '\n'

    encrypted = encrypt_with_cbc(input_text)
    print 'Encrypting done.\nResult: ', encrypted, '\n'
    output_file_to_encrypting.write(encrypted)

    decrypted = decrypt_with_cbc(encrypted)
    print 'Decrypting done.\nResult: ', decrypted, '\n'
    output_file_to_decrypting.write(decrypted)

    # Close files.
    input_file_to_encrypting.close()
    output_file_to_encrypting.close()
    output_file_to_decrypting.close()


# Full programme without CBC.
def start_without_cbc():
    # Init files to encrypt and decrypt.
    input_file_to_encrypting = open("input.txt", "r")
    output_file_to_encrypting = open("encrypted.txt", "w")
    output_file_to_decrypting = open("decrypted.txt", "w")

    print '====================================================='
    print 'Crypto without CBC'
    print '====================================================='

    input_text = input_file_to_encrypting.read()
    print 'Input text: ', input_text, '\n'

    encrypted = encrypt(input_text)
    print 'Encrypting done.\nResult: ', encrypted, '\n'
    output_file_to_encrypting.write(encrypted)

    decrypted = decrypt(encrypted)
    print 'Decrypting done.\nResult: ', decrypted, '\n'
    output_file_to_decrypting.write(decrypted)

    # Close files.
    input_file_to_encrypting.close()
    output_file_to_encrypting.close()
    output_file_to_decrypting.close()


# Here run one of start_with_cbc or start_without_cbc
start_with_cbc()
