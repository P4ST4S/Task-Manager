from tkinter import *
from tkinter import messagebox
from datetime import datetime

from database import connect_db, get_tasks


def create_gui():
    window = Tk()
    window.title("Task Manager")

    conn = connect_db()

    tasks = get_tasks(conn)

    task_list = Listbox(window)
    task_list.pack()

    for task in tasks:
        task_list.insert(END, task)

    add_task_button = Button(
        window, text="Add Task", command=lambda: open_add_task_dialog(window, conn, task_list))
    add_task_button.pack()

    window.mainloop()
    conn.close()


def open_add_task_dialog(window, conn, tasks_list):
    add_task_window = Toplevel(window)
    add_task_window.title("Add Task")

    task_name_label = Label(add_task_window, text="Task Name")
    task_name_label.pack()

    task_name_entry = Entry(add_task_window)
    task_name_entry.pack()

    task_description_label = Label(add_task_window, text="Task Description")
    task_description_label.pack()

    task_description_entry = Entry(add_task_window)
    task_description_entry.pack()

    task_due_date_label = Label(add_task_window, text="Task Due Date")
    task_due_date_label.pack()

    task_due_date_entry = Entry(add_task_window)
    task_due_date_entry.pack()

    task_priority_label = Label(add_task_window, text="Task Priority")
    task_priority_label.pack()

    task_priority_entry = Entry(add_task_window)
    task_priority_entry.pack()

    task_status_label = Label(add_task_window, text="Task Status")
    task_status_label.pack()

    task_status_entry = Entry(add_task_window)
    task_status_entry.pack()

    add_button = Button(add_task_window, text="Add Task", command=lambda: add_task(
        conn,
        tasks_list,
        add_task_window,
        task_name_entry.get(),
        task_description_entry.get(),
        task_due_date_entry.get(),
        task_priority_entry.get(),
        task_status_entry.get()
    ))
    add_button.pack()


def verify_date(date):
    try:
        datetime.strptime(date, "%d/%m/%Y")
        return True
    except ValueError:
        messagebox.showerror(
            "Error", "Incorrect data format, should be Day/Month/Year")
        return False


def add_task(conn, tasks_list, add_task_window, name, description, due_date, priority, status):
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

        if messagebox.showinfo("Success", "Task added successfully"):
            add_task_window.destroy()
            update_tasks_list(tasks_list, conn)


def update_tasks_list(task_list, conn):
    task_list.delete(0, END)

    tasks = get_tasks(conn)

    for task in tasks:
        task_list.insert(END, task)
