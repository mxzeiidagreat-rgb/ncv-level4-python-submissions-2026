with open("notes.txt", "a") as f:
      f.write("Forth line\n")
with open("notes.txt") as f:
    
    for line in f:
        print(line.strip(), print(len(line)))
