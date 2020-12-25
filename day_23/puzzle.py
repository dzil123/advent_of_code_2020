from collections import deque
from pprint import pprint
import itertools

# FILE, MOVES = "test.txt", 10
# FILE, MOVES = "test.txt", 100
# FILE, MOVES = "test.txt", 10_000_000
# FILE, MOVES = "puzzle.txt", 100
FILE, MOVES = "puzzle.txt", 10_000_000

def read():
    with open(FILE, "r") as f:
        line = f.readline().strip()
        return [int(n) for n in line]

triggered = []

def kprint(*args, **kwargs):
    if triggered:
        print(*args, **kwargs)

def part1():
    cups = read() # 1 to num_cups
    cups = deque(cups)
    num_cups = len(cups)
    print(cups)
    print()


    for i in range(MOVES):
        # if i > 10:
        #     triggered.append(1)
        kprint(i, list(cups))

        current_cup = cups[0]

        cups.rotate(-1)
        holding = [cups.popleft() for _ in range(3)]
        cups.rotate(1)

        looking = current_cup
        failed = 0
        while True:
            # subtract 1, mod num_cups but starts at 1 instead of 0
            looking = (looking - 2) % num_cups + 1
            try:
                destination = cups.index(looking)
                break
            except ValueError:
                failed += 1
                pass
        
        kprint(cups)
        kprint(holding)
        kprint(destination)

        # insert() puts it before the index, not after, so need to add 1
        destination = (destination + 1) % (len(cups) + 1) # ahh i didnt add 1 to the len which cost so much time, thanks david
        kprint(destination)
        for num in holding[::-1]:
            cups.insert(destination, num)
        
        kprint(cups)
        cups.rotate(-1)
        kprint(cups)
        kprint()

    print(cups)
    while cups[0] != 1:
        cups.rotate(-1)
    
    print(cups)
    cups.popleft()
    result = list(cups)
    result = ''.join(str(n) for n in result)
    print(result)

class Node:
    __slots__ = ("num", "next")

    def __init__(self, num, next=None):
        self.num = num
        self.next = next
    
    def __repr__(self):
        return f"Node({self.num} -> [{self.next}])"

    def print(self, name, limit=None):
        print(f"{name}: ({self.num})", end=" ")
        cup = self
        for i in itertools.count(1):
            if limit is not None and i >= limit:
                break
            cup = cup.next
            if cup is self or cup is None:
                break
            print(cup.num, end=" ")
        print()


def part2():
    cups = read()

    new_cups = [Node(cups[-1])]
    for cup in cups[:-1][::-1]:
        new_cups.insert(0, Node(cup, new_cups[0]))
    
    cups = new_cups

    cup_lookup = {cup.num: cup for cup in cups}

    cup = cups[-1]
    num_cups = 1_000_000
    # num_cups = 15
    # num_cups = 9
    for i in range(len(cups) + 1, num_cups + 1):
        new_cup = Node(i)
        cup.next = new_cup
        # cups.append(new_cup)
        cup_lookup[i] = new_cup
        cup = new_cup
    print(cup.num)
    cup.next = cups[0]
    print(cup.next.num)

    print(len(cup_lookup))
    print(cups[0].num, cups[-1].num, cups[-1].next.num)
    print()

    MISSING = object()

    current_cup = cups[0]
    for i in range(MOVES):
        # print()
        # current_cup.print("cups")

        holding = current_cup.next
        current_cup.next = holding.next.next.next
        holding.next.next.next = None

        # current_cup.print("new_cups")
        # holding.print("holding")

        looking = current_cup.num
        failed = 0
        while True:
            # subtract 1, mod num_cups but starts at 1 instead of 0
            looking = (looking - 2) % num_cups + 1
            if looking == holding.num or looking == holding.next.num or looking == holding.next.next.num:
                failed += 1
                continue
            destination = cup_lookup[looking]
            break

        # print(f"destination val: {destination.num}")

        holding.next.next.next = destination.next
        destination.next = holding

        current_cup = current_cup.next

        n = 1_000_000
        if i % n == 0:
            print(i, i/MOVES)
    
    cup_one = cup_lookup[1]
    cup = cup_one
    print('result')
    for _ in range(2):
        cup = cup.next
        if cup is cup_one:
            break
        print(cup.num, end=" ")
    print()

    # pprint(cups)


# part1()
part2()

# from cProfile import run
# run("part2()")
