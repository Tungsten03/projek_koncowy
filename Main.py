"""
Main application for requesting air quality data from the GIOS API and saving it to an SQLite database.
The user can analyze the data and view it on a map.

Functionality:

- Populating the database with stations, sensors, and measurements from the GIOS API.
- Analyzing the air quality data in new window using the analyze_full() function.
- Displaying the stations on a map of Poland using the show_stations_on_map() function.

Usage:

- Click the "START" button to populate the database with stations, sensors, and measurements.
- Click the "Mapa stacji" button to display the stations on a map of Poland.
- Click the "Analiza danych" button to analyze the air quality data.
- Click the "WYJŚCIE" button to exit the application.
- Click the 'TESTY' button to run unittest
Author: Kacper Rajewski
"""

from utility import labels as lbl
from peewee import *
import tkinter as tk
from database import db_functions
from analyze_full import analyze_full
from data_filter.localize import show_stations_on_map
from tkinter import messagebox
import unittest




def start_database_full() -> None:
    """
     Start the process of populating the database with stations, sensors, and measurements.

    This function begins the process of populating the database by adding stations, sensors, and measurements
    using the appropriate functions from the `db_functions` module.
    It updates the appearance of the status bar and start button to indicate the progress and completion of the process.

    :return: None
    """
    # Update the start button and status appearence
    status.configure(text=lbl.status_prog, bg='yellow')
    start.configure(bg='yellow')
    root.update()
    # Check the internet connection, update connection flag and add stations to database
    conection_flag = db_functions.db_add_stations()
    # Add sensor to database
    db_functions.db_add_sensors(conection_flag)
    # Add measurements to database
    db_functions.db_add_measurements(conection_flag)
    if conection_flag:
        # If connection is successful update status to updated and disable the button
        start.configure(bg='green', state='disabled')
        status.configure(text=lbl.status_done, bg='green')
        root.update()
    else:
        # If connection fails, update status to historical and disable the button
        start.configure(bg='blue', state='disabled')
        status.configure(text=lbl.status_history, bg='blue', fg='white')
        root.update()
    # Enable buttons
    show_map.configure(state='normal')
    analyze.configure(state='normal')



def quit_app() -> None:
    """
    Quit the application by closing the database connection and destroying the root window.

    This function is called when the application needs to be closed. It closes the database connection by calling the
    `close()` method on the database object. It also terminates the application.

    :return: None
    """
    db = SqliteDatabase('database/stations.db')
    db.close()
    root.destroy()

def run_tests():
    """
    Run unit tests.

    Function runs all unit tests in 'tests' directory using 'unittest' framework.
    After tests it displays a popup window with success/failure message

    :return: None
    """
    # Load the tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    # Run tests
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    # Show result
    if result.wasSuccessful():
        messagebox.showinfo(lbl.test_popup, lbl.test_success)
    else:
        messagebox.showerror(lbl.test_popup, lbl.test_fail)


root = tk.Tk()

root.title(lbl.app_name)
root.geometry('800x400')

# Create labels
app_name = tk.Label(root, text=lbl.app_name)
app_full_name = tk.Label(root, text=lbl.app_full_name)
bar = tk.Label(root, text=140 * '-')
status_start = tk.Label(root, text=lbl.status_start)
status = tk.Label(root, text=lbl.status_start)
show_map_info = tk.Label(root, text=lbl.show_map_info)
analyze_info = tk.Label(root, text=lbl.analyze_info)
instruction = tk.Label(root, text=lbl.start_menu, justify='center')

# Create buttons
start = tk.Button(root, text='START', command=start_database_full, bg='red', width=20)
show_map = tk.Button(root, text=lbl.show_map, command=show_stations_on_map, width=20)
show_map.configure(state='disabled')
analyze = tk.Button(root, text='Analiza danych', command=analyze_full, width=20)
analyze.configure(state='disabled')
kill = tk.Button(root, text='WYJŚCIE', command=quit_app)
testing = tk.Button(root, text='TESTY', command=run_tests)


# Grid layout
app_name.grid(column=0, columnspan=2, row=0)
app_name.configure(anchor='center')

app_full_name.grid(column=0, columnspan=2, row=1)
app_full_name.configure(anchor='center')

bar.grid(column=0, columnspan=2, row=3)
bar.configure(anchor='center')

instruction.grid(column=0, columnspan=2, row=4)
instruction.configure(anchor='center')

start.grid(column=0, row=5, pady=10)
status.grid(column=1, row=5, pady=10)

show_map.grid(column=0, row=6, pady=10)
show_map_info.grid(column=1, row=6, pady=10)

analyze.grid(column=0, row=7, pady=10)
analyze_info.grid(column=1, row=7, pady=10)

testing.grid(column=0, row=8, pady=30)

kill.grid(column=1, row=8, pady=30)
kill.configure(anchor='center')



# Configuire column weights
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

root.mainloop()
