"""----------------------------------KRAQEN-----------------------------------
-------------------------Kacper Rajewski Air Quality Environment-----------------------
"""
# Application requests air quality data from GIOS Api
# Requested data is saved in sqlite3 database
# User can analyze data blablablabla

from utility import labels as lbl

import tkinter as tk

root = tk.Tk()
root.title('KRAQEN v 1.0')
root.geometry('700x500')

info1 = tk.Label(root, text='--KRAQEN--').pack()
info2 = tk.Label(root, text='--Kacper Rajewski Air Quality Environment--').pack()
info3 = tk.Label(root, text='--v 1.0--').pack()
info3 = tk.Label(root, text=240*'-').pack()
info2 = tk.Label(root, text='').pack()
info2 = tk.Label(root, text='Aplikacja pozwala na pobranie i przechowanie danych pomiarowych z API GIOS').pack()

instuction = tk.Label(root, text=lbl.start_menu, justify="center").pack()

start = tk.Button(root, text='START', command=print('start program')).place(x=310, y=300, width=80, height=80)
start = tk.Button(root, text='QUIT', command=root.destroy).place(x=320, y=450, width=60, height=40)



root.mainloop()