import sys
import dataclasses


def read():
    FILE = "intcode2.txt"
    program = []

    with open(FILE, "r") as f:
        for line in f:
            line = line.strip()
            instruction, argument = line.split()
            program.append([instruction, int(argument)])

    return program


@dataclasses.dataclass
class State:
    program: list
    visited: set() = dataclasses.field(default_factory=set)
    ins: int = 0
    acc: int = 0


def run_one_ins(state):
    instruction, argument = state.program[state.ins]

    if instruction == "nop":
        pass
    elif instruction == "acc":
        state.acc += argument
    elif instruction == "jmp":
        state.ins += argument
        return
    else:
        raise Exception

    state.ins += 1


def run_one_step(state):
    if state.ins == len(state.program):
        print(state.acc)
        sys.exit()

    if state.ins in state.visited:
        return True  # failed, infinite loop
    state.visited.add(state.ins)

    run_one_ins(state)


def run_to_end(state):
    while not run_one_step(state):
        pass


def part2():
    state = State(read())
    while True:
        instruction, _ = state.program[state.ins]
        while True:
            if instruction == "jmp":
                instruction = "nop"
            elif instruction == "nop":
                instruction = "jmp"
            else:
                break

            program_copy = [inst[:] for inst in state.program]
            program_copy[state.ins][0] = instruction

            state_copy = dataclasses.replace(
                state, program=program_copy, visited=state.visited.copy()
            )

            run_to_end(state_copy)
            break

        if run_one_step(state):
            raise Exception


part2()
