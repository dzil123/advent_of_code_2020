from typing import NamedTuple
import dataclasses


class Range(NamedTuple):
    low: int
    high: int

    @classmethod
    def parse(cls, s: str) -> "Range":
        low, high = [int(x) for x in s.strip().split("-")]
        assert low <= high
        return cls(low=low, high=high)

    @classmethod
    def parse_many(cls, s: str) -> list["Range"]:
        ranges = s.strip().split(" or ")
        return [cls.parse(x) for x in ranges]

    def contains(self, x):
        return self.low <= x <= self.high


@dataclasses.dataclass
class Rule:
    name: str
    ranges: list[Range]

    @classmethod
    def parse(cls, s: str) -> "Rule":
        name, rest = s.strip().split(":", 1)
        ranges = Range.parse_many(rest)
        return cls(name=name, ranges=ranges)


Ticket = list[int]


def Ticket_parse(s: str) -> Ticket:
    return [int(x) for x in s.strip().split(",")]


@dataclasses.dataclass
class Input:
    rules: list[Rule]
    my_ticket: Ticket
    nearby_tickets: list[Ticket]

    @classmethod
    def parse(cls, f):
        rules = []
        for line in f:
            line = line.strip()
            if not line:
                break
            rules.append(Rule.parse(line))

        assert f.readline().strip() == "your ticket:"
        my_ticket = Ticket_parse(f.readline())

        assert f.readline().strip() == ""
        assert f.readline().strip() == "nearby tickets:"
        nearby_tickets = []
        for line in f:
            nearby_tickets.append(Ticket_parse(line))

        return cls(rules=rules, my_ticket=my_ticket, nearby_tickets=nearby_tickets)


def read_file(filename):
    with open(filename, "r") as f:
        return Input.parse(f)


def part1(data):
    ranges = []
    for rule in data.rules:
        ranges += rule.ranges

    invalid_fields = []
    valid_tickets = []
    for ticket in data.nearby_tickets:
        valid_ticket = True
        for field in ticket:
            for rang in ranges:
                if rang.contains(field):
                    break
            else:
                invalid_fields.append(field)
                valid_ticket = False
        if valid_ticket:
            valid_tickets.append(ticket)

    valid_data = dataclasses.replace(data, nearby_tickets=valid_tickets)

    return sum(invalid_fields), valid_data


def is_rule_valid(rule, field_index, data):
    for ticket in data.nearby_tickets:
        if not any(rang.contains(ticket[field_index]) for rang in rule.ranges):
            return False
    return True


def is_solved(possible_fields):
    for field in possible_fields:
        if len(field) == 0:
            raise Exception("unsolvable")
        elif len(field) > 1:
            return False
    return True


def part2(data):
    possible_fields = [set() for _ in range(len(data.my_ticket))]

    for rule_index, rule in enumerate(data.rules):
        for field_index in range(len(data.my_ticket)):
            if is_rule_valid(rule, field_index, data):
                possible_fields[field_index].add(rule.name)

    already_solved = set()

    while not is_solved(possible_fields):
        for index, possible_field in enumerate(possible_fields):
            if index in already_solved:
                continue
            if len(possible_field) == 1:
                # solved this rule, remove this rule from all other possibilities
                already_solved.add(index)
                rule = next(iter(possible_field))
                for i in range(len(possible_fields)):
                    if i == index:
                        continue
                    possible_fields[i].discard(rule)
                break
        else:
            # went all through the loop without solving one field
            raise Exception("unsolvable")

    # now each field in possible_fields has only one option in it, aka it is solved
    fields = [next(iter(field)) for field in possible_fields]

    product = 1
    for index, field in enumerate(fields):
        if not field.startswith("departure"):
            continue
        product *= data.my_ticket[index]

    return possible_fields, product


def main():
    # FILE = "test.txt"
    # FILE = "test2.txt"
    FILE = "puzzle.txt"

    data = read_file(FILE)

    sum_invalid_fields, data = part1(data)
    print(sum_invalid_fields, end="\n\n")

    print(part2(data))


if __name__ == "__main__":
    main()
