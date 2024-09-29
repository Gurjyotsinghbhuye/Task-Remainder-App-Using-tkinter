import sqlite3

# Create a connection to SQLite database
conn = sqlite3.connect('reminders.db')
cursor = conn.cursor()

# Create a table for reminders
cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT,
                    due_date TEXT,
                    status TEXT
                )''')
conn.commit()


from datetime import datetime

def add_reminder(task_name, due_date):
    cursor.execute("INSERT INTO reminders (task_name, due_date, status) VALUES (?, ?, ?)", 
                   (task_name, due_date, 'Pending'))
    conn.commit()
    print(f'Reminder "{task_name}" added with due date {due_date}.')

# Example usage
add_reminder('Submit project', '2024-09-30 10:00')

def view_pending_reminders():
    cursor.execute("SELECT * FROM reminders WHERE status = 'Pending'")
    reminders = cursor.fetchall()
    
    print("Pending Reminders:")
    for reminder in reminders:
        print(f"ID: {reminder[0]}, Task: {reminder[1]}, Due Date: {reminder[2]}, Status: {reminder[3]}")

# Example usage
view_pending_reminders()


def mark_completed(reminder_id):
    cursor.execute("UPDATE reminders SET status = 'Completed' WHERE id = ?", (reminder_id,))
    conn.commit()
    print(f"Reminder ID {reminder_id} marked as completed.")

# Example usage
mark_completed(1)

def delete_reminder(reminder_id):
    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()
    print(f"Reminder ID {reminder_id} deleted.")

# Example usage
# delete_reminder(1)

import time
from plyer import notification

def check_reminders():
    while True:
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        cursor.execute("SELECT * FROM reminders WHERE due_date <= ? AND status = 'Pending'", (now,))
        due_reminders = cursor.fetchall()
        
        for reminder in due_reminders:
            notification.notify(
                title='Task Reminder',
                message=f"Task: {reminder[1]} is due now!",
                timeout=10
            )
            mark_completed(reminder[0])  # Mark reminder as completed after notifying

        time.sleep(60)  # Check every minute

# Example usage
check_reminders()  # This will run indefinitely to check for reminders

def menu():
    while True:
        print("\nReminder App")
        print("1. View all reminders")
        print("2. View pending reminders")
        print("3. Add a new reminder")
        print("4. Mark a reminder as completed")
        print("5. Delete a reminder")
        print("6. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            cursor.execute("SELECT * FROM reminders")
            reminders = cursor.fetchall()
            print(reminders)
        elif choice == '2':
            view_pending_reminders()
        elif choice == '3':
            task_name = input("Enter task name: ")
            due_date = input("Enter due date (YYYY-MM-DD HH:MM): ")
            add_reminder(task_name, due_date)
        elif choice == '4':
            reminder_id = int(input("Enter reminder ID to mark as completed: "))
            mark_completed(reminder_id)
        elif choice == '5':
            reminder_id = int(input("Enter reminder ID to delete: "))
            delete_reminder(reminder_id)
        elif choice == '6':
            break
        else:
            print("Invalid choice, please try again.")

menu()


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry

def add_task_gui():
    task_name = task_entry.get()
    due_date = date_entry.get()
    hour = hour_var.get()
    minute = minute_var.get()
    
    # Combine date and time into a single string
    due_date_time = f"{due_date} {hour}:{minute}"
    
    add_reminder(task_name, due_date_time)
    messagebox.showinfo("Success", f"Task '{task_name}' added with due date {due_date_time}!")
    task_entry.delete(0, tk.END)

app = tk.Tk()
app.title('Task Reminder App')

tk.Label(app, text='Task').grid(row=0)
tk.Label(app, text='Due Date').grid(row=1)
tk.Label(app, text='Hour (HH)').grid(row=2)
tk.Label(app, text='Minute (MM)').grid(row=3)

task_entry = tk.Entry(app)
date_entry = DateEntry(app, date_pattern='yyyy-mm-dd')  # Calendar widget

# Variables for hour and minute
hour_var = tk.StringVar()
minute_var = tk.StringVar()

# Hour dropdown (0-23)
hour_dropdown = ttk.Combobox(app, textvariable=hour_var, values=[f"{i:02}" for i in range(24)], width=5)
hour_dropdown.grid(row=2, column=1)

# Minute dropdown (0-59)
minute_dropdown = ttk.Combobox(app, textvariable=minute_var, values=[f"{i:02}" for i in range(60)], width=5)
minute_dropdown.grid(row=3, column=1)

# Set default values
hour_var.set("00")
minute_var.set("00")

task_entry.grid(row=0, column=1)
date_entry.grid(row=1, column=1)

tk.Button(app, text='Add Task', command=add_task_gui).grid(row=4, column=1)

app.mainloop()
