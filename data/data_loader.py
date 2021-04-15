import pandas as pd
from utils.path_util import get_project_root
import mat4py


def load_raw_visibility_data():
    visibility_path = _get_data_root_dir() / "PWD Visibility data"
    visibility_header = visibility_path / "PWD_header.dat"
    header = []
    with open(visibility_header, "r+") as header_file:
        header = header_file.read().split()  # todo these are bad column names
        header = header[:-5] + ["1", "2", "3", "4", "5"]  # replacing - columns
    data = _load_visibility_file(visibility_path, header, "PWD_180913.dat")
    data2 = _load_visibility_file(visibility_path, header, "PWD_180914.dat")
    data.append(data2)
    return data


def load_balloon_data(day, launch_number):
    balloon_dir = _get_data_root_dir() / "BalloonData"
    launch_dir = balloon_dir / ("201809" + str(day) + ".00" + str(launch_number))
    dat_files_in_dir = list(launch_dir.glob(r"*.DAT"))
    if len(dat_files_in_dir) > 1:
        raise Exception("Balloon data folder has more than one .DAT file")
    dat_file = dat_files_in_dir[0]
    data = pd.read_csv(launch_dir / dat_file, sep=r"\s+", skiprows=[1,2])
    return data


def load_sonic_data():
    try:
        return pd.read_csv(_get_sonic_data_dir() / "joined_sonic_data.csv", index_col=0, sep="\t")
    except FileNotFoundError as e:
        import sys
        raise FileNotFoundError(str(e) + "\nYou need to download joined_sonic_data.csv " \
                                "from Adair's ubox and put it in the SonicData folder.")\
            .with_traceback(sys.exc_info()[2])


def _load_visibility_file(visibility_path, header, day_file):
    return pd.read_csv(visibility_path / day_file, names=header, sep=r"\s+")


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
   print(load_sonic_data())
