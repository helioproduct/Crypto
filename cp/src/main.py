import random
import string
import logging
import bitarray
import matplotlib.pyplot as plt

CNT_TESTS = 11


def get_random_string(N=50):
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(N)
    )


def change_one_bit(msg):
    ba = bitarray.bitarray()
    ba.frombytes(msg.encode("ascii"))
    last_bit = ba[-1]
    new_last = bitarray.bitarray("0") if last_bit else bitarray.bitarray("1")
    ba = ba[:-1]
    ba += new_last
    return bitarray.bitarray(ba.tolist()).tobytes().decode("ascii")


def bitcount(n):
    return bin(n).count("1")


def mean(list_):
    return [int(sum(i) / len(i)) for i in zip(*list_)]


import math
import hashlib


def md5_built_in(s):
    return hashlib.md5(s).hexdigest()


rotate_amounts = [
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
]

tsin = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

init_values = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]

functions = [
    lambda b, c, d: (b & c) | (~b & d),
    lambda b, c, d: (d & b) | (~d & c),
    lambda b, c, d: b ^ c ^ d,
    lambda b, c, d: c ^ (b | ~d),
]

index_functions = [
    lambda i: i,
    lambda i: (5 * i + 1) % 16,
    lambda i: (3 * i + 5) % 16,
    lambda i: (7 * i) % 16,
]


def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


def md5(message_, rounds=4):
    message = bytearray(message_)
    orig_len_in_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder="little")

    hash_pieces = init_values[:]

    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst : chunk_ofst + 64]
        for rr in range(rounds):
            r = rr % 4
            for kk in range(16):
                i = r * 16 + kk
                k = index_functions[r](i)
                x_k = int.from_bytes(chunk[4 * k : 4 * k + 4], byteorder="little")
                f = functions[r](b, c, d)
                to_rotate = a + f + tsin[i] + x_k
                new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
                a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))


def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder="little")
    return "{:032x}".format(int.from_bytes(raw, byteorder="big"))


if __name__ == "__main__":
    logging.basicConfig(filename="analysis.log", level=logging.INFO)

    all_diffs = []
    cnt_rounds = [i for i in range(0, 81, 5)]
    for i in range(1, CNT_TESTS):
        logging.info("Test #{0}".format(i))
        input1 = get_random_string()
        input2 = change_one_bit(input1)

        logging.info("Input string:   {0}".format(input1))
        logging.info("Changed string: {0}".format(input2))

        diffs = []
        rounds = range(0, 81, 5)
        for r in rounds:
            logging.info("Count rounds: {0}".format(r))

            input1_bytes = input1.encode("utf-8")
            input2_bytes = input2.encode("utf-8")

            output1 = md5_to_hex(md5(input1_bytes, r))
            output2 = md5_to_hex(md5(input2_bytes, r))

            logging.info("Output original:  {0}".format(output1))
            logging.info("Output changed:   {0}".format(output2))
            res = bitcount(int(output1, 16) ^ int(output2, 16))
            diffs.append(res)
            logging.info("Count of different bits: {0}".format(res))
        logging.info("------------")
        all_diffs.append(diffs)

    mean_diffs = mean(all_diffs)
    for i, j in zip(cnt_rounds, mean_diffs):
        print("Count rounds: {0}".format(i))
        print("Count of different bits: {0}".format(j))
        print("------------")

    plt.bar(cnt_rounds, mean_diffs, align="center")
    plt.xlabel("Count rounds")
    plt.ylabel("Count of different bits")
    plt.show()
