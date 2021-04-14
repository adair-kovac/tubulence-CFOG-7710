import pandas as pd
from utils.path_util import get_project_root
import scipy.io as sio
import numpy as np


def load_raw_visibility_data():
    visibility_path = get_data_root_dir() / "PWD Visibility data"
    visibility_header = visibility_path / "PWD_header.dat"
    header = []
    with open(visibility_header, "r+") as header_file:
        header = header_file.read().split()  # todo these are bad column names
        header = header[:-5] + ["1", "2", "3", "4", "5"]  # replacing - columns
    data = load_visibility_file(visibility_path, header, "PWD_180913.dat")
    data2 = load_visibility_file(visibility_path, header, "PWD_180914.dat")
    data.append(data2)
    return data


def load_balloon_data(day, launch_number):
    balloon_dir = get_data_root_dir() / "BalloonData"
    launch_dir = balloon_dir / ("201809" + str(day) + ".00" + str(launch_number))
    dat_files_in_dir = list(launch_dir.glob(r"*.DAT"))
    if len(dat_files_in_dir) > 1:
        raise Exception("Balloon data folder has more than one .DAT file")
    dat_file = dat_files_in_dir[0]
    data = pd.read_csv(launch_dir / dat_file, sep=r"\s+", skiprows=[1,2])
    return data


def load_raw_sonic_data():
    raise Exception("not correctly implemented yet")
    sonic_dir = get_data_root_dir() / "SonicData"
    day_file = "CSV_1_raw_GPF_LinDet_2018_09_13.mat"
    mat_data = sio.loadmat(sonic_dir / day_file)
    return mat_data # how to read this?


def load_visibility_file(visibility_path, header, day_file):
    return pd.read_csv(visibility_path / day_file, names=header, sep=r"\s+")


def get_data_root_dir():
    return get_project_root() / "data" / "2021 Final Project Data"

if __name__=="__main__":
    print(load_raw_sonic_data())