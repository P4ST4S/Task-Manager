from tkinter import *
from tkinter import messagebox
from datetime import datetime

from database import connect_db


def create_gui():

    conn = connect_db()

    window = Tk()
    window.title("Task Manager")

    task_name_label = Label(window, text="Task Name")
    task_name_label.pack()

    task_name_entry = Entry(window)
    task_name_entry.pack()

    task_description_label = Label(window, text="Task Description")
    task_description_label.pack()

    task_description_entry = Entry(window)
    task_description_entry.pack()

    task_due_date_label = Label(window, text="Task Due Date")
    task_due_date_label.pack()

    task_due_date_entry = Entry(window)
    task_due_date_entry.pack()

    task_priority_label = Label(window, text="Task Priority")
    task_priority_label.pack()

    task_priority_entry = Entry(window)
    task_priority_entry.pack()

    task_status_label = Label(window, text="Task Status")
    task_status_label.pack()

    task_status_entry = Entry(window)
    task_status_entry.pack()

    add_button = Button(window, text="Add Task", command=lambda: add_task(
        conn,
        task_name_entry.get(),
        task_description_entry.get(),
        task_due_date_entry.get(),
        task_priority_entry.get(),
        task_status_entry.get()
    ))
    add_button.pack()

    window.mainloop()

    conn.close()


def verify_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        messagebox.showerror(
            "Error", "Incorrect data format, should be YYYY-MM-DD")
        return False


def add_task(conn, name, description, due_date, priority, status):
    if not all([name, description, due_date, priority, status]):
        messagebox.showerror("Error", "All fields are required")
        return

    if not verify_date(due_date):
        return

    with conn:
        c = conn.cursor()

        c.execute("""
        INSERT INTO tasks (name, description, due_date, priority, status)
        VALUES (?, ?, ?, ?, ?)
        """, (name, description, due_date, priority, status))

        conn.commit()

        messagebox.showinfo("Success", "Task added successfully")
