from tkinter import *
from tkinter import messagebox
from datetime import datetime

from database import connect_db, get_tasks
from label import *


def create_gui():
    window = Tk()
    window.title("Task Manager")

    conn = connect_db()

    tasks = get_tasks(conn)

    task_list = Listbox(window, selectmode=SINGLE)
    task_list.pack()

    task_list.bind("<<ListboxSelect>>", lambda event: show_task_details(
        window, tasks[task_list.curselection()[0]]))

    for task in tasks:
        task_list.insert(END, task[1])

    add_task_button = Button(
        window, text="Add Task", command=lambda: open_add_task_dialog(window, conn, task_list))
    add_task_button.pack()

    window.mainloop()
    conn.close()


def show_task_details(window, task):
    task_details_window = Toplevel(window)
    task_details_window.title(task[1])

    for i, detail in enumerate(task):
        label = Label(task_details_window, text=detail)
        label.grid(row=i, column=0)

    task_details_window.mainloop()


def open_add_task_dialog(window, conn, tasks_list):
    add_task_window = Toplevel(window)
    add_task_window.title("Add Task")

    task_name_entry = create_task_name(add_task_window)
    task_description_entry = create_description(add_task_window)
    task_due_date_entry = create_task_due_date(add_task_window)
    task_priority_entry = create_task_priority(add_task_window)
    task_status_entry = create_task_status(add_task_window)

    add_button = Button(add_task_window, text="Add Task", command=lambda: check_and_add_task(
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


def check_and_add_task(conn, tasks_list, add_task_window, name, description, due_date, priority, status):
    if not all([name, description, due_date, priority, status]):
        messagebox.showerror("Error", "All fields are required")
        return

    if not verify_date(due_date):
        return

    add_task(conn, tasks_list, add_task_window, name,
             description, due_date, priority, status)


def add_task(conn, tasks_list, add_task_window, name, description, due_date, priority, status):
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
