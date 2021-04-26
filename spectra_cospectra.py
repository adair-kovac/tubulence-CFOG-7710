import numpy as np
import matplotlib.pyplot as plt
from data import data_loader
from utils import path_util

#if calculating the energy spectrum, enter the same variable in place of variable 1 and variable 2, these have to have the same length and the same sampling frequency
def spectra(variable1, variable2, sampling_frequency, variable_name, directory):
    samp_f = sampling_frequency #should be 20 the campbell CSAT3 sonic anemometers

    u = variable1 #redefine arbitrarily so easier to read
    v = variable2 #redefine arbitrarily so easier to read

    u_mean = sum(u)/len(u)
    v_mean = sum(v)/len(v)

    u = u - u_mean #get rid of the mean component of the flow so we are only assessing the fluctuations within the flow
    v = v - v_mean #get rid of the mean component of the flow so we are only assessing the fluctuations within the flow

    N = len(u) #number of points in the data
    N_f = len(u)//2 # nyquist number of points

    n_tilda = samp_f*N_f//N #maximum reportable frequency

    delta_n_tilda = samp_f/N

    fk_u = np.fft.fft(u) #calculate fourier coefficients
    fk_v = np.fft.fft(v) #calculate fourier coefficients

    fk_u = fk_u/len(u) #normalize by scaling by length of your time/space series
    fk_v = fk_v/len(v) #normalize by scaling by length of your time/space series

    Euv_f = 2*fk_u*np.conj(fk_v) # 2 * to account for the folding over of frequencies past the nyquist frequency

    Suv_f = Euv_f/delta_n_tilda

    Suv_f = Suv_f[0:N_f]

    f = np.linspace(1,n_tilda,N_f)

    plt.loglog(f,Suv_f)

    plt.xlabel("Frequency")
    plt.ylabel("Power Spectral Density of {}".format(variable_name)) #insert which variable you are plugging in.
    plt.savefig(directory / "{}-spectral-density.png".format(variable_name))
    plt.close()


def main(test=True):
    levels = [2, 5, 10]
    for level in levels:
        data = data_loader.load_processed_sonic_data(level, directory_override=test)
        # u, v, w, and T
        u = data["u"].dropna()
        v = data["v"].dropna()
        w = data["w"].dropna()
        T = data["temp"].dropna()

        output_dir = path_util.get_project_root() / "spectra"
        if test:
            output_dir = output_dir / "test"
        output_dir = output_dir / str(level)
        output_dir.mkdir(parents=True, exist_ok=True)

        sampling_freq = 20
        print("u")
        spectra(u, u, sampling_freq, "U", output_dir)
        print("v")
        spectra(v, v, sampling_freq, "V", output_dir)
        print("w")
        spectra(w, w, sampling_freq, "W", output_dir)
        print("T")
        spectra(T, T, sampling_freq, "Temperature", output_dir)


if __name__=="__main__":
    main(test=False)
