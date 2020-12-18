import re


class Int:
    def __init__(self, val):
        self.val = val

    # operator + in part 1
    def __add__(self, other):
        return Int(self.val + other.val)

    # operator + in part 2
    def __truediv__(self, other):
        return self + other

    # operator * in part 1 and part 2
    def __sub__(self, other):
        return Int(self.val * other.val)

    def __str__(self):
        return str(self.val)


class Part1:
    @classmethod
    def eval(cls, expr):
        expr = cls.modify(expr)
        return eval(expr).val

    @classmethod
    def modify(cls, expr):
        return re.sub(r"(\d+)", r"Int(\1)", expr).replace("*", "-")


class Part2(Part1):
    # eg "1 + 2 * 3 + 4 * 5 + 6" -> "Int(1) / Int(2) - Int(3) / Int(4) - Int(5) / Int(6)"
    @classmethod
    def modify(cls, expr):
        return super().modify(expr).replace("+", "/")


def run():
    result = 0

    with open("puzzle.txt", "r") as f:
        for line in f:
            line = line.strip()
            result += Part2.eval(line)  # changeme for part 1/2

    return result


print(run())
