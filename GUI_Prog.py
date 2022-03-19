from tkinter import *
from sys import platform
from tkcalendar import Calendar, DateEntry
import csv

if platform == "darwin":
    from tkmacosx import Button


def add_new_data():
    """
    :param data: This is a tuple (Date, WPM, Accuracy)
    :return: None
    """
    date = date_entry.get_date().strftime("%d-%m-%Y")
    try:
        wpm = int(wpm_value.get())
        attempt = int(attempt_count.get())
        accuracy = float(accuracy_value.get())
        data = (date, wpm, attempt, accuracy)
        wpm_value.delete(0, END)
        attempt_count.delete(0, END)
        accuracy_value.delete(0, END)
        with open('touchTypingProgress.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        waring_msg.config(text="DATA ADDED")
    except ValueError:
        waring_msg.config(text="WARNING!! ENTER VALID PRACTICE DATA. All values should be numeric")


def analyse_data():
    records = []
    typing_speed = []
    days = []
    accuracy_list = []

    with open("touchTypingProgress.csv", "r") as file:
        for line in file:
            records.append(line.strip())

    for record in records[1:]:
        if record != '':
            print(record)
            typing_speed.append(int(record.split(",")[1]))
            days.append(record.split(",")[0])
            if record.split(",")[3] != '':
                accuracy_list.append(float(record.split(",")[3]))

    return sum(accuracy_list) / len(accuracy_list), sum(typing_speed) / len(typing_speed), len(records)


def show_analysis_data():
    waring_msg.config(text='')
    avg_accuracy = analyse_data()[0]
    avg_wpm = analyse_data()[1]
    time_spent = analyse_data()[2]
    avg_accuracy_val.config(text=f'{avg_accuracy}')
    avg_wpm_val.config(text=f'{avg_wpm}')
    time_spent_val_display.config(text=f'{time_spent} minutes')


root = Tk()

# This is the section of code which creates the main window
root.geometry('520x300')
# root.configure(background='#F0F8FF')
root.title('My Touch Typing Progress Analyser')

Label(root, text='Enter Practice Data', font=('arial', 15, 'bold')).place(x=25, y=10)

# Date
Label(root, text='Date', font=('arial', 12, 'normal')).place(x=38, y=40)
date_entry = DateEntry(root, width=10, year=2022)
date_entry.place(x=38, y=65)

# WPM
Label(root, text='WPM', font=('arial', 12, 'normal')).place(x=170, y=40)
wpm_value = Entry(root, width=3, bg='grey')
wpm_value.place(x=170, y=65)

# Attempt
Label(root, text='Attempt', font=('arial', 12, 'normal')).place(x=230, y=40)
attempt_count = Entry(root, width=3, bg='grey')
attempt_count.place(x=230, y=65)

# Accuracy
Label(root, text='Accuracy', font=('arial', 12, 'normal')).place(x=300, y=41)
accuracy_value = Entry(root, width=6, bg='grey')
accuracy_value.place(x=300, y=65)

# Add Button
add_btn = Button(root, text="Add", command=add_new_data)
add_btn.place(x=400, y=65)

waring_msg = Label(root, text='', fg='red', font=('arial', 12, 'normal'))
waring_msg.place(x=25, y=100)

# PROGRESS ANALYSIS
Label(root, text='Progress Analysis', font=('arial', 15, 'bold')).place(x=25, y=130)
show_analysis = Button(root, text="show", command=show_analysis_data)
show_analysis.place(x=180, y=130)

Label(root, text='Average Accuracy:', font=('arial', 12, 'normal')).place(x=38, y=170)

Label(root, text='Average WPM:', font=('arial', 12, 'normal')).place(x=38, y=200)

Label(root, text='Total Time Spent:', font=('arial', 12, 'normal')).place(x=38, y=230)

avg_accuracy_val = Label(root, text='', font=('arial', 12, 'normal'))
avg_accuracy_val.place(x=160, y=170)

avg_wpm_val = Label(root, text='', font=('arial', 12, 'normal'))
avg_wpm_val.place(x=160, y=200)

time_spent_val_display = Label(root, text='', font=('arial', 12, 'normal'))
time_spent_val_display.place(x=160, y=230)

root.mainloop()

# TODO: Add progress graphs and display on the GUI (Growth Graph WPM and Accuracy over the time)
# TODO: Add logo to the GUI
