import utility.utils
from utility import labels as lbl
from utility import utils
from database import start_database as sdb
from data_filter.data_analysis import plot_values2
from geolocation import localize
from data_filter.data_analysis import lowest_measurement, highest_measurement, avg_measurement



import tkinter as tk
from tkinter import ttk

from database import db_functions

def analyze_full():
    def refresh_stations():
        listbox.delete(0, tk.END)
        calculate.configure(state='disabled')
        plot_data.configure(state='disabled')
        for station in sdb.Station.select().order_by(sdb.Station.cityName.asc()):
            listbox.insert(tk.END, (station.id, station.stationName))

    def update_entry(event):
            selected_item = listbox.get(listbox.curselection())
            selected_id = selected_item[0]  # Pobierz pierwszy element krotki (id)
            listbox_entry.delete(0, tk.END)  # Wyczyść istniejący tekst w Entry
            listbox_entry.insert(tk.END, selected_id)  # Dodaj id do Entry

    def calculate_data():
        sensor = listbox_entry.get()
        min_val_calc = lowest_measurement(sensor)
        max_val_calc = highest_measurement(sensor)
        # avg_val_calc = avg_measurement(sensor)
        min_val.delete(0, tk.END)
        max_val.delete(0, tk.END)
        avg_val.delete(0, tk.END)
        min_val.insert(tk.END, min_val_calc)
        max_val.insert(tk.END, max_val_calc)
        # avg_val.insert(tk.END, avg_val_calc)

    @utils.log_exec_time
    def show_sensors():
        try:
            station = listbox_entry.get()
            query = sdb.Sensor.select().where(sdb.Sensor.stationId == station)
            listbox.delete(0, tk.END)
            for sensor in query:
                listbox.insert(tk.END, (sensor.id, sensor.paramCode))
            calculate.configure(state='normal')
            plot_data.configure(state='normal')
        except Exception:
            print('Nie zaznaczono żadnej pozycji z listy.')
    def make_plot():
        sensor = listbox_entry.get()
        plot_values2(sensor)

    def show_in_range():
        listbox.delete(0, tk.END)
        calculate.configure(state='disabled')
        plot_data.configure(state='disabled')
        user_place = station_info.get()
        range = float(entry_range.get())
        station_dict = localize.stations_in_range(user_place, range)
        for key, value in station_dict:
            listbox.insert(tk.END, (key, value))




    root = tk.Tk()
    root.title(lbl.app_name_analyze)
    root.geometry('800x600')

    results = tk.Frame(root, relief=tk.RAISED, width=2)
    calculate = tk.Button(results, text='Wylicz dane', command=calculate_data, width=20)
    calculate.configure(state='disabled')
    min = tk.Label(results, text='minimalny:')
    max = tk.Label(results, text='maksymalny:')
    avg = tk.Label(results, text='średnio:')
    min_val = tk.Entry(results)
    max_val = tk.Entry(results)
    avg_val = tk.Entry(results)


    app_help = tk.Button(root, text='POMOC', width=10)
    back = tk.Button(root, text='WSTECZ',command=root.destroy, width=10)

    all_stat = tk.Button(root, text='Wszystkie stacje', command=refresh_stations, width=15)
    in_range = tk.Button(root, text='W zasięgu', command=show_in_range, width=15)
    choose_station = tk.Button(root, text='Wybierz stacje', command=show_sensors, width=20)

    station_info = utils.EntryWithPlaceholder(root, 'Opis lokacji')
    entry_range = utils.EntryWithPlaceholder(root, 'Promień [km]')
    plot_data = tk.Button(root, text='Wykres', command=make_plot, width=20)
    plot_data.configure(state='disabled')

    listbox_entry = utils.EntryWithPlaceholder(root, 'Aktywny wybór', 'red')


    listbox = tk.Listbox(root, width=400)
    scrollbar = tk.Scrollbar(listbox, orient='vertical', command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set, height=40)
    scrollbar.pack(side='right', fill='y')
    listbox.bind("<<ListboxSelect>>", update_entry)

    app_help.grid(column=1, row=0, padx=3, sticky='w')
    back.grid(column=1, row=0, padx=3, sticky='e')

    all_stat.grid(column=0, row=1, padx=3, sticky='w')

    in_range.grid(column=0, row=1, padx=3,sticky='e')
    station_info.grid(column=1, row=1, padx=3, sticky='we')
    entry_range.grid(column=1, row=1, padx=3, sticky='e')
    choose_station.grid(column=1, row=2, padx=3)
    listbox_entry.grid(column=1, row=3)
    plot_data.grid(column=0, row=2)

    results.grid(column=2, row=1, rowspan=3)
    calculate.grid(column=0, columnspan=2, row=0, padx=3)
    min.grid(column=0, row=1)
    max.grid(column=0, row=2)
    avg.grid(column=0, row=3)
    min_val.grid(column=1, row=1, sticky='e')
    max_val.grid(column=1, row=2, sticky='e')
    avg_val.grid(column=1, row=3, sticky='e')

    listbox.grid(column=0, columnspan=3, row=5, sticky='nswe')


    for station in sdb.Station.select().order_by(sdb.Station.cityName.asc()):
        listbox.insert(tk.END, (station.id, station.stationName))

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(5, weight=3)





    root.mainloop()