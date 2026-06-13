students = []
attendance = {}
def add_student():
    name = input("Enter student name: ")
    students.append(name)
    attendance[name] = []
    print(f"{name} added successfully.")
def mark_attendance():
    if not students:
        print("No students available.")
        return
    date = input("Enter date (YYYY-MM-DD): ")
    for student in students:
        status = input(f"{student} (P/A): ").upper()
        if status == "P":
            attendance[student].append((date, "Present"))
        else:
            attendance[student].append((date, "Absent"))
    print("Attendance marked successfully.")
def view_attendance():
    for student, records in attendance.items():
        print(f"\nStudent: {student}")
        for date, status in records:
            print(f"{date} - {status}")
while True:
    print("\nAttendance Management System")
    print("1.Add Student")
    print("2.Mark Attendance")
    print("3.View Attendance")
    print("4.Exit")
    choice = input("Enter choice: ")
    if choice == "1":
        add_student()
    elif choice == "2":
        mark_attendance()
    elif choice == "3":
        view_attendance()
    elif choice == "4":
        print("Exiting")
        break
    else:
        print("Invalid choice")