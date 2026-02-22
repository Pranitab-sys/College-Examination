import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="college_exam_db"
    )

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("College Exam Management System")
root.geometry("1200x700")
root.resizable(False, False)

bg_main = "#1f2937"
bg_sidebar = "#111827"
accent = "#2563eb"

root.configure(bg=bg_main)

# ---------------- HEADER ----------------
header = tk.Frame(root, bg=accent, height=60)
header.pack(fill="x")

tk.Label(header,
         text="College Exam Management System",
         bg=accent,
         fg="white",
         font=("Segoe UI", 18, "bold")).pack(pady=10)

# ---------------- SIDEBAR ----------------
sidebar = tk.Frame(root, bg=bg_sidebar, width=220)
sidebar.pack(side="left", fill="y")

# ---------------- MAIN AREA ----------------
main_area = tk.Frame(root, bg=bg_main)
main_area.pack(side="right", fill="both", expand=True)

# ---------------- TREEVIEW ----------------
tree = ttk.Treeview(main_area)
tree.pack(fill="both", expand=True, padx=20, pady=20)

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=28,
                fieldbackground="white")

# ---------------- CLEAR TREE ----------------
def clear_tree():
    for item in tree.get_children():
        tree.delete(item)

# ---------------- SHOW DATA ----------------
def show_data(query):

    try:
        conn = get_connection()
        cursor = conn.cursor(buffered=True)

        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        clear_tree()

        tree["columns"] = columns
        tree["show"] = "headings"

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for row in rows:
            tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- FORM AREA ----------------
form_frame = tk.Frame(main_area, bg=bg_main)
form_frame.pack(pady=10)

entries = {}

def create_form(labels):

    for widget in form_frame.winfo_children():
        widget.destroy()

    entries.clear()

    for i, label in enumerate(labels):

        tk.Label(form_frame,
                 text=label,
                 bg=bg_main,
                 fg="white",
                 font=("Segoe UI", 10)).grid(row=0, column=i, padx=5)

        entry = tk.Entry(form_frame)
        entry.grid(row=1, column=i, padx=5)

        entries[label] = entry


