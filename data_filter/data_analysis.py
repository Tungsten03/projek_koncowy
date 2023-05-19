from database import start_database as sdb
from utility import utils
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

query = sdb.Measurement.select()


def highest_measurement(sensor: int):
    """
    Function takes sensor ID and print out highest value saved in database.
    :param sensor:
    :return: str
    """
    try:
        # Setup query and sort values descending
        query = sdb.Measurement.select().order_by(sdb.Measurement.value.desc()).where(
            sdb.Measurement.sensorId == sensor).get()

        max_result = f'{query.value} d:{query.date}'
        return max_result
    except sdb.Sensor.DoesNotExist:
        print('podano niepoprawny id')


def lowest_measurement(sensor: int):
    """
    Function takes sensor ID and print out the highest value saved in database.
    :param sensor:
    :return: str
    """
    try:
        # Setup query and sort values descending
        query = sdb.Measurement.select().order_by(sdb.Measurement.value.asc()).where(
            (sdb.Measurement.value.is_null(False)) & (sdb.Measurement.sensorId == sensor)).get()
        min_result = f'{query.value} d:{query.date}'
        return min_result
    except sdb.Sensor.DoesNotExist:
        print('podano niepoprawny id')


def avg_measurement(sensor: int):
    pass
    query = sdb.Measurement.select(sdb.Measurement.value).where(
        (sdb.Measurement.value.is_null(False)) & (sdb.Measurement.sensorId == sensor))

    measurements = [measurement.value for measurement in query]

    total = sum(measurements)
    average = total / len(measurements)
    return round(average, 3)


@utils.log_exec_time
def plot_values(sensor_id: int):
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


if __name__ == '__main__':
    from peewee import *

    db = SqliteDatabase('database/stations.db')
    db.connect()
    avg_measurement(744)
