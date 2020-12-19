import re

# FILE = "test.txt"
# FILE = "test2.txt"
FILE = "puzzle.txt"


def regex(line):
    R = r"(?P<index>\d+)\:\s*(?P<rest>.*)"
    match = re.search(R, line)

    index, rest = (match[key] for key in ("index", "rest"))

    R = r"(?:\"(?P<literal>.*?)\")|(?P<rest>.*)"
    match = re.search(R, rest)

    if (literal := match["literal"]) is not None:
        return index, literal

    rest = match["rest"]
    # assert rest is not None

    options = []
    for branch in rest.split("|"):
        R = r"(\d+)"
        parsed = re.findall(R, branch)
        options.append(parsed)

    return index, options


def fmt_group(pattern):
    return "(?:{})".format(pattern)


def compile(rules, index, cache=None):
    if cache is None:
        cache = {}

    if (res := cache.get(index)) is not None:
        return res

    def compile_branch(branch):
        if index not in branch:  # part 1
            return "".join(compile(rules, i, cache) for i in branch)

        # part 2
        # assume the recursive index only occurs once in branch, eg "1: 2 3 | 2 1 1 3" not allowed
        recur_index = branch.index(index)
        start, end = branch[:recur_index], branch[recur_index + 1 :]
        start, end = compile_branch(start), compile_branch(end)

        fmt_str = ""
        for x in (start, end):
            if x:
                fmt_str += fmt_group(x) + "{{{0}}}"

        def loop():
            # doing it up to any number of recursions is really hard, see https://stackoverflow.com/a/23002044
            # since each pattern must consume 1+ chars, the max number of recursions is max(len(message)) -> 80 for my input
            # but turns out my input only requires 6, so whatever
            for x in range(1, 6):
                yield fmt_group(fmt_str.format(x))

        return fmt_group("|".join(loop()))

    rule = rules[index]

    if isinstance(rule, str):
        res = re.escape(rule)
    else:
        res = fmt_group("|".join(compile_branch(branch) for branch in rule))

    cache[index] = res
    return res


def read():
    rules = {}
    messages = []

    with open(FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                break

            index, rule = regex(line)
            rules[index] = rule

        for line in f:
            messages.append(line.strip())

    return rules, messages


def partn(hook=lambda x: x):
    rules, messages = read()

    rules = hook(rules)

    ROOT = "0"
    compiled = compile(rules, ROOT)

    matches = sum(re.fullmatch(compiled, message) is not None for message in messages)

    return matches


def part1():
    return partn()


def part2():
    OVERRIDE = """8: 42 | 42 8
                  11: 42 31 | 42 11 31"""

    def hook(rules):
        for line in OVERRIDE.split("\n"):
            index, rule = regex(line)
            rules[index] = rule
        return rules

    return partn(hook)


print(part1())
print(part2())
