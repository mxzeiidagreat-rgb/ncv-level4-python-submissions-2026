with open("log.txt", "w") as f:
    f.write("first\n")
with open("log.txt", "w") as f:
    f.write("second\n")
with open("log.txt") as f:
  print(f.read())
