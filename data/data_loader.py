""" Code for loading the data files. Includes transformation of raw data. """
import pandas as pd
from utils.path_util import get_project_root
import mat4py
from data import time_format
from data import wind_coordinate
import numpy as np


def load_raw_visibility_data():
    """
    Loads both days of visibility data with columns:
    "time", "vis_1_min", "vis_10_min"
    :return: pandas.DataFrame
    """
    visibility_path = _get_data_root_dir() / "PWD Visibility data"
    visibility_header = visibility_path / "PWD_header.dat"
    with open(visibility_header, "r+") as header_file:
        header = header_file.read().split()
        header = header[:-5] + ["1", "2", "3", "4", "5"]  # replacing - columns
    data = _load_visibility_file(visibility_path, header, "PWD_180913.dat")
    data2 = _load_visibility_file(visibility_path, header, "PWD_180914.dat")
    data.append(data2)
    data = data[["time", "Vis1Min",	"Vis10Min"]]
    data.columns = ["time", "vis_1_min",	"vis_10_min"]
    return data


def load_balloon_data(day, launch_number):
    """
    Loads the sounding data, returns dataframe with columns:
    "time", "pressure", "temp", "relative_humidity", "altitude", "speed",
                    "direction", "potential_temp", "dewpoint"

    Note that valid day/launch_number combos are (13, 2), (13,3), (14, 2), (14, 4), and (14, 5).

    :param day: 13 or 14
    :param launch_number: 1, 2, 3, 4, or 5 (has to exist for the day passed)
    :return: pandas.DataFrame
    """
    balloon_dir = _get_data_root_dir() / "BalloonData"
    launch_dir = balloon_dir / ("201809" + str(day) + ".00" + str(launch_number))
    dat_files_in_dir = list(launch_dir.glob(r"*.DAT"))
    if len(dat_files_in_dir) > 1:
        raise Exception("Balloon data folder has more than one .DAT file")
    dat_file = dat_files_in_dir[0]
    data = pd.read_csv(launch_dir / dat_file, sep=r"\s+", skiprows=[1,2], parse_dates=["Time"],
                       date_parser=time_format.get_parser_for_balloon_time(day))
    data = data[["Time", "Press", "Temp", "Rh", "Alt", "Speed", "Dir", "P.Temp", "Dew"]]
    data.columns = ["time", "pressure", "temp", "relative_humidity", "altitude", "speed",
                    "direction", "potential_temp", "dewpoint"]
    return data


def load_processed_sonic_data(level):
    """
    Loads the sonic anemometer data (from an intermediate dataset you need to download!)

    Column names are:
    "time", "pressure", "rho_v", "u", "v", "w", "virtual_temp", "temp", "potential_temp"

    :param level: 2, 5, or 10 - the height (in meters) of the dataset
    :return: pandas.DataFrame
    """
    file = _get_sonic_data_dir() / "select_fields" / ("sonic_data_" + str(level))
    try:
        df = pd.read_csv(file, sep="\t", parse_dates=["time"], index_col=0)
        return df
    except FileNotFoundError as e:
        _handle_file_not_found(e, "select_fields")


def _load_sonic_data_select_columns():
    data = _load_sonic_data()
    keep_plain = ["t_0", "P_1", "rhov_0"]
    keep_indexed = ["u", "v", "w", "sonTs", "fwT", "fwTh"]
    suffixes = ["2", "5", "10"]
    new_names = ["time", "pressure", "rho_v", "u", "v", "w", "virtual_temp", "temp", "potential_temp"]
    for level_i in range(0, 3):
        keep_at_level = keep_plain + [col + "_" + str(level_i) for col in keep_indexed]
        df_at_level = data[keep_at_level]
        df_at_level.columns = new_names
        df_at_level = _process_wind_data(df_at_level)
        df_at_level["time"] = time_format.convert_matlab_time_column(df_at_level["time"])
        output_dir = _get_sonic_data_dir() / "select_fields"
        output_dir.mkdir(parents=True, exist_ok=True)
        df_at_level.to_csv(output_dir / ("sonic_data_"
                                      + suffixes[level_i]), sep="\t")


def _process_wind_data(df):
    bearing = 60
    direction = wind_coordinate.get_wind_direction(df["u"], df["v"], bearing)
    u, v, speed = wind_coordinate.transform_wind(df["u"], df["v"], direction)
    df["u"] = u
    df["v"] = v
    df["speed"] = speed
    df["direction"] = direction
    return df


def _load_sonic_data():
    try:
        file = "joined_sonic_data.csv"  # "test_sonic_data.csv"
        header_frame = pd.read_csv(_get_sonic_data_dir() / file, index_col=0, sep="\t", nrows=0)
        types_to_shorten = list(header_frame.columns)
        types_to_shorten.remove("t_0")
        types = _get_single_types_dict(types_to_shorten)
        return pd.read_csv(_get_sonic_data_dir() / file, index_col=0, sep="\t", dtype=types)
    except FileNotFoundError as e:
        _handle_file_not_found(e, file)


def _handle_file_not_found(e, file_name):
    import sys
    raise FileNotFoundError(str(e) + "\nYou need to download {} from Adair's ubox " \
                                     "and put it in the SonicData folder.".format(file_name)) \
        .with_traceback(sys.exc_info()[2])


def _get_single_types_dict(single_types):
    types_dict = dict()
    for single in single_types:
        types_dict[single] = np.single

def _load_visibility_file(visibility_path, header, day_file):
    kwargs = time_format.get_time_parsing_args_for_visibility_data()
    return pd.read_csv(visibility_path / day_file, names=header, sep=r"\s+", **kwargs)


def _combine_sonic_data_csv():
    # get all the file names
    day_dir = _get_sonic_data_dir() / "13"
    dataframes = []
    for file in day_dir.iterdir():
        var_name = file.name[:-4] # remove .csv
        df = pd.read_csv(file, sep="\t", index_col=0)
        df2 = pd.read_csv(_get_sonic_data_dir() / "14" / file.name, sep="\t", index_col=0)
        df = df.append(df2)
        df = df.reset_index()
        df.columns = [var_name + "_" + column for column in df.columns]
        dataframes.append(df)
    joined = dataframes[0].join(dataframes[1:])
    joined.to_csv(_get_sonic_data_dir() / "sonic_data.csv", sep="\t")


def _remove_index_columns():
    # Fix for accidentally including index columns in combine_sonic_data_csv
    data = pd.read_csv(_get_sonic_data_dir() / "sonic_data.csv", sep="\t", index_col=0)
    keep_columns = [column for column in data.columns if not column.endswith("_index")]
    data = data[keep_columns]
    data.to_csv(_get_sonic_data_dir() / "joined_sonic_data.csv", sep="\t")


def _mat_to_csv_sonic_data():
    sonic_dir = _get_sonic_data_dir()
    day_file = "CSV_1_raw_GPF_LinDet_2018_09_14.mat"
    with open(sonic_dir / day_file, 'rb') as mat_file:
        mat_data = mat4py.loadmat(mat_file)
        raw_flux = mat_data["rawFlux"]
        columns_output_dir = sonic_dir / "14"
        columns_output_dir.mkdir(parents=True, exist_ok=True)
        for key, value in raw_flux.items():
            df = pd.DataFrame(value)
            df.to_csv(columns_output_dir / (key + ".csv"), sep="\t")


def _get_sonic_data_dir():
    return _get_data_root_dir() / "SonicData"


def _get_data_root_dir():
    return get_project_root() / "data" / "2021 Final Project Data"

if __name__=="__main__":
   print(load_processed_sonic_data(5))
