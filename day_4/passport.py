import sys


def check_byr(x):
    return 1920 <= int(x) <= 2002


def check_iyr(x):
    return 2010 <= int(x) <= 2020


def check_eyr(x):
    return 2020 <= int(x) <= 2030


def check_hgt(x):
    unit = x[-2:]
    x = int(x[:-2])
    if unit == "cm":
        return 150 <= x <= 193
    elif unit == "in":
        return 59 <= x <= 76
    raise Exception("not valid unit", unit, x)


def check_hcl(x):
    assert x[0] == "#"
    x = x[1:]
    for c in x:
        assert c in "0123456789abcdef"
    return len(x) == 6


def check_ecl(x):
    return x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def check_pid(x):
    for c in x:
        assert c in "0123456789"
    return len(x) == 9


KEYS1 = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]  # problem 1
KEYS2 = {  # problem 2
    "iyr": check_iyr,
    "ecl": check_ecl,
    "eyr": check_eyr,
    "hgt": check_hgt,
    "hcl": check_hcl,
    "pid": check_pid,
    "byr": check_byr,
}


valid = [0]


def check_passport1(passport):
    print("check:")
    for key in KEYS1:
        if not key in passport:
            print("missing", key)
            break
    else:
        print("valid")
        valid[0] += 1
    print()


def check_passport2(passport):
    print(passport)
    for key, check in KEYS2.items():
        val = passport.get(key)
        if val is None:
            print("missing", key)
            break
        try:
            if not check(val):
                print("fail", key)
                break
        except:
            print(key, sys.exc_info()[1])
            break
    else:
        print("valid")
        valid[0] += 1
    print()


check_passport = check_passport2  # select problem 1 or problem 2 here

with open("passport.txt", "r") as f:
    passport = {}
    for line in f:
        line = line.strip()
        if not line:
            if passport == {}:
                continue
            check_passport(passport)
            passport = {}
            continue
        for item in line.split():
            key, value = item.split(":")
            passport[key] = value
    if passport:
        check_passport(passport)
        passport = {}

print(valid[0])
