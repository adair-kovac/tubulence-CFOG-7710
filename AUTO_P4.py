import numpy as np
import matplotlib.pyplot as plt
from utils import path_util
import datetime
from data import data_loader

def main():
    U = np.random.normal(5, 1, 1000) # Insert 30-min U period here
    V = np.random.normal(5, 1, 1000) # Insert 30-min V period here
    W = np.random.normal(5, 1, 1000) # Insert 30-min W period here
    T = np.random.normal(5, 1, 1000) # Insert 30-min T period here

    data = get_30_minute_data_window()
    U = data["u"].to_numpy()
    V = data["v"].to_numpy()
    W = data["w"].to_numpy()
    T = data["virtual_temp"].to_numpy()

    plot_autocorrelation(T, U, V, W)

def get_30_minute_data_window():
    minutes = 30
    frequency = 20 # Hz
    num_observations = minutes * 60 * frequency
    sonic_data = data_loader.load_processed_sonic_data(10, directory_override=True)
    return sonic_data.iloc[0:num_observations]

def plot_autocorrelation(T, U, V, W):
    print("starting autocorrelations")
    auto_corr_lag_U = calculate_autocorrelation(U)
    print("finished u")
    auto_corr_lag_V = calculate_autocorrelation(V)
    print("finished v")
    auto_corr_lag_W = calculate_autocorrelation(W)
    print("finished w")
    auto_corr_lag_T = calculate_autocorrelation(T)
    print("finished T")
    dt = 1 / 20  # 20 Hz
    time = np.arange(1, int(len(U)*dt))

    plt.plot(time, auto_corr_lag_U, label="U velocity")
    plt.plot(time, auto_corr_lag_V, label="V velocity")
    plt.plot(time, auto_corr_lag_W, label="W velocity")
    plt.plot(time, auto_corr_lag_T, label="Virtual Temperature")
    plt.ylabel('Autocorrelation')
    plt.xlabel("Lag (seconds)")
    plt.legend()
    plt.grid()
    plt.title("Autocorrelation vs. Lag")
    plt.savefig(path_util.get_project_root() /
                "AutocorrelationLag-{}.png".format(datetime.datetime.now()))


def calculate_autocorrelation(variable):
    mean = np.nanmean(variable)
    auto_corr_lag = []
    primes = variable - mean
    auto_corr_denominator = np.nansum(np.float_power(primes, 2))
    # Assumption made: Data are sufficiently stationary (or homogeneous in space)
    for j in range(1, int(len(variable)/20)):  # time lag
        skip = j*20
        pairs = primes[skip:len(primes)]
        lag = np.nansum(primes[0:len(primes)-skip]*pairs)
        auto_corr_lag.append(lag / auto_corr_denominator)
    return auto_corr_lag


if __name__=="__main__":
    main()