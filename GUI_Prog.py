from tkinter import *
from sys import platform
from tkcalendar import Calendar, DateEntry
import csv
import os.path

if platform == "darwin":
    from tkmacosx import Button

FILE_NAME = 'touchTypingProgress.csv'

if not os.path.isfile(FILE_NAME):
    # open(FILE_NAME, 'a').close()
    header = 'day', 'speed', 'attempt', 'accuracy'
    with open(FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)


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
        with open(FILE_NAME, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        waring_msg.config(text="DATA ADDED")
    except ValueError:
        waring_msg.config(text="WARNING!! ENTER VALID PRACTICE DATA. All values should be numeric")


def analyse_data():
    """
    Read the CSV File and Return Calculated data as mentioned below.
    :return: Avg accurcy, Avg WPM, Total Time, Time Per Day
    """
    records = []
    typing_speed = []
    days = []
    set_of_days = set()
    accuracy_list = []
    avg_accuracy, avg_wpm, time_spent, time_spent_per_day = 0, 0, 0, 0

    with open(FILE_NAME, "r") as file:
        for line in file:
            records.append(line.strip())

    for record in records[1:]:
        if record != '':
            time_spent += 1
            typing_speed.append(int(record.split(",")[1]))
            days.append(record.split(",")[0])
            set_of_days = set(days)
            if record.split(",")[3] != '':  # I did not record accuracy at the beginning so there are data without
                # accuracy
                accuracy_list.append(float(record.split(",")[3]))

    if len(accuracy_list) != 0 and len(typing_speed) != 0:
        avg_accuracy = sum(accuracy_list) / len(accuracy_list)
        avg_wpm = sum(typing_speed) / len(typing_speed)
        time_spent_per_day = time_spent / len(set_of_days)

    return avg_accuracy, avg_wpm, time_spent, time_spent_per_day
    # return sum(accuracy_list) / len(accuracy_list), sum(typing_speed) / len(typing_speed), time, time/len(set_of_days)


# def cal_attempts_per_day(days):
#     attempts_per_day = {i:days.count(i) for i in days}

def show_analysis_data():
    waring_msg.config(text='')
    avg_accuracy = analyse_data()[0]
    avg_wpm = analyse_data()[1]
    time_spent = analyse_data()[2]
    time_spent_per_day = analyse_data()[3]
    avg_accuracy_val.config(text=f'{avg_accuracy:.4f}')
    avg_wpm_val.config(text=f'{avg_wpm:.4f}')
    time_spent_val_display.config(text=f'{time_spent} minutes')
    time_spent_per_day_val_display.config(text=f'{time_spent_per_day:.4f} minutes')


# ####################### GUI Design #######################

root = Tk()

# This is the section of code which creates the main window
root.geometry('520x320')
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
if platform == "darwin":
    show_analysis.place(x=180, y=130)
elif platform == "win32":
    show_analysis.place(x=210, y=130)

Label(root, text='Average Accuracy:', font=('arial', 12, 'normal')).place(x=38, y=170)

Label(root, text='Average WPM:', font=('arial', 12, 'normal')).place(x=38, y=200)

Label(root, text='Total Time Spent:', font=('arial', 12, 'normal')).place(x=38, y=230)

Label(root, text='Avg Time Per Day:', font=('arial', 12, 'normal')).place(x=38, y=260)

avg_accuracy_val = Label(root, text='', font=('arial', 12, 'normal'))
avg_wpm_val = Label(root, text='', font=('arial', 12, 'normal'))
time_spent_val_display = Label(root, text='', font=('arial', 12, 'normal'))
time_spent_per_day_val_display = Label(root, text='', font=('arial', 12, 'normal'))

if platform == "darwin":
    avg_accuracy_val.place(x=160, y=170)
    avg_wpm_val.place(x=160, y=200)
    time_spent_val_display.place(x=160, y=230)
    time_spent_per_day_val_display.place(x=160, y=260)
elif platform == "win32":
    avg_accuracy_val.place(x=180, y=170)
    avg_wpm_val.place(x=180, y=200)
    time_spent_val_display.place(x=180, y=230)
    time_spent_per_day_val_display.place(x=180, y=260)

root.mainloop()

# TODO: Add progress graphs and display on the GUI (Growth Graph WPM and Accuracy over the time)
# TODO: Add logo to the GUI
# TODO: Add fastest of all time
