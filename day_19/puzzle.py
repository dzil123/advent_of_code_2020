import re

FILE = "test.txt"
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
    assert rest is not None

    options = []
    for branch in rest.split("|"):
        R = r"(\d+)"
        parsed = re.findall(R, branch)
        options.append(parsed)

    return index, options


def compile(rules, index, cache=None):
    if cache is None:
        cache = {}

    if (res := cache.get(index)) is not None:
        return res

    rule = rules[index]

    if isinstance(rule, str):
        res = re.escape(rule)
    else:
        res = "(?:{})".format(
            "|".join(
                "".join(compile(rules, i, cache) for i in branch) for branch in rule
            )
        )

    cache[index] = res
    return res


def part1():
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

    ROOT = "0"
    compiled = compile(rules, ROOT)
    # compiled = f"^{compiled}$"

    matches = sum(re.fullmatch(compiled, message) is not None for message in messages)

    return matches


print(part1())
