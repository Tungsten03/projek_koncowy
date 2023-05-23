"""
Module for Data Analysis of Measurement Values.

This module provides functions for analyzing measurement values stored in the database. It includes functions to
retrieve the highest and lowest measurement values, calculate the average measurement value, and plot the measurement
values with a linear regression line.

Functions:

- highest_measurement(sensor: int) -> str: Retrieves the highest measurement value saved in the database for a given sensor ID.
- lowest_measurement(sensor: int) -> str: Retrieves the lowest measurement value saved in the database for a given sensor ID.
- avg_measurement(sensor: int) -> float: Calculates the average measurement value for a given sensor ID.
- plot_values(sensor_id: int): Plots the measurement values with a linear regression line for a given sensor ID.
"""

from database import start_database as sdb
from utility import utils
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from tkinter import messagebox

query = sdb.Measurement.select()


def highest_measurement(sensor: int) -> str:
    """
    Retrieve the highest value saved in the database for a given sensor ID.

    This function takes a sensor ID as input and retrieves the highest value stored in the database for that sensor.
    It sorts the values in descending order and returns the result as a string in the format "{value} d:{date}".

    :param sensor: The ID of the sensor.
    :return: The highest value as a string in the format "{value} d:{date}".
    :raises sdb.Sensor.DoesNotExist: If the sensor ID does not exist in the database.
    """
    try:
        # Setup query and sort values descending
        query = sdb.Measurement.select().order_by(sdb.Measurement.value.desc()).where(
            sdb.Measurement.sensorId == sensor).first()

        max_result = f'{query.value} d:{query.date}'
        return max_result
    except sdb.Sensor.DoesNotExist:
        print('podano niepoprawny id')


def lowest_measurement(sensor: int) -> str:
    """
    Retrieve the lowest value saved in the database for a given sensor ID.

    This function takes a sensor ID as input and retrieves the lowest value stored in the database for that sensor.
    It sorts the values in ascending order and returns the result as a string in the format "{value} d:{date}".

    :param sensor: The ID of the sensor.
    :return: The lowest value as a string in the format "{value} d:{date}".
    :raises sdb.Sensor.DoesNotExist: If the sensor ID does not exist in the database.
    """
    try:
        # Setup query and sort values descending
        query = sdb.Measurement.select().order_by(sdb.Measurement.value.asc()).where(
            (sdb.Measurement.value.is_null(False)) & (sdb.Measurement.sensorId == sensor)).first()
        if query is None:
            messagebox.showerror('Błąd', 'Nie wybrano sensora')
        else:
            min_result = f'{query.value} d:{query.date}'
            return min_result
    except sdb.Sensor.DoesNotExist:
        messagebox.showerror('Błąd', 'Podano niepoproawny ID')


def avg_measurement(sensor: int) -> float:
    """
    Calculate the average measurement value for a given sensor ID.

    This function takes a sensor ID as input and calculates the average measurement value for that sensor.
    It retrieves the measurements from the database, filters out the null values, and calculates the average.

    :param sensor: The ID of the sensor.
    :return: The average measurement value rounded to 3 decimal places.
    """
    query = sdb.Measurement.select(sdb.Measurement.value).where(
        (sdb.Measurement.value.is_null(False)) & (sdb.Measurement.sensorId == sensor))

    measurements = [measurement.value for measurement in query]

    if measurements:
        total = sum(measurements)
        average = total / len(measurements)
        return round(average, 3)
    else:
        return 0.0


@utils.log_exec_time
def plot_values(sensor_id: int) -> None:
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
        query = sdb.Measurement.select().order_by(sdb.Measurement.date.asc()).where(
            sdb.Measurement.sensorId == sensor_id)

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
        plt.xticks(np.arange(0, len(dates), 5), dates[::5], rotation=-90)
        # plt.grid(True, which='both')

        # Get max and min values
        max_val = max(values)
        min_val = min(values)

        # Make annotations on plot and format arrow
        plt.annotate(f'Max: {max_val}', xy=(data_encoded[values.index(max_val)], max_val),
                     xytext=(10, -20),
                     textcoords='offset points',
                     color='red',
                     arrowprops=dict(arrowstyle='simple'))

        plt.annotate(f'Min: {min_val}', xy=(data_encoded[values.index(min_val)], min_val),
                     xytext=(10, 20),
                     textcoords='offset points',
                     color='red',
                     arrowprops=dict(arrowstyle='simple'))

        # Adjust plot layout and title position
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)

        plt.title(f'Wykres: {sensor_measured.paramFormula} dla stacji: {station.stationName}')

        plt.show()
    except (sdb.Station.DoesNotExist, sdb.Sensor.DoesNotExist):
        print('podano niepoprawny id')
