from utils import path_util
import pandas as pd
import CFOG_Q1 as cq
import datetime
from data import data_loader


def main(test=True):
    intermediate_dir = path_util.get_project_root() / "data" / "intermediate"
    output_dir = path_util.get_project_root() / "calculations" / "calc_from_intermediate"
    if test:
        intermediate_dir = intermediate_dir / "test"
        output_dir = output_dir / "test"
    tke_output_dir = output_dir / "tke_10"
    levels = [2, 5, 10]
    tke_10_min_sets = dict()
    for level in levels:
        input_dir = intermediate_dir / str(level)
        datasets = load_datasets(input_dir)
        if level == 2:
            surface_data = datasets

        run_calculations(level, datasets, surface_data, output_dir / str(level), test)

    #     tke_10_min_sets[level] = calculate_tke_10_min(datasets, tke_output_dir / str(level))
    # plot_tke_10_min(tke_10_min_sets, tke_output_dir)


def calculate_tke_10_min(datasets, output_dir):
    print("Calculating TKE")
    u_prime = datasets["u_prime"]["u_prime"]
    v_prime = datasets["v_prime"]["v_prime"]
    w_prime = datasets["w_prime"]["w_prime"]
    tke = cq.compute_tke(u_prime, v_prime, w_prime, dt=10)

    start_time = get_start_time(datasets)
    output = cq.create_dataframe("tke", dt=10, start_time=start_time, values=tke)

    output_path = output_dir / "results-tke-10min.csv"
    output_dir.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False, sep="\t")
    return output

def plot_tke_10_min(datasets, output_dir):
    from calculations.scripts.plots import PlotVariables, plot_variable
    print("making plot")
    args = PlotVariables(
        column="tke",
        plot_title="Turbulent Kinetic Energy (tke)",
        y_label="tke (J/kg)",
        output_path=output_dir/"tke.png"
    )
    plot_variable(datasets, args)


def run_calculations(height, datasets, surface_data, output_dir, test):
    w_prime = datasets["w_prime"]["w_prime"]
    T_prime = datasets["T_prime"]["T_prime"]
    print("Calculating temp flux")
    flux = cq.kinematic_temp_flux(w_prime, T_prime)

    start_time = get_start_time(datasets)
    output = cq.create_dataframe("kinematic_temp_flux", dt=30, start_time=start_time, values=flux)

    print("Calculating friction velocity")
    u_prime = datasets["u_prime"]["u_prime"]
    v_prime = datasets["v_prime"]["v_prime"]
    ws_prime = surface_data["w_prime"]["w_prime"]

    # u_star = cq.friction_velocity(u_prime, v_prime, ws_prime)
    # output["friction_velocity"] = u_star

    # print("Calculating sensible heat flux")
    # rho = 1.2 # kg/m^3 Using standard value
    # c_p = 1004 # J/kg/K
    # heat_flux = cq.sensible_heat_flux(flux, rho, c_p)
    # output["H_s"] = heat_flux
    #
    # print("Calculating TKE")
    # tke = cq.compute_tke(u_prime, v_prime, w_prime)
    # output["tke"] = tke

    print("Calculating w*")
    temp_v_prime_surface = surface_data["T_s_prime"]["T_s_prime"] # temp is practically theta for this data
    temp_v_bar = get_average("virtual_temp", height, test) + 273.15
    w_star = cq.convective_velocity_scale(1000, temp_v_bar, ws_prime, temp_v_prime_surface)
    output["w_star"] = w_star

    # print("Calculating Obukhov length")
    # L = cq.obukhov_length(temp_v_bar, u_star, ws_prime, temp_v_prime_surface)
    # output["L"] = L

    print("Writing results")
    output_path = output_dir / "results-w*.csv"
    output_dir.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False, sep="\t")


def get_start_time(datasets):
    return datasets["w_prime"].iloc[0]["time"] - datetime.timedelta(days=1) - datetime.timedelta(days=365)


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


def get_average(column, level, test):
    sonic_data = get_sonic_data(level, test)
    return cq.compute_avg(sonic_data[column])


sonic_data_cached = dict()
def get_sonic_data(level, test):
    if level in sonic_data_cached:
        return sonic_data_cached[level]
    test_dir = None
    if test:
        test_dir = path_util.get_project_root() / "data/2021 Final Project Data/SonicData/select_fields/1hr"
    print("Loading sonic data")
    sonic_data = data_loader.load_processed_sonic_data(level, directory_override=test_dir)
    print("... Loaded")
    sonic_data_cached[level] = sonic_data
    return sonic_data


if __name__=="__main__":
    main(test=False)