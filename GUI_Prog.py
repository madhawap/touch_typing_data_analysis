from tkinter import *
from tkinter import ttk
from sys import platform
from tkcalendar import Calendar, DateEntry
import csv
import os.path

if platform == "darwin":
    from tkmacosx import Button
elif platform == "winn32":
    from winreg import *

FILE_NAME = 'touchTypingProgress.csv'

if not os.path.isfile(FILE_NAME):
    # open(FILE_NAME, 'a').close()
    header = 'day', 'speed', 'attempt', 'accuracy'
    with open(FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

# ################ Creates the main window #########################
root = Tk()
root.geometry('510x320')
# root.configure(background='#F0F8FF')
root.title('My Touch Typing Progress Analyser')
style = ttk.Style()


# ################ Functionalities #########################

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
        waring_msg.place_forget()
        success_msg.config(text="DATA ADDED SUCCESSFULLY.")
        success_msg.place(x=25, y=100)
    except ValueError:
        success_msg.place_forget()
        waring_msg.config(text="WARNING!! ENTER VALID PRACTICE DATA.")
        waring_msg.place(x=25, y=100)

def analyse_data():
    """
    Read the CSV File and Return Calculated data as mentioned below.
    :return: Avg accurcy, Avg WPM, Total Time, Time Per Day, Max WPM, Max WPM Date
    """
    records = []
    typing_speed = []
    days = []
    set_of_days = set()
    accuracy_list = []
    avg_accuracy, avg_wpm, time_spent, time_spent_per_day, max_wpm, max_wpm_date = 0, 0, 0, 0, 0, 0

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
        max_wpm = max(typing_speed)
        max_wpm_date = days[typing_speed.index(max_wpm)]
        time_spent_per_day = time_spent / len(set_of_days)

    return avg_accuracy, avg_wpm, time_spent, time_spent_per_day, max_wpm, max_wpm_date
    # return sum(accuracy_list) / len(accuracy_list), sum(typing_speed) / len(typing_speed), time, time/len(set_of_days)


# def cal_attempts_per_day(days):
#     attempts_per_day = {i:days.count(i) for i in days}

def show_analysis_data():
    # waring_msg.config(text='')
    waring_msg.place_forget()
    success_msg.place_forget()
    avg_accuracy = analyse_data()[0]
    avg_wpm = analyse_data()[1]
    time_spent = analyse_data()[2]
    time_spent_per_day = analyse_data()[3]
    avg_accuracy_val.config(text=f'{avg_accuracy:.4f}')
    avg_wpm_val.config(text=f'{avg_wpm:.4f}')
    time_spent_val_display.config(text=f'{time_spent} minutes')
    time_spent_per_day_val_display.config(text=f'{time_spent_per_day:.4f} minutes')
    best_wpm.config(text=f'{analyse_data()[4]}')
    best_wpm_date.config(text=f'{analyse_data()[5]}')


def monitor_changes():
    if platform == "winn32":
        style.configure("Normal.Label", foreground="black", background="white")
        registry = ConnectRegistry(None, HKEY_CURRENT_USER)
        key = OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
        mode = QueryValueEx(key, "AppsUseLightTheme")
        root.config(bg="white" if mode[0] else "black")
        style.configure("Normal.Label", foreground="black" if mode[0] else "white",
                        background="white" if mode[0] else "black")
        style.configure("Warning.Label", foreground="red" if mode[0] else "red",
                        background="white" if mode[0] else "black")
        # label.config(text="Light Mode on" if mode[0] else "Dark Mode on",
        #              bg="white" if mode[0] else "black",
        #              fg="black" if mode[0] else "white")
        root.after(100, monitor_changes)
    elif platform == "darwin":
        style.configure("Normal.Label")
        style.configure("Warning.Label", foreground="red")
        style.configure("Success.Label", foreground="green")


monitor_changes()

# ####################### GUI Design #######################

ttk.Label(root, text='Enter Practice Data', style="Normal.Label", font=('arial', 15, 'bold')).place(x=25, y=10)

# Date
ttk.Label(root, text='Date', style="BW.TLabel", font=('arial', 12, 'normal')).place(x=38, y=40)
date_entry = DateEntry(root, width=10, year=2022)
date_entry.place(x=38, y=65)

# WPM
ttk.Label(root, text='WPM', style="Normal.Label", font=('arial', 12, 'normal')).place(x=170, y=40)
wpm_value = Entry(root, width=3, bg='grey')
wpm_value.place(x=170, y=65)

# Attempt
ttk.Label(root, text='Attempt', style="Normal.Label", font=('arial', 12, 'normal')).place(x=230, y=40)
attempt_count = Entry(root, width=3, bg='grey')
attempt_count.place(x=230, y=65)

# Accuracy
ttk.Label(root, text='Accuracy', style="Normal.Label", font=('arial', 12, 'normal')).place(x=292, y=41)
accuracy_value = Entry(root, width=6, bg='grey')
accuracy_value.place(x=290, y=65)

# Add Button
add_btn = Button(root, text="Add", command=add_new_data)
add_btn.place(x=370, y=65)

waring_msg = ttk.Label(root, text='', style="Warning.Label", font=('arial', 12, 'normal'))
# waring_msg.place(x=25, y=100)

success_msg = ttk.Label(root, text='', style="Success.Label", font=('arial', 12, 'normal'))
# success_msg.place(x=25, y=100)

# PROGRESS ANALYSIS
ttk.Label(root, text='Progress Analysis', style="Normal.Label", font=('arial', 15, 'bold')).place(x=25, y=130)
show_analysis = Button(root, text="show", command=show_analysis_data)
if platform == "darwin":
    show_analysis.place(x=180, y=130)
elif platform == "win32":
    show_analysis.place(x=210, y=130)

ttk.Label(root, text='Average Accuracy:', style="Normal.Label", font=('arial', 12, 'normal')).place(x=38, y=170)

ttk.Label(root, text='Average WPM:', style="Normal.Label", font=('arial', 12, 'normal')).place(x=38, y=200)

ttk.Label(root, text='Total Time Spent:', style="Normal.Label", font=('arial', 12, 'normal')).place(x=38, y=230)

ttk.Label(root, text='Avg Time Per Day:', style="Normal.Label", font=('arial', 12, 'normal')).place(x=38, y=260)

avg_accuracy_val = ttk.Label(root, text='', style="Normal.Label", font=('arial', 12, 'normal'))
avg_wpm_val = ttk.Label(root, text='', style="Normal.Label", font=('arial', 12, 'normal'))
time_spent_val_display = ttk.Label(root, text='', style="Normal.Label", font=('arial', 12, 'normal'))
time_spent_per_day_val_display = ttk.Label(root, text='', style="Normal.Label", font=('arial', 12, 'normal'))

if platform == "darwin":
    avg_accuracy_val.place(x=160, y=170)
    avg_wpm_val.place(x=160, y=200)
    time_spent_val_display.place(x=160, y=230)
    time_spent_per_day_val_display.place(x=160, y=260)
    best_wpm_canvas = Canvas(root, width=98, height=148)
    best_wpm_canvas.create_rectangle(0, 0, 98, 148, fill='#444444', outline='#444444')
    best_wpm_canvas.place(x=330, y=130)

    Label(root, text='Best WPM', bg='#444444', fg='white', font=('arial', 14, 'normal')).place(x=345, y=141)

    best_wpm = Label(root, text='00', bg='#444444', fg='white', font=('arial', 42, 'normal'))
    best_wpm.place(x=355, y=161)

    Label(root, text='on', bg='#444444', fg='white', font=('arial', 14, 'normal')).place(x=374, y=215)

    best_wpm_date = Label(root, text='00-00-0000', bg='#444444', fg='white', font=('arial', 14, 'normal'))
    best_wpm_date.place(x=345, y=246)
elif platform == "win32":
    avg_accuracy_val.place(x=180, y=170)
    avg_wpm_val.place(x=180, y=200)
    time_spent_val_display.place(x=180, y=230)
    time_spent_per_day_val_display.place(x=180, y=260)
    best_wpm_canvas = Canvas(root, width=110, height=148)
    best_wpm_canvas.create_rectangle(0, 0, 110, 148, fill='black', outline='black')
    best_wpm_canvas.place(x=330, y=138)

    Label(root, text='Best WPM', bg='black', fg='white', font=('arial', 12, 'normal')).place(x=345, y=149)

    best_wpm = Label(root, text='00', bg='black', fg='white', font=('arial', 40, 'normal'))
    best_wpm.place(x=355, y=173)

    Label(root, text='on', bg='black', fg='white', font=('arial', 12, 'normal')).place(x=374, y=227)

    best_wpm_date = Label(root, text='00-00-0000', bg='black', fg='white', font=('arial', 12, 'normal'))
    best_wpm_date.place(x=345, y=255)

root.mainloop()

# TODO: Add progress graphs and display on the GUI (Growth Graph WPM and Accuracy over the time)
# TODO: Add logo to the GUI
