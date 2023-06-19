from tkinter import *


def create_task_name(add_task_window):
    task_name_label = Label(add_task_window, text="Task Name")
    task_name_label.pack()

    task_name_entry = Entry(add_task_window)
    task_name_entry.pack()

    return task_name_entry


def create_description(add_task_window):
    task_description_label = Label(add_task_window, text="Task Description")
    task_description_label.pack()

    task_description_entry = Entry(add_task_window)
    task_description_entry.pack()

    return task_description_entry


def create_task_due_date(add_task_window):
    task_due_date_label = Label(add_task_window, text="Task Due Date")
    task_due_date_label.pack()

    task_due_date_entry = Entry(add_task_window)
    task_due_date_entry.pack()

    return task_due_date_entry


def create_task_priority(add_task_window):
    task_priority_label = Label(add_task_window, text="Task Priority")
    task_priority_label.pack()

    task_priority_entry = Entry(add_task_window)
    task_priority_entry.pack()

    return task_priority_entry


def create_task_status(add_task_window):
    task_status_label = Label(add_task_window, text="Task Status")
    task_status_label.pack()

    task_status_entry = Entry(add_task_window)
    task_status_entry.pack()

    return task_status_entry
