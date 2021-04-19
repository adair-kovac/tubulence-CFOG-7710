"""
Handles the sonic anemometer coordinate transformation (since the instrument wasn't
oriented due north). Note that due to meteorological convention, the direction of the
wind is opposite the direction of the wind vector.
"""
import numpy as np
import math


def get_wind_direction(u, v, bearing):
    """
    Calculates the actual wind direction given the wind components measured by the sonic anemometer.

    :param u: x-component of wind as returned by sensor
    :param v: y-component of wind as returned by sensor
    :param bearing: degrees between true north and -x axis of sensor
    :return: wind direction in degrees clockwise from north
    """
    sensor_wind_dir = math.degrees(np.arctan(-v/u))  # or u/v? or -u/v?
    angle_from_north = bearing + sensor_wind_dir  # or should it be bearing - 90 ?
    angle_from_north = np.mod(angle_from_north, 360)
    return angle_from_north


def transform_wind(u, v, wind_direction):
    """
    Once we rotate our coordinate system to the new wind direction, u and v
    are different. This function returns the new u and v.

    :param u: Original wind direction (x component)
    :param v: Original wind direction (y component)
    :param wind_direction: Actual wind direction in degrees
    :return: u, v translated into the new coordinate system
    """
    wind_speed = np.sqrt(u**2 + v**2)
    wind_direction = math.radians(wind_direction)
    new_u = - wind_speed * np.sin(wind_direction)
    new_v = - wind_speed * np.cos(wind_direction)
    return new_u, new_v


if __name__=="__main__":
    u = 0.2589
    v = 0.9659
    bearing = 90

    wind_dir = get_wind_direction(u, v, bearing)
    print(wind_dir)
    print(transform_wind(u, v, wind_dir))