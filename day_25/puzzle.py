import re
import enum
from collections import defaultdict
from pprint import pprint
import sympy
import itertools
from sys import exit
import math 

FILE = "test.txt"
# FILE = "test2.txt"
# FILE = "puzzle.txt"

# def encrypt(subject, loop):
#     val = 1
#     for i in range(loop):
#         val = (val * subject) % 20201227
#     return val

def encrypt(subject, loop):
    return (subject ** loop) % 20201227

def read():
    data = []

    with open(FILE, "r") as f:
        for line in f:
            line = line.strip()
    
    return data

def try_factor(x):
    for n in itertools.count():
        xx = x + n * 20201227
        f = sympy.factorint(xx)
        if len(f) == 1:
            X, N = list(f.items())[0]
            if N == 1:
                continue
            yield X, N

def try_factor2(xs):
    for N in itertools.count():
        n = N * 20201227
        for x in xs:
            xx = x + n
            f = math.log(xx, 7)
            if int(f) == f:
                yield x, 7, N

def try_factor3(xs):
    x1, x2 = xs
    c = 1
    for N in itertools.count():
        c = (c * 7) % 20201227
        if c == x1:
            yield (x1, N)
        if c == x2:
            yield (x2, N)

def part1():
    print(encrypt(13651422, 620543+1))
    exit()

    # xs = (5764801, 17807724)
    xs = (13316116, 13651422)
    i = try_factor3(xs)
    while True:
        print(next(i))

    # print(next(try_factor(5764801)))
    # print(next(try_factor(17807724)))
    # print(next(try_factor(13316116)))
    # print(next(try_factor(13651422)))

    # data = read()
    # for n in itertools.count():
    #     if n > 20:
    #         break
    #     print(n)
    #     try_factor(5764801, n)
    #     try_factor(17807724, n)


def run():
    part1()

if __name__ == "__main__":
    run()
