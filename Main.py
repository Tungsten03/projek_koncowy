"""----------------------------------KRAQEN-----------------------------------
-------------------------Kacper Rajewski Air Quality Environment-----------------------
"""

# Application requests air quality data from GIOS Api
# Requested data is saved in sqlite3 database
# User can analyze data blablablabla

from utility import labels as lbl
from peewee import *



import tkinter as tk
from tkinter import ttk

from database import db_functions
from analyze_full import analyze_full



def start_database_full():
    status_bar.configure(text=lbl.status_bar_prog, bg='yellow')
    start.configure(bg='yellow')
    root.update()
    conection_flag = db_functions.db_add_stations()
    db_functions.db_add_sensors(conection_flag)
    db_functions.db_add_measurements(conection_flag)
    if conection_flag == True:
        start.configure(bg='green', state='disabled')
        status_bar.configure(text=lbl.status_bar_done, bg='green')
        root.update()
    else:
        start.configure(bg='blue', state='disabled')
        status_bar.configure(text=lbl.status_bar_history, bg='blue', fg='white')
        root.update()
def quit():
    db = SqliteDatabase('database/stations.db')
    db.close()
    root.destroy()



root = tk.Tk()


root.title(lbl.app_name)
root.geometry('800x400')




app_name = tk.Label(root, text=lbl.app_name)
app_full_name = tk.Label(root, text=lbl.app_full_name)
bar = tk.Label(root, text=140*'-')
status_bar_start = tk.Label(root, text=lbl.status_bar_start)
status_bar = tk.Label(root, text=lbl.status_bar_start)
show_map_info = tk.Label(root, text=lbl.show_map_info)
analyze_info = tk.Label(root, text=lbl.analyze_info)

instruction = tk.Label(root, text=lbl.start_menu, justify="center")

start = tk.Button(root, text='START', command=start_database_full, bg='red', width=20)
show_map = tk.Button(root, text=lbl.show_map, width=20)
analyze = tk.Button(root, text='Analiza danych', command=analyze_full, width=20)

kill = tk.Button(root, text='WYJŚCIE', command=quit)


app_name.grid(column=0, columnspan=2, row=0)
app_name.configure(anchor='center')
app_full_name.grid(column=0, columnspan=2, row=1)
app_full_name.configure(anchor='center')
bar.grid(column=0, columnspan=2, row=3)
bar.configure(anchor='center')
instruction.grid(column=0, columnspan=2, row=4)
instruction.configure(anchor='center')
start.grid(column=0, row=5, pady=10)
status_bar.grid(column=1, row=5, pady=10)
show_map.grid(column=0, row=6, pady=10)
show_map_info.grid(column=1, row=6, pady=10)
analyze.grid(column=0, row=7, pady=10)
analyze_info.grid(column=1, row=7, pady=10)
kill.grid(column=0, columnspan=2, row=8, pady=30)
kill.configure(anchor='center')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)







root.mainloop()