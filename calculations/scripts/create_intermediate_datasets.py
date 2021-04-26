# w', T', u', v', theta_v' :(
from data.data_loader import load_processed_sonic_data, _get_data_root_dir
import CFOG_Q1 as cq
from utils import path_util
import pandas as pd


def main(test=True):
    root_output_dir = path_util.get_project_root() / "data" / "intermediate"
    override = None
    if test:
        root_output_dir = root_output_dir / "test"
        override = _get_data_root_dir() / "SonicData/select_fields/1hr"
    levels = [2, 5, 10]

    for level in levels:
        output_dir = root_output_dir / str(level)
        output_dir.mkdir(parents=True, exist_ok=True)
        sonic_data = load_processed_sonic_data(level, override)
        ## Change which methods to call
        calculate_w_prime(sonic_data, output_dir / "w_prime.csv")
        calculate_u_prime(sonic_data, output_dir / "u_prime.csv")
        calculate_T_prime(sonic_data, output_dir / "T_prime.csv")
        calculate_v_prime(sonic_data, output_dir / "v_prime.csv")
        calculate_T_s_prime(sonic_data, output_dir / "T_s_prime.csv")


def calculate_w_prime(sonic_data, output_path):
    start_time = sonic_data.iloc[0]["time"]
    a_bar = cq.compute_avg_with_start_times(start_time, "w", sonic_data["w"])
    a_prime = cq.compute_prime(sonic_data["w"], a_bar["w"])
    make_dataframe(sonic_data, a_prime, "w_prime", output_path)


def calculate_u_prime(sonic_data, output_path):
    start_time = sonic_data.iloc[0]["time"]
    a_bar = cq.compute_avg_with_start_times(start_time, "u", sonic_data["u"])
    a_prime = cq.compute_prime(sonic_data["u"], a_bar["u"])
    make_dataframe(sonic_data, a_prime, "u_prime", output_path)


def calculate_v_prime(sonic_data, output_path):
    start_time = sonic_data.iloc[0]["time"]
    a_bar = cq.compute_avg_with_start_times(start_time, "v", sonic_data["w"])
    a_prime = cq.compute_prime(sonic_data["v"], a_bar["v"])
    make_dataframe(sonic_data, a_prime, "v_prime", output_path)


def calculate_T_prime(sonic_data, output_path):
    start_time = sonic_data.iloc[0]["time"]
    a_bar = cq.compute_avg_with_start_times(start_time, "temp", sonic_data["temp"])
    a_prime = cq.compute_prime(sonic_data["temp"], a_bar["temp"])
    make_dataframe(sonic_data, a_prime, "T_prime", output_path)


def calculate_T_s_prime(sonic_data, output_path):
    start_time = sonic_data.iloc[0]["time"]
    a_bar = cq.compute_avg_with_start_times(start_time, "virtual_temp", sonic_data["virtual_temp"])
    a_prime = cq.compute_prime(sonic_data["virtual_temp"], a_bar["virtual_temp"])
    make_dataframe(sonic_data, a_prime, "T_s_prime", output_path)


def make_dataframe(sonic_data, column, column_name, output_path):
    df = pd.DataFrame()
    df["time"] = sonic_data["time"]
    df[column_name] = column
    df.to_csv(output_path, index=False, sep="\t")

if __name__=="__main__":
    main(test=True)