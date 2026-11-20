import tkinter as tk
from tkinter import ttk, messagebox

def add_learner(learners, number, name):
    if number in learners:
        return False
    learners[number] = {"name": name, "marks": []}
    return True

def add_mark(learners, number, mark):
    if number not in learners:
        return False
    learners[number]["marks"].append(mark)
    return True

def rename_learner(learners, number, new_name):
    if number not in learners:
        return False
    learners[number]["name"] = new_name
    return True

def delete_learner(learners, number):
    if number not in learners:
        return False
    del learners[number]
    return True

def find_by_name(learners, text):
    matches = []
    for number in learners:
        if text.lower() in learners[number]["name"].lower():
            matches.append(number)
    return matches

def average_of(values):
    total = 0
    for v in values:
        total = total + v
    return total / len(values)

def learner_average(learners, number):
    marks = learners[number]["marks"]
    if len(marks) == 0:
        return None
    return average_of(marks)

def ranking(learners):
    rows = []
    for number in learners:
        avg = learner_average(learners, number)
        if avg is not None:
            rows.append((avg, number))
    n = len(rows)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if rows[j][0] < rows[j + 1][0]:
                rows[j], rows[j + 1] = rows[j + 1], rows[j]
    return rows

def print_ranking(learners):
    rows = ranking(learners)
    if len(rows) == 0:
        print("No marks captured yet.")
        return
    print("Rank  Number    Name          Average")
    for position in range(len(rows)):
        avg = rows[position][0]
        number = rows[position][1]
        name = learners[number]["name"]
        print(f"{position + 1:<6}{number:<10}{name:<14}{avg:>6.1f}")

def is_valid_number(text):
    return text.isdigit() and len(text) == 7

def is_valid_mark(text):
    return text.isdigit() and int(text) <= 100

def show_menu():
    print()
    print("1. Add learner")
    print("2. Add mark")
    print("3. Rename learner")
    print("4. Delete learner")
    print("5. Find by name")
    print("6. Show ranking")
    print("7. Exit")

def ask_number():
    return input("Student number (7 digits): ")

def main():
    learners = {}
    choice = ""
    while choice != "7":
        show_menu()
        choice = input("Choice: ")
        if choice == "1":
            number = ask_number()
            name = input("Name: ")
            if not is_valid_number(number) or name == "":
                print("Invalid number or name.")
            elif add_learner(learners, number, name):
                print("Added.")
            else:
                print("That student number already exists.")
        elif choice == "2":
            number = ask_number()
            text = input("Mark (0-100): ")
            if not is_valid_mark(text):
                print("Invalid mark.")
            elif add_mark(learners, number, int(text)):
                print("Mark added.")
            else:
                print("No such learner.")
        elif choice == "3":
            number = ask_number()
            if rename_learner(learners, number, input("New name: ")):
                print("Renamed.")
            else:
                print("No such learner.")
        elif choice == "4":
            if delete_learner(learners, ask_number()):
                print("Deleted.")
            else:
                print("No such learner.")
        elif choice == "5":
            found = find_by_name(learners, input("Name contains: "))
            if len(found) == 0:
                print("No match.")
            for number in found:
                print(number, learners[number]["name"], learners[number]["marks"])
        elif choice == "6":
            print_ranking(learners)
        elif choice == "7":
            print("Goodbye.")
        else:
            print("Invalid choice. Enter 1 to 7.")

class LearnerRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NCV LEVEL 4 • LEARNER REGISTER")
        self.root.geometry("950x650")
        self.root.configure(bg="#f4f6f7")
        
        self.learners = {}
        
        self.create_widgets()
        self.load_examples()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg="#1a5276", pady=15)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="NCV LEVEL 4 • LEARNER REGISTER", 
                 font=("Helvetica", 18, "bold"), fg="white", bg="#1a5276").pack()
        tk.Label(header_frame, text="Day 3 | Dictionaries · Lists · Bubble Sort · Validation", 
                 font=("Helvetica", 10), fg="#aeb6bf", bg="#1a5276").pack()

        input_frame = tk.Frame(self.root, bg="#f4f6f7", padx=20, pady=15)
        input_frame.pack(fill=tk.X)
        
        def make_entry(parent, label_text, col):
            tk.Label(parent, text=label_text, bg="#f4f6f7", font=("Helvetica", 9)).grid(row=0, column=col, sticky="w", pady=(0, 2))
            entry = tk.Entry(parent, width=20 if col != 2 else 10)
            entry.grid(row=1, column=col, padx=(0, 15), pady=0)
            return entry

        self.entry_number = make_entry(input_frame, "Student number (7 digits)", 0)
        self.entry_name = make_entry(input_frame, "Name", 1)
        self.entry_mark = make_entry(input_frame, "Mark (0-100)", 2)

        btn_frame = tk.Frame(self.root, bg="#f4f6f7", padx=20)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        btn_opts = {"bg": "#e5e8e8", "activebackground": "#d5dbdb", "relief": tk.RAISED, "bd": 1}
        
        buttons = [
            ("1. Add learner", self.gui_add_learner, 0),
            ("2. Add mark", self.gui_add_mark, 1),
            ("3. Rename", self.gui_rename, 2),
            ("4. Delete", self.gui_delete, 3),
            ("5. Find by name", self.gui_find, 4),
            ("6. Show ranking", self.gui_show_ranking, 5),
            ("7. Exit", self.root.quit, 6)
        ]
        
        for text, cmd, col in buttons:
            tk.Button(btn_frame, text=text, command=cmd, width=14, **btn_opts).grid(row=0, column=col, padx=2)

        tk.Button(btn_frame, text="Load example learners", command=self.load_examples, **btn_opts).grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))
        tk.Button(btn_frame, text="Class statistics", command=self.gui_class_stats, **btn_opts).grid(row=1, column=2, columnspan=2, sticky="w", pady=(10, 0))

        table_frame = tk.Frame(self.root, bg="#f4f6f7", padx=20, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(table_frame, text="Learner records (select a row to edit)", bg="#f4f6f7", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 5))

        columns = ("Student Number", "Learner Name", "Marks", "Average")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
            
        self.tree.column("Student Number", width=130)
        self.tree.column("Learner Name", width=200)
        self.tree.column("Marks", width=300)
        self.tree.column("Average", width=120)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_examples(self):
        self.learners = {
            "2024001": {"name": "Phetolo", "marks": [65, 72]},
            "2024002": {"name": "Thandi", "marks": [90, 55]},
            "2024003": {"name": "Sipho", "marks": [48, 72]},
            "2024004": {"name": "Maria", "marks": [48, 72]},
        }
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for number, data in self.learners.items():
            name = data["name"]
            marks_str = ", ".join(str(m) for m in data["marks"])
            avg = learner_average(self.learners, number)
            avg_str = f"{avg:.1f}%" if avg is not None else "N/A"
            
            self.tree.insert("", tk.END, values=(number, name, marks_str, avg_str))

    def clear_entries(self):
        self.entry_number.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_mark.delete(0, tk.END)

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, 'values')
        if values:
            self.clear_entries()
            self.entry_number.insert(0, values[0])
            self.entry_name.insert(0, values[1])

    def gui_add_learner(self):
        number = self.entry_number.get().strip()
        name = self.entry_name.get().strip()
        
        if not is_valid_number(number) or name == "":
            messagebox.showerror("Error", "Invalid number (must be 7 digits) or name.")
            return
            
        if add_learner(self.learners, number, name):
            messagebox.showinfo("Success", "Learner Added.")
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "That student number already exists.")

    def gui_add_mark(self):
        number = self.entry_number.get().strip()
        text = self.entry_mark.get().strip()
        
        if not is_valid_mark(text):
            messagebox.showerror("Error", "Invalid mark. Must be 0-100.")
            return
            
        if add_mark(self.learners, number, int(text)):
            messagebox.showinfo("Success", "Mark added.")
            self.refresh_table()
            self.entry_mark.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No such learner found.")

    def gui_rename(self):
        number = self.entry_number.get().strip()
        new_name = self.entry_name.get().strip()
        
        if new_name == "":
            messagebox.showerror("Error", "Name cannot be empty.")
            return
            
        if rename_learner(self.learners, number, new_name):
            messagebox.showinfo("Success", "Renamed.")
            self.refresh_table()
        else:
            messagebox.showerror("Error", "No such learner found.")

    def gui_delete(self):
        number = self.entry_number.get().strip()
        if not number:
            messagebox.showerror("Error", "Select a learner or enter a number to delete.")
            return
            
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete {number}?")
        if confirm:
            if delete_learner(self.learners, number):
                messagebox.showinfo("Success", "Deleted.")
                self.refresh_table()
                self.clear_entries()
            else:
                messagebox.showerror("Error", "No such learner found.")

    def gui_find(self):
        search_term = self.entry_name.get().strip()
        if not search_term:
            messagebox.showinfo("Search", "Type a name in the 'Name' box to search.")
            return
            
        found = find_by_name(self.learners, search_term)
        if len(found) == 0:
            messagebox.showinfo("Search", "No match found.")
        else:
            result_text = "Found:\n"
            for number in found:
                result_text += f"{number}: {self.learners[number]['name']}\n"
            messagebox.showinfo("Search Results", result_text)

    def gui_show_ranking(self):
        rows = ranking(self.learners)
        if len(rows) == 0:
            messagebox.showinfo("Ranking", "No marks captured yet.")
            return
            
        result_text = "Rank  Number    Name          Average\n"
        result_text += "-" * 45 + "\n"
        for position in range(len(rows)):
            avg = rows[position][0]
            number = rows[position][1]
            name = self.learners[number]["name"]
            result_text += f"{position + 1:<6}{number:<10}{name:<14}{avg:>6.1f}%\n"
            
        top = tk.Toplevel(self.root)
        top.title("Class Ranking")
        top.geometry("500x400")
        
        text_widget = tk.Text(top, font=("Courier", 11), padx=10, pady=10, bg="#fdfefe")
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, result_text)
        text_widget.config(state=tk.DISABLED)

    def gui_class_stats(self):
        if not self.learners:
            messagebox.showinfo("Statistics", "No learners in the register.")
            return
            
        all_marks = []
        for num in self.learners:
            all_marks.extend(self.learners[num]["marks"])
            
        if not all_marks:
            messagebox.showinfo("Statistics", "No marks entered yet.")
            return
            
        highest = all_marks[0]
        lowest = all_marks[0]
        total = 0
        for m in all_marks:
            total += m
            if m > highest: highest = m
            if m < lowest: lowest = m
            
        avg = total / len(all_marks)
        
        stats_text = (
            f"Class Statistics\n"
            f"-----------------\n"
            f"Total learners: {len(self.learners)}\n"
            f"Total marks recorded: {len(all_marks)}\n"
            f"Class Average: {avg:.1f}%\n"
            f"Highest Mark: {highest}\n"
            f"Lowest Mark: {lowest}\n"
        )
        messagebox.showinfo("Class Statistics", stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = LearnerRegisterApp(root)
    root.mainloop()

