
names = ["Thandi", "Sipho", "Lerato", "Dumisani", "Naledi"]

with open("names.txt", "w") as f:
    for n in names:
        f.write(n + "\n")

with open("names.txt", "a") as f:
    f.write("Karabo\n")

with open("names.txt", "r") as f:
    lines = f.readlines()

print("Lines:", len(lines))
print("\nBackward:")
for line in reversed(lines):
    print(line.strip().upper())

try:
    open("does_not_exist.txt").read()
except FileNotFoundError:
    print("\nFile does not exist - no crash.")