# w', T', u', v', theta_v' :(
from data.data_loader import load_processed_sonic_data, _get_data_root_dir
import CFOG_Q1 as cq
from utils import path_util



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
    a_prime = cq.compute_prime_with_start_times(start_time, "w_prime", sonic_data["w"], a_bar["w"])
    a_prime.to_csv(output_path, index=False, sep="\t")

def calculate_u_prime(sonic_data, output_path):
    start_time = sonic_data.iloc[0]["time"]
    a_bar = cq.compute_avg_with_start_times(start_time, "u", sonic_data["u"])
    a_prime = cq.compute_prime_with_start_times(start_time, "u_prime", sonic_data["u"], a_bar["u"])
    a_prime.to_csv(output_path, index=False, sep="\t")


def calculate_v_prime(sonic_data, output_path):
    start_time = sonic_data.iloc[0]["time"]
    a_bar = cq.compute_avg_with_start_times(start_time, "v", sonic_data["w"])
    a_prime = cq.compute_prime_with_start_times(start_time, "v_prime", sonic_data["v"], a_bar["v"])
    a_prime.to_csv(output_path, index=False, sep="\t")

def calculate_T_prime(sonic_data, output_path):
    start_time = sonic_data.iloc[0]["time"]
    a_bar = cq.compute_avg_with_start_times(start_time, "temp", sonic_data["temp"])
    a_prime = cq.compute_prime_with_start_times(start_time, "T_prime", sonic_data["temp"], a_bar["temp"])
    a_prime.to_csv(output_path, index=False, sep="\t")

def calculate_T_s_prime(sonic_data, output_path):
    start_time = sonic_data.iloc[0]["time"]
    a_bar = cq.compute_avg_with_start_times(start_time, "virtual_temp", sonic_data["virtual_temp"])
    a_prime = cq.compute_prime_with_start_times(start_time, "T_s", sonic_data["virtual_temp"], a_bar["virtual_temp"])
    a_prime.to_csv(output_path, index=False, sep="\t")

if __name__=="__main__":
    main(test=False)