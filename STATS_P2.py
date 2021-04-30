import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import scipy.stats as stats
from utils import path_util



file1 = r'C:\Users\makom\source\repos\EFD_Final_Project\EFD_Final_Project\select_fields\sonic_data_2'
file2 = r'C:\Users\makom\source\repos\EFD_Final_Project\EFD_Final_Project\select_fields\sonic_data_5'
file3 = r'C:\Users\makom\source\repos\EFD_Final_Project\EFD_Final_Project\select_fields\sonic_data_10'

# file_dir = path_util.get_project_root() / "data" / "2021 Final Project Data" / "SonicData" / "select_fields"
# file1 = file_dir / "sonic_data_2"
# file2 = file_dir / "sonic_data_5"
# file3 = file_dir / "sonic_data_10"

sonic2 = pd.read_csv(file1, sep="\t", index_col=0)
print(sonic2)

sonic5 = pd.read_csv(file2, sep="\t", index_col=0)

sonic10 = pd.read_csv(file3, sep="\t", index_col=0)

u2 = np.array(sonic2['u'][0:396000].dropna())

v2 = np.array(sonic2['v'][0:396000].dropna())

w2 = np.array(sonic2['w'][0:396000].dropna())
#pd.to_numeric(w2, errors='coerce')
T2 = np.array(sonic2['virtual_temp'][0:396000].dropna())
pd.to_numeric(T2, errors='coerce')


u5 = np.array(sonic5['u'][0:396000].dropna())
#pd.to_numeric(u5, errors='coerce')
v5 = np.array(sonic5['v'][0:396000].dropna())
pd.to_numeric(v5, errors='coerce')
w5 = np.array(sonic5['w'][0:396000].dropna())
pd.to_numeric(w5, errors='coerce')
T5 = np.array(sonic5['virtual_temp'][0:396000].dropna())
pd.to_numeric(T5, errors='coerce')

u10 = np.array(sonic10['u'][0:396000].dropna())
#pd.to_numeric(u10, errors='coerce')
v10 = np.array(sonic10['v'][0:396000].dropna())
pd.to_numeric(v10, errors='coerce')
w10 = np.array(sonic10['w'][0:396000].dropna())
pd.to_numeric(w10, errors='coerce')
T10 = np.array(sonic10['virtual_temp'][0:396000].dropna())
pd.to_numeric(T10, errors='coerce')
print(np.nanmean(u5))
print(np.nanmean(v5))


