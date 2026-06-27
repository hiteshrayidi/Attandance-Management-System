import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import date
DATA_FILE = "students.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"students": [], "attendance": {}}
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
data = load_data()
today = str(date.today())
root = tk.Tk()
root.title("Attendance System")
root.geometry("700x500")
root.config(bg="lightblue")
tk.Label(root, text="Attendance Management System", font=("Arial", 18, "bold"),
         bg="lightblue").pack(pady=10)
tk.Label(root, text="Date: " + today, font=("Arial", 11), bg="lightblue").pack()
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True, padx=10, pady=10)
tab1 = tk.Frame(tabs, bg="lightyellow")
tabs.add(tab1, text="Add Student")
tk.Label(tab1, text="Roll Number:", font=("Arial", 11), bg="lightyellow").pack(pady=(30, 2))
roll_box = tk.Entry(tab1, font=("Arial", 11), width=25)
roll_box.pack()
tk.Label(tab1, text="Student Name:", font=("Arial", 11), bg="lightyellow").pack(pady=(10, 2))
name_box = tk.Entry(tab1, font=("Arial", 11), width=25)
name_box.pack()
msg1 = tk.Label(tab1, text="", font=("Arial", 10), bg="lightyellow", fg="green")
msg1.pack(pady=5)
def add_student():
    roll = roll_box.get().strip()
    name = name_box.get().strip()
    if roll == "" or name == "":
        messagebox.showwarning("Warning", "Please enter both Roll No and Name!")
        return
    for s in data["students"]:
        if s["roll"] == roll:
            messagebox.showerror("Error", "Roll number already exists!")
            return
    data["students"].append({"roll": roll, "name": name})
    save_data(data)
    msg1.config(text="Student added: " + name)
    roll_box.delete(0, tk.END)
    name_box.delete(0, tk.END)
    update_listbox()
tk.Button(tab1, text="Add Student", font=("Arial", 11), bg="green", fg="white",
          command=add_student).pack(pady=8)
tk.Label(tab1, text="Students List:", font=("Arial", 11, "bold"), bg="lightyellow").pack()
listbox = tk.Listbox(tab1, font=("Arial", 10), width=45, height=7)
listbox.pack(pady=5)
def update_listbox():
    listbox.delete(0, tk.END)
    for s in data["students"]:
        listbox.insert(tk.END, "Roll: " + s["roll"] + "  |  Name: " + s["name"])
update_listbox()
def delete_student():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Info", "Select a student to delete!")
        return
    i = selected[0]
    name = data["students"][i]["name"]
    data["students"].pop(i)
    save_data(data)
    msg1.config(text="Deleted: " + name, fg="red")
    update_listbox()
tk.Button(tab1, text="Delete Student", font=("Arial", 10), bg="red", fg="white",
          command=delete_student).pack()
tab2 = tk.Frame(tabs, bg="lightgreen")
tabs.add(tab2, text="Mark Attendance")
tk.Label(tab2, text="Mark Attendance for Today", font=("Arial", 13, "bold"),
         bg="lightgreen").pack(pady=10)
att_frame = tk.Frame(tab2, bg="lightgreen")
att_frame.pack()
att_vars = {}
def load_attendance_tab():
    for widget in att_frame.winfo_children():
        widget.destroy()
    att_vars.clear()
    if len(data["students"]) == 0:
        tk.Label(att_frame, text="No students added yet!", font=("Arial", 11),
                 bg="lightgreen").pack(pady=20)
        return
    existing = data["attendance"].get(today, {})
    tk.Label(att_frame, text="Roll    Name                  Status",
             font=("Arial", 10, "bold"), bg="lightgreen").pack()
    for s in data["students"]:
        roll = s["roll"]
        name = s["name"]
        var = tk.StringVar(value=existing.get(roll, "Present"))
        att_vars[roll] = var
        row = tk.Frame(att_frame, bg="lightgreen")
        row.pack(pady=3)
        tk.Label(row, text=roll, font=("Arial", 10), bg="lightgreen", width=8).pack(side="left")
        tk.Label(row, text=name, font=("Arial", 10), bg="lightgreen", width=20, anchor="w").pack(side="left")
        tk.Radiobutton(row, text="Present", variable=var, value="Present",
                       bg="lightgreen", fg="darkgreen", font=("Arial", 10)).pack(side="left", padx=5)
        tk.Radiobutton(row, text="Absent", variable=var, value="Absent",
                       bg="lightgreen", fg="red", font=("Arial", 10)).pack(side="left")
