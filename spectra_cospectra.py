import numpy as np

#if calculating the energy spectrum, enter the same variable in place of variable 1 and variable 2, these have to have the same length and the same sampling frequency

def spectra(variable1, variable2, sampling_frequency, bool_spec): #if bool_spec = 1, calculation of cospectra is being performed

    #set bool_sepc in the function definitions equal to 1 if you want to calculate the cospectrum
    if bool_spec == 1:
        continue

    #if bool_spec is equal to zero we will enter the else statement and calculate the spectral energy
    else:

        samp_f = sampling_frequency #should be 20 the campbell CSAT3 sonic anemometers

        u = variable1 #redefine arbitrarily so easier to read
        v = variable2 #redefine arbitrarily so easier to read

        u_mean = sum(u)/len(u)
        v_mean = sum(v)/len(v)

        u = u - u_mean #get rid of the mean component of the flow so we are only assessing the fluctuations within the flow
        v = v - v_mean #get rid of the mean component of the flow so we are only assessing the fluctuations within the flow
        
        N = len(u) #number of points in the data
        N_f = len(u)//2 # nyquist number of points

        n_tila = samp_f*N_f//N #maximum reportable frequency

        delta_n_tilda = samp_f/N

        fk_u = np.fft(u) #calculate fourier coefficients
        fk_v = np.fft(v) #calculate fourier coefficients

        fk_u = fk_u/len(u) #normalize by scaling by length of your time/space series
        fk_v = fk_v/len(v) #normalize by scaling by length of your time/space series

        Euv_f = 2*fk_u*np.conj(fk_v) # 2 * to account for the folding over of frequencies past the nyquist frequency

        Suv_f = Euv_f/delta_n_tilda

        Suv_f = Suv_f[0:N_f]

        f = np.linspace(1,n_tilda,N_f)

        plt.loglog(f,Suv_f)

        plt.xlabel("Frequency")
        plt.ylabel("Power Spectral Density of ________") #insert which variable you are plugging in.
        plt.show()

spectra = np.vectorize(spectra)