def comp_stats(u_comp,v_comp, w_comp): #ignore the terrible naming, this is a generic funciton that will calculatie all the plots for any three indep 1-d array


    for i in range(len(u_comp)):
        if u_comp[i] < 10 or u_comp[i] > 25:
            u_comp[i] = math.nan
    for i in range(len(v_comp)):
        if v_comp[i] < 10 or v_comp[i] > 25:
            v_comp[i] = math.nan
    for i in range(len(w_comp)):
        if w_comp[i] < 10 or w_comp[i] > 25:
            w_comp[i] = math.nan

    def drop_nan(array):
        return array[np.logical_not(np.isnan(array))]
    u_comp = drop_nan(u_comp)
    v_comp = drop_nan(v_comp)
    w_comp = drop_nan(w_comp)


    N = len(u_comp) # number of measurements in column
    u_comp_mean = sum(u_comp)/N # mean of measurements

    u_comp_fluc = fluctuations(u_comp, u_comp_mean)
    u_comp_var = variance(N, u_comp_fluc)
    u_comp_std = standard_deviation(u_comp_var)
    u_comp_skew = skew(N, u_comp_fluc,
                       u_comp_std)
    u_comp_kurt = kurtosis(N, u_comp, u_comp_mean,
                           u_comp_std)

    print("The first moment of the data is: ", u_comp_mean)
    print("The second moment of the data is: ", u_comp_var)
    print("The standard deviation of the data is: ", u_comp_std)
    print("The third moment of the data is: ", u_comp_skew)
    print("The fourth moment of the data is: ", u_comp_kurt)

    x1 = np.linspace(10,25,100) #change the number of grid points if you want your distribution to be more or less discrete

    #Calculate Probability Density Function
    def pdf(x):
        P_x = (1/(u_comp_std*np.sqrt(2*math.pi)))*math.exp(-((x-u_comp_mean)**2)/(2*u_comp_std**2))
        return P_x

    pdf = np.vectorize(pdf)
    pdf1 = pdf(x1)


    #Calculate Cumulative Density Function
    cdf = np.zeros(len(pdf1))
    for i in range(len(pdf1)):
        if i == 0:
            cdf[i] = pdf1[i]
        else:
            cdf[i] = cdf[i-1]+pdf1[i]
    cdf1 = cdf/((len(x1)-1)/(25-10)) #multiply by spacial step

    #plot simple histogram
    bin_num = 50

    plt.hist(u_comp, bins = bin_num, density = True, histtype = 'step', label = "T-2m: Histogram")
    #plt.hist(u_comp, bins = bin_num, density = True, cumulative = True, histtype = 'bar', label = "Cumulative Histogram") 

    plt.plot(x1, pdf1, label = "T-2m: PDF") #plot the probability distribution function
    plt.plot(x1,cdf1, label = "T-2m: CDF") #plot the cumulative distribution function
    #plt.ticklabel_format(useOffset=False) #if your x axis looks weird, look up the library and play around with settings
    #plt.xlabel("U (m/s)") #change this to you variable of interest
    #plt.ylabel("Frequency")
    #plt.grid()
    #plt.legend()
    #plt.title("U - Component of Velocity")
    #plt.show()

    N = len(v_comp) # number of measurements in column
    v_comp_mean = sum(v_comp)/N # mean of measurements

    #list compreheson: super weird pythonic notation that allows you to basically write a for loop inside the list where you are storing the output
    v_comp_fluc = fluctuations(v_comp, v_comp_mean)  # fluctuation of each measurement

    v_comp_var = variance(N, v_comp_fluc)  #calcuv_compion of variance from squaring the fluctuations
    v_comp_std = standard_deviation(v_comp_var)  # the square root of the variance is the standard deviation
    v_comp_skew = skew(N, v_comp_fluc,
                       v_comp_std)
    v_comp_kurt = kurtosis(N, v_comp, v_comp_mean,
                           v_comp_std)  #calcuv_compion of kurtosis (the fourth moment) using list comprehension, the minus 3 is because the normal distribution has a value of 3... therefore the value returned from your data is in reference to the kurtosis of the normal distribution.

    print("The first moment of the data is: ", v_comp_mean)
    print("The second moment of the data is: ", v_comp_var)
    print("The standard deviation of the data is: ", v_comp_std)
    print("The third moment of the data is: ", v_comp_skew)
    print("The fourth moment of the data is: ", v_comp_kurt)

    x2 = np.linspace(10,25,100) #change the number of grid points if you want your distribution to be more or less discrete

    #Calculate Probability Density Function
    def pdf(x):
        P_x = (1/(v_comp_std*np.sqrt(2*math.pi)))*math.exp(-((x-v_comp_mean)**2)/(2*v_comp_std**2))
        return P_x

    pdf = np.vectorize(pdf)
    pdf2 = pdf(x2)


    #Calculate Cumulative Density Function
    cdf = np.zeros(len(pdf2))
    for i in range(len(pdf2)):
        if i == 0:
            cdf[i] = pdf2[i]
        else:
            cdf[i] = cdf[i-1]+pdf2[i]
    cdf2 = cdf/((len(x2)-1)/(25-10)) #multiply by spacial step

    #plot simple histogram
    bin_num = 50
    print(bin_num)
    plt.hist(v_comp, bins = bin_num, density = True, histtype = 'step', label = "T-5m: Histogram")
    #plt.hist(v_comp, bins = bin_num, density = True, cumulative = True, histtype = 'bar', label = "Cumulative Histogram") 

    plt.plot(x2, pdf2, label = "T-5m: PDF") #plot the probability distribution function
    plt.plot(x2, cdf2, label = "T-5m: CDF") #plot the cumulative distribution function
    #plt.ticklabel_format(useOffset=False) #if your x axis looks weird, look up the library and play around with settings
    #plt.xlabel("V (m/s)") #change this to you variable of interest
    #plt.ylabel("Frequency")
    #plt.grid()
    #plt.legend()
    #plt.title("V - Component of Velocity")
    #plt.show()

    N = len(w_comp) # number of measurements in column
    w_comp_mean = sum(w_comp)/N # mean of measurements

    #list compreheson: super weird pythonic notation that allows you to basically write a for loop inside the list where you are storing the output
    w_comp_fluc = fluctuations(w_comp, w_comp_mean)
    w_comp_var = variance(N, w_comp_fluc)  #calcuw_compion of variance from squaring the fluctuations
    w_comp_std = standard_deviation(w_comp_var)
    w_comp_skew = skew(N, w_comp_fluc,
                       w_comp_std)  #calcuw_compion of skewness (the third moment) using list comprehension
    w_comp_kurt = kurtosis(N, w_comp, w_comp_mean,
                           w_comp_std)

    print("The first moment of the data is: ", w_comp_mean)
    print("The second moment of the data is: ", w_comp_var)
    print("The standard deviation of the data is: ", w_comp_std)
    print("The third moment of the data is: ", w_comp_skew)
    print("The fourth moment of the data is: ", w_comp_kurt)

    x3 = np.linspace(10,25,100) #change the number of grid points if you want your distribution to be more or less discrete

    #Calculate Probability Density Function
    def pdf(x):
        P_x = (1/(w_comp_std*np.sqrt(2*math.pi)))*math.exp(-((x-w_comp_mean)**2)/(2*w_comp_std**2))
        return P_x

    pdf = np.vectorize(pdf)
    pdf3 = pdf(x3)


    #Calculate Cumulative Density Function
    cdf = np.zeros(len(pdf3))
    for i in range(len(pdf3)):
        if i == 0:
            cdf[i] = pdf3[i]
        else:
            cdf[i] = cdf[i-1]+pdf3[i]
    cdf3 = cdf/((len(x3)-1)/(25-10)) #multiply by spacial step

    #plot simple histogram
    bin_num = 50
    print(bin_num)
    plt.hist(w_comp, bins = bin_num, density = True, histtype = 'step', label = "T-10m: Histogram")
    #plt.hist(w_comp, bins = bin_num, density = True, cumulative = True, histtype = 'bar', label = "Cumulative Histogram") 

    skew2 = "The Skewness at 2m: "
    skew5 = "The Skewness at 5m: "
    skew10 = "The Skewness at 10m: "
    
    kurt2 = "The Kurtosis at 2m: "
    kurt5 = "The Kurtosis at 5m: "
    kurt10 = "The Kurtosis at 10m: "
    plt.text(12.5, 0.65, skew2+str('{0:.3g}'.format(u_comp_skew)))
    plt.text(12.5, 0.6, skew5+str('{0:.3g}'.format(v_comp_skew)))
    plt.text(12.5, 0.55, skew10+str('{0:.3g}'.format(w_comp_skew)))

    plt.text(12.5, 0.5, kurt2+str('{0:.3g}'.format(u_comp_kurt)))
    plt.text(12.5, 0.45, kurt5+str('{0:.3g}'.format(v_comp_kurt)))
    plt.text(12.5, 0.4, kurt10+str('{0:.3g}'.format(w_comp_kurt)))



    plt.plot(x3,pdf3, label = "T-10m: PDF") #plot the probability distribution function
    plt.plot(x3,cdf3, label = "T-10m: CDF") #plot the cumulative distribution function
    plt.ticklabel_format(useOffset=False) #if your x axis looks weird, look up the library and play around with settings
    plt.xlabel("Temperature") #change this to you variable of interest
    plt.ylabel("Frequency")
    plt.grid()
    plt.title("Temperature During Fog Event")
    plt.legend(loc = "upper left")
    plt.show()


def standard_deviation(variance):
    """
    the square root of the variance is the standard deviation
    """
    return variance ** (1 / 2)


def variance(N, fluctuations):
    return sum(x ** 2 for x in fluctuations) / (N - 1)


def fluctuations(data, mean):
    return [x - mean for x in data]


def skew(N, fluctuations, std):
    """
    calculate skewness (the third moment) using list comprehension
    """
    return sum(x ** 3 for x in fluctuations) / ((N - 1) * std ** 3)


def kurtosis(N, data, mean, std):
    """
    calculate kurtosis (the fourth moment) using list comprehension, the minus 3 is because the
    normal distribution has a value of 3... therefore the value returned from your data is in reference
    to the kurtosis of the normal distribution.
    """
    return (sum((x - mean) ** 4 for x in data) / std ** 4 / N) - 3


U = comp_stats(T2,T5,T10)
