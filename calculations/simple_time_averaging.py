import CFOG_Q1 as cq
from calculations.config import Config
from data.data_loader import load_processed_sonic_data
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import numpy as np
import datetime

def main():
    setup_matplotlib()
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


def setup_matplotlib():
    import matplotlib.units as munits
    converter = mdates.ConciseDateConverter()  # formats=['', '', '%d', '%H', '', ''])
    munits.registry[np.datetime64] = converter
    munits.registry[datetime.date] = converter
    munits.registry[datetime.datetime] = converter
    munits.registry[pd.Timestamp] = converter


def plot_w_avg_from_saved_data(config, levels):
    plot_var_avg_from_saved_data("w", config, levels)


def run_w_avg(config, sonic_data_sets):
    run_var_average("w", "w", config, sonic_data_sets)


def run_T_avg(config, sonic_data_sets):
    run_var_average("T", "temp", config, sonic_data_sets)


def plot_T_avg_from_saved_data(config, levels):
    plot_var_avg_from_saved_data("T", config, levels)


def plot_var_avg_from_saved_data(variable, config, levels):
    averages = dict()
    for level in levels:
        file = config.get_data_output_dir() / "{}_avg_{}.csv".format(variable, level)
        averages[level] = pd.read_csv(file, sep="\t", parse_dates=["start_time"])
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
    fig, ax = plt.subplots()
    for level, data in averages.items():
        plt.plot(data["start_time"], data[variable], label=level)
    plt.legend()
    ax.set_xlabel("Time Interval Start")
    ax.set_ylabel(config.config["calculations"]["{}_avg".format(variable)]["y_label"])
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    plt.title("30-Minute Averages - {}".format(variable))
    plt.savefig(config.get_figure_output_dir() / "{}_avg.png".format(variable))
    plt.close()

if __name__=="__main__":
    main()