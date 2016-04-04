from math import floor


# returns array of basic multipliers
# multipliers[0] = p, multipliers[1] = q
def factor(number):
    # number = self.n
    multipliers = []
    divider = 2
    while divider * divider <= number:
        if number % divider == 0:
            multipliers.append(divider)
            number //= divider
        else:
            divider += 1
    if number > 1:
        multipliers.append(number)
    return multipliers


# Both functions take positive integers a, b as input, and return a triple (g, x, y),
# such that ax + by = g = gcd(a, b).
def egcd(a, b):  # e, n in our task
    x, y,  u, v = 0, 1,  1, 0
    while a != 0:
        q, r = b//a, b % a
        m, n = x - u * q, y - v * q
        b, a,  x, y,  u, v = a, r,  u, v,  m, n
    gcd = b
    return gcd, x, y


# An application of extended GCD algorithm to finding modular inverses
def modinv(a, m):  # e, n in our tsk
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


def dectobin(x):
    bin = []
    while x != 0:
        bin.append(x % 2)
        x = floor(x / 2)
    return bin


def bigmod(base, exponent, mod):
    a = dectobin(exponent)
    # b = len(a)
    btemp = 1
    f = []
    i = 0
    j = 0
    f.append((base**(2**0)) % mod)
    while i < len(a) - 1:
        f.append((f[i]**2) % mod)
        i += 1
    while j < len(a):
        if a[j] == 1.0:
            btemp = (btemp*f[j]) % mod
        j += 1

    modp = btemp % mod
    return modp


def get_list_of_encrypted_blocks(num, max_value):
    encrypted_text = str(num)
    blocks = []
    i = 0
    len_max = len(str(max_value))
    while i < len(encrypted_text):
        block = encrypted_text[i:i+len_max]
        if int(block) < max_value:
            blocks.append(int(block))
            i += len_max
        else:
            blocks.append(int(encrypted_text[i:i+len_max - 1]))
            i += len_max - 1
    return blocks


def int_to_char(block):
    str_block = str(block)
    result = []
    i = 0
    while i < len(str_block):
        part = int(str_block[i:i+2])
        result.append(chr(part))
        i += 2
    return result


def start():
    n = 274611845366113
    e = 23311
    crypto = 108230462382949240744446393133139920760825242128635453394626156290136879344
    multipliers = factor(n)
    print multipliers
    fi = (multipliers[0] - 1)*(multipliers[1] - 1)
    d = modinv(e, fi)
    encrypto_blocks = get_list_of_encrypted_blocks(crypto, n)
    decrypto_blocks = []

    for block in encrypto_blocks:
        decrypto_blocks.append(str(bigmod(block, d, n)))

    decrypto_blocks_str = ''.join(decrypto_blocks)

    print ''.join(int_to_char(decrypto_blocks_str))

start()