msg2 = tk.Label(tab2, text="", font=("Arial", 10), bg="lightgreen", fg="blue")
msg2.pack(pady=4)
def save_attendance():
    if len(data["students"]) == 0:
        messagebox.showinfo("Info", "No students to save!")
        return
    data["attendance"][today] = {}
    for roll, var in att_vars.items():
        data["attendance"][today][roll] = var.get()
    save_data(data)
    msg2.config(text="Attendance saved for " + today + " !")
tk.Button(tab2, text="Save Attendance", font=("Arial", 11), bg="blue", fg="white",
          command=save_attendance).pack(pady=6)
load_attendance_tab()
tab3 = tk.Frame(tabs, bg="lightyellow")
tabs.add(tab3, text="View Records")
tk.Label(tab3, text="Attendance Records", font=("Arial", 13, "bold"),
         bg="lightyellow").pack(pady=10)
cols = ("Roll", "Name", "Present", "Absent", "Percentage")
table = ttk.Treeview(tab3, columns=cols, show="headings", height=10)
for c in cols:
    table.heading(c, text=c)
    table.column(c, width=120, anchor="center")
table.pack(padx=10, fill="both", expand=True)
def refresh_table():
    table.delete(*table.get_children())
    for s in data["students"]:
        roll = s["roll"]
        name = s["name"]
        p = 0
        a = 0
        for day in data["attendance"]:
            status = data["attendance"][day].get(roll, "")
            if status == "Present":
                p += 1
            elif status == "Absent":
                a += 1
        total = p + a
        pct = str(round(p / total * 100)) + "%" if total > 0 else "N/A"
        table.insert("", "end", values=(roll, name, p, a, pct))
refresh_table()
tk.Button(tab3, text="Refresh", font=("Arial", 10), bg="purple", fg="white",
          command=refresh_table).pack(pady=6)
tab4 = tk.Frame(tabs, bg="lightpink")
tabs.add(tab4, text="Today Summary")
tk.Label(tab4, text="Today's Attendance Summary", font=("Arial", 13, "bold"),
         bg="lightpink").pack(pady=10)
summary_box = tk.Text(tab4, font=("Arial", 11), width=55, height=14,
                      state="disabled", relief="solid", bd=1)
summary_box.pack(padx=10)
def show_summary():
    summary_box.config(state="normal")
    summary_box.delete("1.0", tk.END)
    att_today = data["attendance"].get(today, {})
    present = 0
    absent  = 0
    summary_box.insert(tk.END, "Date: " + today + "\n")
    summary_box.insert(tk.END, "-" * 40 + "\n")
    if len(data["students"]) == 0:
        summary_box.insert(tk.END, "No students added yet!\n")
    else:
        for s in data["students"]:
            roll   = s["roll"]
            name   = s["name"]
            status = att_today.get(roll, "Not Marked")
            if status == "Present":
                present += 1
                summary_box.insert(tk.END, "PRESENT  -  " + roll + "  " + name + "\n")
            elif status == "Absent":
                absent += 1
                summary_box.insert(tk.END, "ABSENT   -  " + roll + "  " + name + "\n")
            else:
                summary_box.insert(tk.END, "?        -  " + roll + "  " + name + "\n")
        summary_box.insert(tk.END, "-" * 40 + "\n")
        summary_box.insert(tk.END, "Total Present : " + str(present) + "\n")
        summary_box.insert(tk.END, "Total Absent  : " + str(absent)  + "\n")
        summary_box.insert(tk.END, "Total Students: " + str(len(data["students"])) + "\n")
    summary_box.config(state="disabled")
show_summary()
tk.Button(tab4, text="Refresh Summary", font=("Arial", 10), bg="orange", fg="white",
          command=show_summary).pack(pady=6)
root.mainloop()