# ---------------- STUDENT MODULE ----------------
def student_module():

    create_form(["ID", "Name", "Roll No", "Course", "Semester"])

    # ADD
    def add():

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO student (name, roll_no, course, semester) VALUES (%s,%s,%s,%s)",
                (
                    entries["Name"].get(),
                    entries["Roll No"].get(),
                    entries["Course"].get(),
                    entries["Semester"].get()
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            show_data("""
SELECT 
ROW_NUMBER() OVER (ORDER BY student_id) AS Sr_No,
student_id,
name,
roll_no,
course,
semester
FROM student
""")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    # UPDATE
    def update():

        if entries["ID"].get() == "":
            messagebox.showwarning("Warning", "Enter ID to update")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """UPDATE student
                   SET name=%s, roll_no=%s, course=%s, semester=%s
                   WHERE student_id=%s""",
                (
                    entries["Name"].get(),
                    entries["Roll No"].get(),
                    entries["Course"].get(),
                    entries["Semester"].get(),
                    int(entries["ID"].get())
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            show_data("SELECT * FROM student")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    # DELETE (FIXED)
    def delete():

        if entries["ID"].get() == "":
            messagebox.showwarning("Warning", "Enter ID to delete")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM student WHERE student_id=%s",
                (int(entries["ID"].get()),)
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Deleted Successfully")

            show_data("SELECT * FROM student")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    tk.Button(form_frame,
              text="Add",
              bg="#16a34a",
              fg="white",
              command=add).grid(row=2, column=0, pady=10)

    tk.Button(form_frame,
              text="Update",
              bg="#f59e0b",
              fg="white",
              command=update).grid(row=2, column=1)

    tk.Button(form_frame,
              text="Delete",
              bg="#dc2626",
              fg="white",
              command=delete).grid(row=2, column=2)

    show_data("SELECT * FROM student")


# ---------------- SUBJECT MODULE ----------------
def subject_module():

    create_form(["Subject Name", "Semester"])

    def add():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO  subject (subject_name, semester) VALUES (%s,%s)",
            (
                entries["Subject Name"].get(),
                entries["Semester"].get()
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        show_data("SELECT * FROM subject")

    tk.Button(form_frame,
              text="Add Subject",
              bg="#16a34a",
              fg="white",
              command=add).grid(row=2, column=0, pady=10)

    show_data("SELECT * FROM subject")


# ---------------- EXAM MODULE ----------------
def exam_module():

    create_form(["Exam Type", "Exam Year"])

    def add():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO exam (exam_type, exam_year) VALUES (%s,%s)",
            (
                entries["Exam Type"].get(),
                entries["Exam Year"].get()
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        show_data("SELECT * FROM exam")

    tk.Button(form_frame,
              text="Add Exam",
              bg="#16a34a",
              fg="white",
              command=add).grid(row=2, column=0, pady=10)

    show_data("SELECT * FROM exam")


# ---------------- MARKS MODULE ----------------

def marks_module():

    create_form(["Marks ID", "Student ID", "Subject ID", "Exam ID", "Marks"])

    # ---------------- FILL FORM WHEN ROW CLICKED ----------------
    def fill_form(event):

        selected = tree.focus()

        if not selected:
            return

        values = tree.item(selected, "values")

        entries["Marks ID"].delete(0, tk.END)
        entries["Student ID"].delete(0, tk.END)
        entries["Subject ID"].delete(0, tk.END)
        entries["Exam ID"].delete(0, tk.END)
        entries["Marks"].delete(0, tk.END)

        entries["Marks ID"].insert(0, values[0])
        entries["Student ID"].insert(0, values[1])
        entries["Subject ID"].insert(0, values[2])
        entries["Exam ID"].insert(0, values[3])
        entries["Marks"].insert(0, values[4])


    tree.bind("<ButtonRelease-1>", fill_form)


    # ---------------- ADD MARKS ----------------
    def add():

        student_id = entries["Student ID"].get().strip()
        subject_id = entries["Subject ID"].get().strip()
        exam_id = entries["Exam ID"].get().strip()
        marks = entries["Marks"].get().strip()

        if not student_id or not subject_id or not exam_id or not marks:
            messagebox.showwarning("Warning", "Fill all fields")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # check duplicate
            cursor.execute("""
                SELECT COUNT(*)
                FROM marks
                WHERE student_id=%s AND subject_id=%s AND exam_id=%s
            """, (student_id, subject_id, exam_id))

            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror(
                    "Duplicate Error",
                    "Marks already exist for this student in this subject and exam"
                )
            else:
                cursor.execute("""
                    INSERT INTO marks
                    (student_id, subject_id, exam_id, marks_obtained)
                    VALUES (%s,%s,%s,%s)
                """, (student_id, subject_id, exam_id, marks))

                conn.commit()

                messagebox.showinfo("Success", "Marks added")

                show_data("SELECT * FROM marks")

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))


    # ---------------- DELETE MARKS ----------------
    def delete():

        marks_id = entries["Marks ID"].get().strip()

        if not marks_id:
            messagebox.showwarning("Warning", "Select a row to delete")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM marks WHERE marks_id=%s",
                (marks_id,)
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Marks deleted")

            show_data("SELECT * FROM marks")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    # ---------------- BUTTONS ----------------
    tk.Button(form_frame,
              text="Add Marks",
              bg="#16a34a",
              fg="white",
              font=("Segoe UI", 10, "bold"),
              command=add).grid(row=2, column=0, pady=10)

    tk.Button(form_frame,
              text="Delete Marks",
              bg="#dc2626",
              fg="white",
              font=("Segoe UI", 10, "bold"),
              command=delete).grid(row=2, column=1, pady=10)


    show_data("SELECT * FROM marks")
# ---------------- GENERATE RESULT ----------------
def generate_result():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("generate_result")

        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Result Generated Successfully")

        result_view()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- RESULT VIEW (FIXED) ----------------
def result_view():

    show_data("SELECT * FROM result_view")


# ---------------- SIDEBAR BUTTONS ----------------
modules = [

    ("Students", student_module),
    ("Subjects", subject_module),
    ("Exams", exam_module),
    ("Marks", marks_module),
    ("Generate Result", generate_result),
    ("Result View", result_view)

]

for text, command in modules:

    tk.Button(sidebar,
              text=text,
              bg=bg_sidebar,
              fg="white",
              activebackground=accent,
              relief="flat",
              font=("Segoe UI", 11),
              command=command).pack(fill="x", pady=3, ipady=8)


root.mainloop()
