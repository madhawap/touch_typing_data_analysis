import tkinter as tk
from tkinter import ttk
from sys import platform
from tkcalendar import DateEntry
import csv
import os.path

if platform == "darwin":
    from tkmacosx import Button #This is no longer used.
elif platform == "win32":
    from winreg import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # ################ Creates the main window #########################
        self.geometry('510x320')
        self.title('My Touch Typing Progress Analyser')
        self.style = ttk.Style()

        # ####################### GUI Design #######################
        ttk.Label(self, text='Enter Practice Data', style="Normal.Label", font=('arial', 15, 'bold')).place(x=25, y=10)

        # Date
        ttk.Label(self, text='Date', style="Normal.Label", font=('arial', 12, 'normal')).place(x=38, y=40)
        self.date_entry = DateEntry(self, width=10, year=2022)
        self.date_entry.place(x=38, y=65)

        # WPM
        ttk.Label(self, text='WPM', style="Normal.Label", font=('arial', 12, 'normal')).place(x=170, y=40)
        self.wpm_value = tk.Entry(self, width=3, bg='grey')
        self.wpm_value.place(x=170, y=65)

        # Attempt
        ttk.Label(self, text='Attempt', style="Normal.Label", font=('arial', 12, 'normal')).place(x=230, y=40)
        self.attempt_count = tk.Entry(self, width=3, bg='grey')
        self.attempt_count.place(x=230, y=65)

        # Accuracy
        ttk.Label(self, text='Accuracy', style="Normal.Label", font=('arial', 12, 'normal')).place(x=292, y=41)
        self.accuracy_value = tk.Entry(self, width=6, bg='grey')
        self.accuracy_value.place(x=290, y=65)

        # Add Button
        self.add_btn = ttk.Button(self, text="Add", command=self.add_new_data)
        self.add_btn.place(x=370, y=65)

        self.waring_msg = ttk.Label(self, text='', style="Warning.Label", font=('arial', 12, 'normal'))
        # waring_msg.place(x=25, y=100)

        self.success_msg = ttk.Label(self, text='', style="Success.Label", font=('arial', 12, 'normal'))
        # success_msg.place(x=25, y=100)

        # PROGRESS ANALYSIS
        ttk.Label(self, text='Progress Analysis', style="Normal.Label", font=('arial', 15, 'bold')).place(x=25, y=130)
        self.show_analysis = ttk.Button(self, text="show", command=self.show_analysis_data)
        if platform == "darwin":
            self.show_analysis.place(x=180, y=130)
        elif platform == "win32":
            self.show_analysis.place(x=210, y=130)

        ttk.Label(self, text='Average Accuracy:', style="Normal.Label", font=('arial', 12, 'normal')).place(x=38, y=170)

        ttk.Label(self, text='Average WPM:', style="Normal.Label", font=('arial', 12, 'normal')).place(x=38, y=200)

        ttk.Label(self, text='Total Time Spent:', style="Normal.Label", font=('arial', 12, 'normal')).place(x=38, y=230)

        ttk.Label(self, text='Avg Time Per Day:', style="Normal.Label", font=('arial', 12, 'normal')).place(x=38, y=260)

        self.avg_accuracy_val = ttk.Label(self, text='', style="Normal.Label", font=('arial', 12, 'normal'))
        self.avg_wpm_val = ttk.Label(self, text='', style="Normal.Label", font=('arial', 12, 'normal'))
        self.time_spent_val_display = ttk.Label(self, text='', style="Normal.Label", font=('arial', 12, 'normal'))
        self.time_spent_per_day_val_display = ttk.Label(self, text='', style="Normal.Label",
                                                        font=('arial', 12, 'normal'))

        if platform == "darwin":
            self.avg_accuracy_val.place(x=160, y=170)
            self.avg_wpm_val.place(x=160, y=200)
            self.time_spent_val_display.place(x=160, y=230)
            self.time_spent_per_day_val_display.place(x=160, y=260)
            self.best_wpm_canvas = tk.Canvas(self, width=98, height=148)
            self.best_wpm_canvas.create_rectangle(0, 0, 98, 148, fill='#444444', outline='#444444')
            self.best_wpm_canvas.place(x=330, y=130)

            tk.Label(self, text='Best WPM', bg='#444444', fg='white', font=('arial', 14, 'normal')).place(x=345,
                                                                                                            y=141)

            self.best_wpm = tk.Label(self, text='00', bg='#444444', fg='white', font=('arial', 42, 'normal'))
            self.best_wpm.place(x=355, y=161)

            tk.Label(self, text='on', bg='#444444', fg='white', font=('arial', 14, 'normal')).place(x=374, y=215)

            self.best_wpm_date = tk.Label(self, text='00-00-0000', bg='#444444', fg='white',
                                          font=('arial', 14, 'normal'))
            self.best_wpm_date.place(x=345, y=246)
        elif platform == "win32":
            self.avg_accuracy_val.place(x=180, y=170)
            self.avg_wpm_val.place(x=180, y=200)
            self.time_spent_val_display.place(x=180, y=230)
            self.time_spent_per_day_val_display.place(x=180, y=260)
            self.best_wpm_canvas = tk.Canvas(self, width=110, height=148)
            self.best_wpm_canvas.create_rectangle(0, 0, 110, 148, fill='black', outline='black')
            self.best_wpm_canvas.place(x=330, y=138)

            tk.Label(self, text='Best WPM', bg='black', fg='white', font=('arial', 12, 'normal')).place(x=345, y=149)

            self.best_wpm = tk.Label(self, text='00', bg='black', fg='white', font=('arial', 40, 'normal'))
            self.best_wpm.place(x=355, y=173)

            tk.Label(self, text='on', bg='black', fg='white', font=('arial', 12, 'normal')).place(x=374, y=227)

            self.best_wpm_date = tk.Label(self, text='00-00-0000', bg='black', fg='white', font=('arial', 12, 'normal'))
            self.best_wpm_date.place(x=345, y=255)

    def create_new_data_file(self):
        # Creates new and empty data file if there is no data file
        if not os.path.isfile(FILE_NAME):
            header = 'day', 'speed', 'attempt', 'accuracy'
            with open(FILE_NAME, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)

    # ################ Functionalities #########################

    def add_new_data(self):
        """
        :param data: This is a tuple (Date, WPM, Accuracy)
        :return: None
        """
        date = self.date_entry.get_date().strftime("%d-%m-%Y")
        try:
            # Read input values in the text fields
            wpm = int(self.wpm_value.get())
            attempt = int(self.attempt_count.get())
            accuracy = float(self.accuracy_value.get())
            data = (date, wpm, attempt, accuracy)

            # Clear the input fields after extracting values
            self.wpm_value.delete(0, tk.END)
            self.attempt_count.delete(0, tk.END)
            self.accuracy_value.delete(0, tk.END)

            with open(FILE_NAME, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)

            # Remove warning message label
            self.waring_msg.place_forget()
            # Display success message
            self.success_msg.config(text="DATA ADDED SUCCESSFULLY.")
            self.success_msg.place(x=25, y=100)
        except ValueError:
            self.success_msg.place_forget()
            self.waring_msg.config(text="WARNING!! ENTER VALID PRACTICE DATA.")
            self.waring_msg.place(x=25, y=100)

    def analyse_typing_progress_data(self):
        """
        Read the CSV File and Return Calculated data as mentioned below.
        :return: Avg accuracy, Avg WPM, Total Time, Time Per Day, Max WPM, Max WPM Date
        """
        # This function can be improve with a selection of proper data structure. E.g. Pandas or numpy 2d arrays
        records = []
        typing_speed = []
        days = []
        accuracy_list = []
        set_of_days = set()
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
                    # accuracy in the csv. This will not be a problem to new users.
                    accuracy_list.append(float(record.split(",")[3]))

        if len(accuracy_list) != 0 and len(typing_speed) != 0:
            avg_accuracy = sum(accuracy_list) / len(accuracy_list)
            avg_wpm = sum(typing_speed) / len(typing_speed)
            max_wpm = max(typing_speed)
            max_wpm_date = days[typing_speed.index(max_wpm)]
            time_spent_per_day = time_spent / len(set_of_days)

        return avg_accuracy, avg_wpm, time_spent, time_spent_per_day, max_wpm, max_wpm_date

    # def cal_attempts_per_day(days):
    #     attempts_per_day = {i:days.count(i) for i in days}

    def show_analysis_data(self):
        """
        This function will set the values generated from the analyse_typing_progress_data() function to GUI labels
        accordingly.
        :return: None
        """
        # Clear any warning or success messages displayed on the GUI
        self.waring_msg.place_forget()
        self.success_msg.place_forget()

        # Set the analysis data to relevant GUI labels
        self.avg_accuracy_val.config(text=f'{self.analyse_typing_progress_data()[0]:.4f}')
        self.avg_wpm_val.config(text=f'{self.analyse_typing_progress_data()[1]:.4f}')
        self.time_spent_val_display.config(text=f'{self.analyse_typing_progress_data()[2]} minutes')
        self.time_spent_per_day_val_display.config(text=f'{self.analyse_typing_progress_data()[3]:.4f} minutes')
        self.best_wpm.config(text=f'{self.analyse_typing_progress_data()[4]}')
        self.best_wpm_date.config(text=f'{self.analyse_typing_progress_data()[5]}')

    def change_gui_style(self):
        """
        This functions will change the GUI styles based on the OS system theme selection.
        :limitation: Currently only works with Windows. macOS will by default adjust the GUI to the OS theme. This needs to
        be further tested.
        :return: None
        """
        if platform == "win32":
            self.style.configure("Normal.Label", foreground="black", background="white")
            registry = ConnectRegistry(None, HKEY_CURRENT_USER)
            key = OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
            mode = QueryValueEx(key, "AppsUseLightTheme")
            self.config(bg="white" if mode[0] else "black")
            self.style.configure("Normal.Label", foreground="black" if mode[0] else "white",
                                 background="white" if mode[0] else "black")
            self.style.configure("Warning.Label", foreground="red" if mode[0] else "red",
                                 background="white" if mode[0] else "black")
            # label.config(text="Light Mode on" if mode[0] else "Dark Mode on",
            #              bg="white" if mode[0] else "black",
            #              fg="black" if mode[0] else "white")
            self.after(100, self.change_gui_style)
        elif platform == "darwin":
            self.style.configure("Normal.Label")
            self.style.configure("Warning.Label", foreground="red")
            self.style.configure("Success.Label", foreground="green")


# TODO: Add progress graphs and display on the GUI (Growth Graph WPM and Accuracy over the time)
# TODO: Add logo to the GUI
# TODO: There is a mix of ttk and tk. This need to be fixed.

if __name__ == '__main__':
    FILE_NAME = 'touchTypingProgress.csv'

    app = App()
    # This will set the GUI styles according the OS selected theme (Only on Windows OS).
    app.change_gui_style()
    app.mainloop()
