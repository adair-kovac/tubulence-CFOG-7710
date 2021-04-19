""" Code related to standardizing time format for the different datasets """
import pandas as pd
import datetime


def get_time_parsing_args_for_visibility_data():
    """
    Gets the keyword args needed to parse the visibility data's time in pandas.read_csv.
    :return: dictionary of pandas keyword args
    """
    args = dict()
    args["parse_dates"] = {"time": ["yyyy/mm/dd", "HH:MM:SS"]}  # these are actually column names
    return args


def get_parser_for_balloon_time(day):
    """ The tethered balloon data has time in the format: 19:18:45. This function returns a parser to convert
     the string to a datetime type instead, adding the year, month, and day data.

    :param day: day of the month (13 or 14 for our data), string or int
    :return: function to pass to pandas.read_csv date_parser
    """

    def parser(time_string):
        time_segments = time_string.split(":")
        time_segments = [int(segment) for segment in time_segments]
        return datetime.datetime(2018, 9, int(day), hour=time_segments[0],
                                 minute=time_segments[1], second=time_segments[2])
    return parser


def convert_matlab_time_column(time_data_in_pandas):
    """ Used to convert the time column from the .mat data

    :param time_data_in_pandas:
    :return: pandas series with pd.Timestamp objects
    """
    return time_data_in_pandas.apply(lambda x: _convert_time(x))


def _float_to_time(time_float):
    hour, residual = divmod(time_float*24, 1)
    minute, residual = divmod(residual*60, 1)
    seconds, residual = divmod(residual*60, 1)
    microseconds = residual*1000000
    return int(hour), int(minute), int(seconds), int(microseconds)


def _convert_time(ordinal_time):
    dt = datetime.datetime.fromordinal(int(ordinal_time))
    hour, minute, second, microsecond = _float_to_time(ordinal_time % 1)
    dt = dt.replace(hour=hour, minute=minute, second=second, microsecond=microsecond)
    return dt