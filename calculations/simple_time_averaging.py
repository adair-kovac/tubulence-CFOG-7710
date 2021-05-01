import CFOG_Q1 as cq
from calculations.config import Config
from data.data_loader import load_processed_sonic_data
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import numpy as np
import datetime

def main():
    config = Config()
    levels = [2, 5, 10]

    sonic_data_sets = [] if config.config["only_plots"] else dict(zip(levels,
                        [load_processed_sonic_data(level, config.get_sonic_data_dir()) for level in levels]))

    for calculation, params in config.config["calculations"].items():
        if config.is_enabled(calculation):
            if config.run_calculation(calculation):
                globals()["run_" + calculation](config, sonic_data_sets)
            else:
                globals()["plot_" + calculation + "_from_saved_data"](config, levels)


def plot_w_avg_from_saved_data(config, levels):
    plot_var_avg_from_saved_data("w", config, levels)


def run_w_avg(config, sonic_data_sets):
    run_var_average("w", "w", config, sonic_data_sets)

def plot_speed_avg_from_saved_data(config, levels):
    plot_var_avg_from_saved_data("speed", config, levels)


def run_speed_avg(config, sonic_data_sets):
    run_var_average("speed", "speed", config, sonic_data_sets)


def plot_u_avg_from_saved_data(config, levels):
    plot_var_avg_from_saved_data("u", config, levels)


def run_u_avg(config, sonic_data_sets):
    run_var_average("u", "u", config, sonic_data_sets)

def plot_dir_avg_from_saved_data(config, levels):
    plot_var_avg_from_saved_data("dir", config, levels)


def run_dir_avg(config, sonic_data_sets):
    run_var_average("dir", "direction", config, sonic_data_sets)


def plot_v_avg_from_saved_data(config, levels):
    plot_var_avg_from_saved_data("v", config, levels)


def run_v_avg(config, sonic_data_sets):
    run_var_average("v", "v", config, sonic_data_sets)

def plot_rho_v_avg_from_saved_data(config, levels):
    plot_var_avg_from_saved_data("rho_v", config, levels)


def run_rho_v_avg(config, sonic_data_sets):
    run_var_average("rho_v", "rho_v", config, sonic_data_sets)

def plot_pressure_avg_from_saved_data(config, levels):
    plot_var_avg_from_saved_data("pressure", config, levels)


def run_pressure_avg(config, sonic_data_sets):
    run_var_average("pressure", "pressure", config, sonic_data_sets)


def run_T_avg(config, sonic_data_sets):
    run_var_average("T", "temp", config, sonic_data_sets)


def plot_T_avg_from_saved_data(config, levels):
    plot_var_avg_from_saved_data("T", config, levels)


def plot_var_avg_from_saved_data(variable, config, levels):
    averages = dict()
    for level in levels:
        file = config.get_data_output_dir() / "{}_avg_{}.csv".format(variable, level)
        averages[level] = pd.read_csv(file, sep="\t", parse_dates=["time"])
    plot_variable_avg(variable, averages, config)


def run_var_average(variable, column, config, sonic_data_sets):
    averages = dict()
    for level, data in sonic_data_sets.items():
        start_time = data.iloc[0]["time"]
        avg = cq.compute_avg_with_start_times(start_time, variable, data[column])
        file = config.get_data_output_dir() / "{}_avg_{}.csv".format(variable, level)
        avg.to_csv(file, index=False, sep="\t")
        averages[level] = avg

    plot_variable_avg(variable, averages, config)


def plot_variable_avg(variable, averages, config):
    dissipation, formation = get_dissipation_formation_times()

    fig, ax = plt.subplots()
    for level, data in averages.items():
        data = data[(data["time"] >= pd.Timestamp('2018-09-13 21:00:00')) &
                    (data["time"] <= pd.Timestamp('2018-09-14 06:00:00'))]
        plt.plot(data["time"], data[variable], label=level)
    plt.legend()
    ax.set_xlabel("Time Interval Start")
    ax.set_ylabel(config.config["calculations"]["{}_avg".format(variable)]["y_label"])
    plt.xlim(pd.Timestamp('2018-09-13 21:00:00'), pd.Timestamp('2018-09-14 06:00:00'))
    for line1, line2 in zip(formation, dissipation):
        ax.axvspan(line1, line2, alpha=0.2, color='blue')
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.HourLocator(interval=3)))
    plt.title("30-Minute Averages - {}".format(variable))
    plt.savefig(config.get_figure_output_dir() / "{}_avg.png".format(variable))
    plt.close()


def get_dissipation_formation_times():
    from data import data_loader
    vis = data_loader.load_raw_visibility_data()
    formation = []
    dissipation = []
    threshold = 1000
    last = 10000000
    for i, row in vis.iterrows():
        current = row["vis_10_min"]
        if last < threshold and current >= threshold:
            dissipation.append(row["time"])
        if last >= threshold and current < threshold:
            formation.append(row["time"])
        last = current
    return dissipation, formation


if __name__=="__main__":
    main()