# FILE = "test.txt"
FILE = "puzzle.txt"

# PART = 1
PART = 2

NUM = object()
RPAREN = object()
OP = object()


def preprocess_token(line):
    line = line.lstrip()
    if not line:
        return None, None, None

    if line.startswith("("):
        expr, rest = preprocess_expression(line[1:])
        return NUM, f"({expr})", rest
    elif line.startswith(")"):
        return RPAREN, None, line[1:]
    else:
        for op in ("+", "*"):
            if line.startswith(op):
                return OP, op, line[1:]

        num, rest = line[0], line[1:]
        return NUM, num, rest


def preprocess_expression(line, lval=None):
    if lval is None:
        token, lval, line = preprocess_token(line)
        assert token == NUM

    token, op, line = preprocess_token(line)
    if token in (None, RPAREN):
        return lval, line
    assert token == OP

    token, rval, line = preprocess_token(line)
    assert token == NUM

    if op == "+":
        if len(lval) > 1:
            lval = f"({lval})"
        if len(rval) > 1:
            rval = f"({rval})"

        acc, res = "", f"({lval} {op} {rval})"
    else:
        acc, res = f"{lval} {op} ", rval

    res, line = preprocess_expression(line, res)
    return acc + res, line


def parse_token(line):
    line = line.lstrip()
    if not line:
        return None, None, None

    if line.startswith("("):
        expr, rest = parse_expression(line[1:])
        return NUM, expr, rest
    elif line.startswith(")"):
        return RPAREN, None, line[1:]
    else:
        for op in ("+", "*"):
            if line.startswith(op):
                return OP, op, line[1:]

        num, rest = line[0], line[1:]
        num = int(num)
        return NUM, num, rest


def parse_expression(line):
    op = None
    acc = None

    while True:
        if op is None:
            token, acc, line = parse_token(line)

            token, op, line = parse_token(line)
            if token in (None, RPAREN):
                return acc, line
            assert token == OP

            continue

        token, rval, line = parse_token(line)
        assert token == NUM

        if op == "+":
            acc = acc + rval
        elif op == "*":
            acc = acc * rval
        else:
            assert False

        token, op, line = parse_token(line)
        if token in (None, RPAREN):
            return acc, line
        assert token == OP


def run():
    result = 0

    with open(FILE, "r") as f:
        for line in f:
            line = line.strip()
            if PART == 2:
                line = preprocess_expression(line)[0]
            result += parse_expression(line)[0]

    return result


print(run())
