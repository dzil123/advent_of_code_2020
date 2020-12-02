valid_passwords = 0

with open("passwords.txt", "r") as f:
    for line in f:
        valid_lens, letter, password = line.strip().split()
        valid_lens = [int(x) for x in valid_lens.split("-")]
        letter = letter.strip(":")
        if valid_lens[0] <= password.count(letter) <= valid_lens[1]:
            valid_passwords += 1

print(valid_passwords)
