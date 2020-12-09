import sys

# FILE = "test.txt"
FILE = "intcode2.txt"

program = []

with open(FILE, "r") as f:
    for line in f:
        line = line.strip()
        instruction, argument = line.split()
        program.append([instruction, int(argument)])


def part1():
    ins = 0  # instruction pointer
    acc = 0  # accumulator
    visited = []

    while True:
        if ins in visited:
            break
        visited.append(ins)

        instruction, argument = program[ins]

        if instruction == "nop":
            pass
        elif instruction == "acc":
            acc += argument
        elif instruction == "jmp":
            ins += argument
            continue
        else:
            raise Exception
        ins += 1

    print(acc)


def try_run(program):
    ins = 0  # instruction pointer
    acc = 0  # accumulator
    visited = []

    while True:
        if ins == len(program):
            print(acc)
            sys.exit()

        if ins in visited:
            return None  # failed, infinite loop
        visited.append(ins)

        instruction, argument = program[ins]

        if instruction == "nop":
            pass
        elif instruction == "acc":
            acc += argument
        elif instruction == "jmp":
            ins += argument
            continue
        else:
            raise Exception
        ins += 1


def part2():
    try_run(program)

    for ins in range(len(program)):
        instruction = program[ins][0]
        if instruction == "jmp":
            instruction = "nop"
        elif instruction == "nop":
            instruction = "jmp"
        else:
            continue

        program_copy = [inst[:] for inst in program]
        program_copy[ins][0] = instruction

        try_run(program_copy)

    print("fail")


# part1()
# part2()


def main():
    import cProfile

    cProfile.run("part2()")


main()
