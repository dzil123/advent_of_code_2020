valid_passwords = 0

with open("passwords.txt", "r") as f:
    for line in f:
        valid_indices, letter, password = line.strip().split()
        valid_indices = [int(x) for x in valid_indices.split("-")]
        letter = letter.strip(":")
        if sum([password[i - 1] == letter for i in valid_indices]) == 1:
            valid_passwords += 1

print(valid_passwords)
