from utils import path_util
import pandas as pd
import CFOG_Q1 as cq


def main(test=True):
    intermediate_dir = path_util.get_project_root() / "data" / "intermediate"
    output_dir = path_util.get_project_root() / "calculations" / "calc_from_intermediate"
    if test:
        intermediate_dir = intermediate_dir / "test"
        output_dir = output_dir / "test"

    levels = [2, 5, 10]
    for level in levels:
        input_dir = intermediate_dir / str(level)
        datasets = load_datasets(input_dir)

        run_calculations(datasets, output_dir / str(level))


def run_calculations(datasets, output_dir):
    w_prime = datasets["w_prime"]["w_prime"]
    T_s_prime = datasets["T_s_prime"]["T_s"]
    print("Calculating temp flux")
    flux = cq.kinematic_temp_flux(w_prime, T_s_prime)

    start_time = datasets["w_prime"].iloc[0]["time"]
    output = cq.create_dataframe("kinematic_temp_flux", dt=30, start_time=start_time, values=flux)

    print("Calculating friction velocity")
    u_prime = datasets["u_prime"]["u_prime"]
    v_prime = datasets["v_prime"]["v_prime"]

    u_star = cq.friction_velocity(u_prime, v_prime, w_prime)
    output["friction_velocity"] = u_star

    print("Calculating sensible heat flux")
    rho = 1.2 # kg/m^3 Using standard value
    c_p = 1004 # J/kg/K
    heat_flux = cq.sensible_heat_flux(flux, rho, c_p)
    output["H_s"] = heat_flux

    print("Calculating TKE")
    tke = cq.compute_tke(u_prime, v_prime, w_prime)
    output["tke"] = tke

    print("Writing results")
    output_path = output_dir / "results.csv"
    output_dir.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False, sep="\t")


def run_level_based_calculations(datasets, output_dir):
    pass # Todo obukhov length and deardorf velocity


def load_datasets(intermediate_dir):
    print("Loading datasets")
    datasets = dict()
    datasets["T_prime"] = load(intermediate_dir / "T_prime.csv")
    datasets["T_s_prime"] = load(intermediate_dir / "T_s_prime.csv")
    datasets["u_prime"] = load(intermediate_dir / "u_prime.csv")
    datasets["v_prime"] = load(intermediate_dir / "v_prime.csv")
    datasets["w_prime"] = load(intermediate_dir / "w_prime.csv")
    print("Datasets loaded")
    return datasets


def load(path):
    return pd.read_csv(path, sep="\t", parse_dates=["time"])


if __name__=="__main__":
    main(test=False)