import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import datetime
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from utils import  path_util

def setup_matplotlib():
    import matplotlib.units as munits
    converter = mdates.ConciseDateConverter()  # formats=['', '', '%d', '%H', '', ''])
    munits.registry[np.datetime64] = converter
    munits.registry[datetime.date] = converter
    munits.registry[datetime.datetime] = converter
    munits.registry[pd.Timestamp] = converter


@dataclass
class PlotVariables:
    column: str
    plot_title: str
    y_label: str
    output_path: Path


def plot_variable(data_at_levels: dict, vars: PlotVariables):
    fig, ax = plt.subplots()
    for level, data in data_at_levels.items():
        plt.plot(data["time"], data[vars.column], label=level)
    plt.legend()
    ax.set_xlabel("Time Interval Start")
    ax.set_ylabel(vars.y_label)
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    plt.title(vars.plot_title)
    plt.savefig(vars.output_path)
    plt.close()


def main(test=True):
    input_dir = path_util.get_project_root() / "calculations" / "calc_from_intermediate"
    if test:
        input_dir = input_dir / "test"

    levels = [2, 5, 10]
    data = dict()
    print("Loading data")
    for level in levels:
        level_input_dir = input_dir / str(level)
        data[level] = pd.read_csv(level_input_dir / "results.csv", sep="\t", parse_dates=["time"])

    output_dir = input_dir / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Making plots")

    #kinematic_temp_flux
    print("Kinematic temp flux")
    args = PlotVariables(
        column="kinematic_temp_flux",
        plot_title="Kinematic Temperature Flux (cov T_S, w)",
        y_label="Flux (K*m/s)",
        output_path=output_dir/"temp_flux.png"
    )
    plot_variable(data, args)

    # friction_velocity
    print("Friction velocity")
    args = PlotVariables(
        column="friction_velocity",
        plot_title="Friction Velocity (u*)",
        y_label="Friction Velocity (m/s)",
        output_path=output_dir/"friction_velocity.png"
    )
    plot_variable(data, args)

    # H_s
    print("H_s")
    args = PlotVariables(
        column="H_s",
        plot_title="Sensible Heat Flux (H_s)",
        y_label="Flux (W/m^2)",
        output_path=output_dir/"sensible_heat_flux.png"
    )
    plot_variable(data, args)

    # tke
    print("tke")
    args = PlotVariables(
        column="tke",
        plot_title="Turbulent Kinetic Energy (tke)",
        y_label="tke (J/kg)",
        output_path=output_dir/"tke.png"
    )
    plot_variable(data, args)


if __name__=="__main__":
    main(test=False)