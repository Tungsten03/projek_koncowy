from database import start_database as sdb
from utility import utils
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


query = sdb.Measurement.select()

@utils.log_exec_time
def highest_measurement(sensor: int):
    """
    Function takes sensor ID and print out highest value saved in database.
    :param sensor:
    :return: str
    """
    try:
        # Get measured parameter from database
        param_measured = sdb.Sensor.select().where(sdb.Sensor.id == sensor).get()
        # Setup query and sort values descending
        query = sdb.Measurement.select().order_by(sdb.Measurement.value.desc()).where(sdb.Measurement.sensorId == sensor).get()

        print(f'najwyższa wartość {param_measured.paramFormula} tej stacji: {round(query.value, 2)}')
        print(f'data pomiaru: {query.date}')
    except sdb.Sensor.DoesNotExist:
        print('podano niepoprawny id')

@utils.log_exec_time
def lowest_measurement(sensor: int):
    """
    Function takes sensor ID and print out the highest value saved in database.
    :param sensor:
    :return: str
    """
    try:
        # Get measured parameter from database
        param_measured = sdb.Sensor.select().where(sdb.Sensor.id == sensor).get()
        # Setup query and sort values descending
        query = sdb.Measurement.select().order_by(sdb.Measurement.value.asc()).where(sdb.Measurement.sensorId == sensor).get()

        print(f'najwyższa wartość {param_measured.paramFormula} tej stacji: {round(query.value, 2)}')
        print(f'data pomiaru: {query.date}')
    except sdb.Sensor.DoesNotExist:
        print('podano niepoprawny id')





def plot_values(sensor):

    #Get data from database and filter them
    dates = []
    values = []


    #measured sensor querry
    sensor_measured = sdb.Sensor.select().where(sdb.Sensor.id == sensor).get()
    #station data querry
    station = sdb.Station.select().where(sdb.Station.id == sensor_measured.stationId).get()
    #
    query = sdb.Measurement.select().order_by(sdb.Measurement.date.asc()).where(sdb.Measurement.sensorId == sensor)
    #iterate through database and save them in lists
    for measurement in query:
        dates.append(measurement.date)
        values.append(measurement.value)

    plt.scatter(dates, values)

    # set the labels rotation for clearence
    plt.xticks(np.arange(0, len(dates), 5), rotation=25)

    #show the plot
    plt.xlabel('Data i godzina pomiaru')
    plt.ylabel('Zmierzona wartość')
    plt.title(f'wykres: {sensor_measured.paramFormula} dla stacji: {station.stationName}')

    plt.show()

@utils.log_exec_time
def plot_values2(sensor_id: int):
    """
    Plots the values measured by sensor of a sensor with a linear regression line.

    Retrieves the sensor measured data from the database and filters them. Function plots calculated regression
    on a scatter plot of measured parameter values in time.

    :param sensor_id: The ID of the sensor.
    :return: None
    """
    try:
        # Filter data got from database
        dates = []
        values = []

        sensor_measured = sdb.Sensor.select().where(sdb.Sensor.id == sensor_id).get()
        station = sdb.Station.select().where(sdb.Station.id == sensor_measured.stationId).get()
        query = sdb.Measurement.select().order_by(sdb.Measurement.date.asc()).where(sdb.Measurement.sensorId == sensor_id)

        for measurement in query:
            # Filter out unmeasured data
            if measurement.value is None:
                pass
            else:
                dates.append(measurement.date)
                values.append(measurement.value)

        # Encode data into numerical values
        data_encoded = range(len(dates))

        # Calculate linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(data_encoded, values)
        regression_line = slope * np.array(data_encoded) + intercept
        # Plot scatter plot and linear regression
        plt.scatter(data_encoded, values)
        plt.plot(data_encoded, regression_line, color='red')

        # X-axis setup for clearance
        plt.xticks(np.arange(0, len(dates), 5), dates[::5], rotation=90)

        # Adjust plot layout and title position
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)

        plt.title(f'Wykres: {sensor_measured.paramFormula} dla stacji: {station.stationName}')

        plt.show()
    except (sdb.Station.DoesNotExist, sdb.Sensor.DoesNotExist):
        print('podano niepoprawny id')