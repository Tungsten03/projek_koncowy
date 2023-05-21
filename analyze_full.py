from utility import labels as lbl
from utility import utils
from database import start_database as sdb
from data_filter.data_analysis import plot_values
from data_filter import localize
from data_filter.data_analysis import lowest_measurement, highest_measurement, avg_measurement
import tkinter as tk


def analyze_full():
    def refresh_stations():
        """
        Lists stations in the listbox.

        This function clears the listbox and fills it with station data requested from database.
        It also updates the state of various buttons to block off analysis functions.

        :return:
        """
        # Clear listbox
        listbox.delete(0, tk.END)
        # Block sensor analysis
        calculate.configure(state='disabled')
        plot_data.configure(state='disabled')
        choose_station.configure(state='normal')
        # Retrieve stations from the database and insert them into the listbox
        for i in sdb.Station.select().order_by(sdb.Station.cityName.asc()):
            formatted_string = f'{i.id:<10} {i.stationName:<20}'
            listbox.insert(tk.END, formatted_string)

    def update_entry(event):
        """
        Updates the entry widget with the selected ID from the listbox.

        This function retrieves the selected item from the listbox and extracts the station ID from it.
        It then updates the entry widget with the selected ID.

        :param event: The event object (e.g. listbox selection)
        :return: None
        """
        selected_item = listbox.get(listbox.curselection())
        if selected_item:
            selected_id = selected_item.split()[0]
            listbox_entry.delete(0, tk.END)
            listbox_entry.insert(tk.END, selected_id)
        else:
            pass

    def calculate_data():
        """
        Calculates and displays data based on the selected sensor ID.

        This function retrieves the sensor ID from the entry widget, calls measurement functions,
        and displays the calculated values in corresponding output widgets.

        :return: None
        """
        sensor = int(listbox_entry.get())
        # Calculate relevant values
        min_val_calc = lowest_measurement(sensor)
        max_val_calc = highest_measurement(sensor)
        avg_val_calc = avg_measurement(sensor)
        # Clear corresponding entry
        min_val.delete(0, tk.END)
        max_val.delete(0, tk.END)
        avg_val.delete(0, tk.END)
        # Insert data to proper entry
        min_val.insert(tk.END, min_val_calc)
        max_val.insert(tk.END, max_val_calc)
        avg_val.insert(tk.END, avg_val_calc)

    @utils.log_exec_time
    def show_sensors():
        """
        Displays the sensors for the selected station.

        This function retrieves the station ID from the entry widget,
        queries the database for sensors associated with the station,
        and populates the listbox with the sensor IDs and parameter codes.

        It also updates the state of buttons to allow sensor analysis.

        :return: None
        """
        try:
            # Get station ID from entry
            station_entry = listbox_entry.get()
            # Query database and clear listbox
            query = sdb.Sensor.select().where(sdb.Sensor.stationId == station_entry)
            listbox.delete(0, tk.END)
            # Populate the listbox
            for sensor in query:
                formatted_string = f'{sensor.id:<10} {sensor.paramFormula:<20}'
                listbox.insert(tk.END, formatted_string)
            # Switch the buttons to proper state
            calculate.configure(state='normal')
            plot_data.configure(state='normal')
            choose_station.configure(state='disabled')
        # Handle the exception
        except ValueError:
            pass

    def make_plot():
        """
        Displays plot  for the selected sensor ID

        :return:
        """
        sensor = listbox_entry.get()
        plot_values(int(sensor))

    def show_in_range():
        """
        Displays stations within a specified range from a user-defined place.

        This function retrieves the user-defined place and range from the respective entry widgets.
        It then calls the 'localize.stations_in_range()' function to get a stations within the specified range.
        The station IDs and names from the dictionary are inserted into the listbox.

        If a ValueError occurs (e.g., invalid range),.
        it opens a popup window displaying a warning message with instructions.

        :return: None
        """
        try:
            # Clear listbox and switch off analysis buttons
            listbox.delete(0, tk.END)
            calculate.configure(state='disabled')
            plot_data.configure(state='disabled')
            # Get data from entry
            user_place = station_info.get()
            user_range = float(entry_range.get())
            # Prepare station dictionary and populate listbox
            station_dict = localize.stations_in_range(user_place, user_range)
            for key, value in station_dict:
                formatted_string = f'{key:<10} {value:<20}'
                listbox.insert(tk.END, formatted_string)
            #
            calculate.configure(state='disabled')
            plot_data.configure(state='disabled')
            choose_station.configure(state='normal')
        # Handle the Value Error and display a warning
        except ValueError:
            popup = tk.Toplevel()
            popup.title('Uwaga!')

            label = tk.Label(popup, text=lbl.popup_warn)
            label.pack(padx=20, pady=20)

            button = tk.Button(popup, text="Zamknij", command=popup.destroy)
            button.pack(pady=10)

    def show_help():
        """
        Display a help popup window with instructions.

        This function creates a new 'Pomoc' popup window using `Toplevel()`. It adds a label to the
        popup window with the help text obtained from `lbl.gui_help`.

        :return: None
        """
        # Create a new popup window with 'Pomoc' title
        popup = tk.Toplevel()
        popup.title('Pomoc')

        # Create a label with help text
        label = tk.Label(popup, text=lbl.gui_help)
        label.pack(padx=20, pady=20)

        # Create a close button
        button = tk.Button(popup, text="Zamknij", command=popup.destroy)
        button.pack(pady=10)

    # Setup GUI for analysis window
    root = tk.Tk()
    root.title(lbl.app_name_analyze)
    root.geometry('800x600')

    # Setup frame for calculation results
    results = tk.Frame(root, relief=tk.RAISED, width=2)

    calculate = tk.Button(results, text='Wylicz dane', command=calculate_data, width=20)
    calculate.configure(state='disabled')

    minimal = tk.Label(results, text='minimalny:')
    maximal = tk.Label(results, text='maksymalny:')
    average = tk.Label(results, text='średnio:')
    min_val = tk.Entry(results)
    max_val = tk.Entry(results)
    avg_val = tk.Entry(results)

    # Setup Buttons
    app_help = tk.Button(root, text='POMOC', command=show_help, width=10)
    back = tk.Button(root, text='WSTECZ', command=root.destroy, width=10)
    all_stat = tk.Button(root, text='Wszystkie stacje', command=refresh_stations, width=15)
    in_range = tk.Button(root, text='W zasięgu', command=show_in_range, width=15)
    choose_station = tk.Button(root, text='Wybierz stacje', command=show_sensors, width=20)

    # Setup Entry widgets with placeholders
    station_info = utils.EntryWithPlaceholder(root, 'Opis lokacji')
    entry_range = utils.EntryWithPlaceholder(root, 'Promień [km]')
    plot_data = tk.Button(root, text='Wykres', command=make_plot, width=20)
    plot_data.configure(state='disabled')
    listbox_entry = utils.EntryWithPlaceholder(root, 'Aktywny wybór', 'red')

    # Setup listbox
    listbox = tk.Listbox(root, width=400, font='Courier')
    scrollbar = tk.Scrollbar(listbox, orient='vertical', command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set, height=40)
    scrollbar.pack(side='right', fill='y')
    listbox.bind("<<ListboxSelect>>", update_entry)

    # GUI widgets arrangement (grid model)
    app_help.grid(column=1, row=0, padx=3, sticky='w')
    back.grid(column=1, row=0, padx=3, sticky='e')

    all_stat.grid(column=0, row=1, padx=3, sticky='w')

    in_range.grid(column=0, row=1, padx=3, sticky='e')
    station_info.grid(column=1, row=1, padx=3, sticky='we')

    entry_range.grid(column=1, row=1, padx=3, sticky='e')
    choose_station.grid(column=1, row=2, padx=3)

    listbox_entry.grid(column=1, row=3)
    plot_data.grid(column=0, row=2)

    # Results widgets arragement
    results.grid(column=2, row=1, rowspan=3)
    calculate.grid(column=0, columnspan=2, row=0, padx=3)

    minimal.grid(column=0, row=1)
    maximal.grid(column=0, row=2)
    average.grid(column=0, row=3)

    min_val.grid(column=1, row=1, sticky='e')
    max_val.grid(column=1, row=2, sticky='e')
    avg_val.grid(column=1, row=3, sticky='e')

    listbox.grid(column=0, columnspan=3, row=5, sticky='nswe')

    # Fill listbox with stations at start
    for station in sdb.Station.select().order_by(sdb.Station.cityName.asc()):
        formatted_string = f'{station.id:<10} {station.stationName:<20}'
        listbox.insert(tk.END, formatted_string)

    # Set column and row weights
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    root.columnconfigure(2, weight=1)
    root.rowconfigure(5, weight=3)

    root.mainloop()
