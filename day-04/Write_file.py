f = open("notes.txt", "w")
f.write("Hello Thonny\n")
f.write("Second line\n")
f.close()

f = open("notes.txt", "r")

print(f.read())
f.close()
