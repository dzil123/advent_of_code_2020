text = open("test.txt", "r").read()
text = [group.split("\n") for group in text.split("\n\n")]
print(text)

with open(FILE, "r") as f:
    text = [group.split("\n") for group in f.read().split("\n\n")]
