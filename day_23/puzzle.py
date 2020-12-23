from collections import deque

# FILE, MOVES = "test.txt", 10
# FILE, MOVES = "test.txt", 100
FILE, MOVES = "puzzle.txt", 100

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


part1()
