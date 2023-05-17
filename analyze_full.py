import utility.utils
from utility import labels as lbl
from utility import utils
from database import start_database as sdb
from data_filter.data_analysis import plot_values2



import tkinter as tk
from tkinter import ttk

from database import db_functions

def analyze_full():
    def refresh_stations():
        listbox.delete(0, tk.END)
        for station in sdb.Station.select().order_by(sdb.Station.cityName.asc()):
            listbox.insert(tk.END, (station.id, station.stationName))

    def update_entry(event):
            selected_item = listbox.get(listbox.curselection())
            selected_id = selected_item[0]  # Pobierz pierwszy element krotki (id)
            listbox_entry.delete(0, tk.END)  # Wyczyść istniejący tekst w Entry
            listbox_entry.insert(tk.END, selected_id)  # Dodaj id do Entry


    def show_sensors():
        station = listbox_entry.get()
        query = sdb.Sensor.select().where(sdb.Sensor.stationId == station)
        listbox.delete(0, tk.END)
        for sensor in query:
            listbox.insert(tk.END, (sensor.id, sensor.paramCode))
    def make_plot():
        sensor = listbox_entry.get()
        plot_values2(sensor)

    root = tk.Tk()
    root.title(lbl.app_name_analyze)
    root.geometry('800x600')

    station_info = utils.EntryWithPlaceholder(root, 'Opis lokacji')
    entry_range = utils.EntryWithPlaceholder(root, 'Promień [km]')
    listbox_entry = utils.EntryWithPlaceholder(root, 'Aktywny wybór', 'red')

    all_stat = tk.Button(root, text='Wszystkie stacje', command=refresh_stations, width=20)
    app_help = tk.Button(root, text='POMOC', width=20)
    back = tk.Button(root, text='WSTECZ',command=root.destroy, width=20)
    in_range = tk.Button(root, text='W zasięgu', width=20)
    choose_station = tk.Button(root, text='Wybierz stacje', command=show_sensors, width=20)
    choose_sensor = tk.Button(root, text='Wybierz sensor', width=20)
    plot_data = tk.Button(root, text='Wykres', command=make_plot, width=20)





    listbox = tk.Listbox(root, width=400)
    scrollbar = tk.Scrollbar(listbox, orient='vertical', command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set, height=40)
    scrollbar.pack(side='right', fill='y')
    listbox.bind("<<ListboxSelect>>", update_entry)

    all_stat.grid(column=0, row=0, padx=3, pady=3)
    app_help.grid(column=1, row=0, padx=3, pady=3)
    back.grid(column=2, row=0, padx=3, pady=3)
    in_range.grid(column=0, row=1, padx=3, pady=3)
    station_info.grid(column=1, row=1, padx=3, pady=3)
    entry_range.grid(column=2, row=1, padx=3, pady=3)
    choose_station.grid(column=0, row=2, padx=3, pady=3)
    listbox_entry.grid(column=1, row=2, rowspan=2, pady=3)
    choose_sensor.grid(column=0, row=3, padx=3, pady=3)
    plot_data.grid(column=0, row=4)
    listbox.grid(column=0, columnspan=3, row=5, sticky='nswe', pady=3)


    for station in sdb.Station.select().order_by(sdb.Station.cityName.asc()):
        listbox.insert(tk.END, (station.id, station.stationName))

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(5, weight=3)





    root.mainloop()