## ------------------------------------------ C.B. Matt Huckins --------------------------------------------------------

import numpy as np
import math
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.stats import norm

u_comp = np.random.normal(5, 1, 1000) #rename column 1 as what you want
v_comp = np.random.normal(5, 1, 1000) #rename column 2 as what you want
w_comp = np.random.normal(5, 1, 1000) #rename column 3 as what you want
T_comp = np.random.normal(5, 1, 1000) #rename column 4 as what you want

N = len(u_comp) # number of measurements in column
u_comp_mean = sum(u_comp)/N # mean of measurements

#list compreheson: super weird pythonic notation that allows you to basically write a for loop inside the list where you are storing the output
u_comp_fluc = [x-u_comp_mean for x in u_comp] # fluctuation of each measurement

u_comp_var = sum(x**2 for x in u_comp_fluc)/(N-1) #calcuu_compion of variance from squaring the fluctuations
u_comp_std = u_comp_var**(1/2) # the square root of the variance is the standard deviation
u_comp_skew = sum(x**3 for x in u_comp_fluc)/((N-1)*u_comp_std**3) #calcuu_compion of skewness (the third moment) using list comprehension
u_comp_kurt = (sum((x-u_comp_mean)**4 for x in u_comp)/u_comp_std**4/N)-3 #calcuu_compion of kurtosis (the fourth moment) using list comprehension, the minus 3 is because the normal distribution has a value of 3... therefore the value returned from your data is in reference to the kurtosis of the normal distribution.

print("The first moment of the data is: ", u_comp_mean)
print("The second moment of the data is: ", u_comp_var)
print("The standard deviation of the data is: ", u_comp_std)
print("The third moment of the data is: ", u_comp_skew)
print("The fourth moment of the data is: ", u_comp_kurt)

x = np.linspace(min(u_comp),max(u_comp),100) #change the number of grid points if you want your distribution to be more or less discrete

#Calculate Probability Density Function
def pdf(x):
    P_x = (1/(u_comp_std*np.sqrt(2*math.pi)))*math.exp(-((x-u_comp_mean)**2)/(2*u_comp_std**2))
    return P_x

pdf = np.vectorize(pdf)
pdf = pdf(x)
print(pdf)

#Calculate Cumulative Density Function
cdf = np.zeros(len(pdf))
for i in range(len(pdf)):
    if i == 0:
        cdf[i] = pdf[i]
    else:
        cdf[i] = cdf[i-1]+pdf[i]
cdf = cdf/((len(x)-1)/(max(u_comp)-min(u_comp))) #multiply by spacial step

#plot simple histogram
bin_num = 25
print(bin_num)
plt.hist(u_comp, bins = bin_num, density = True, histtype = 'bar', label = "Histogram")
#plt.hist(u_comp, bins = bin_num, density = True, cumulative = True, histtype = 'bar', label = "Cumulative Histogram") 

plt.plot(x, pdf, 'r-', label = "Probability Density Function") #plot the probability distribution function
plt.plot(x,cdf, label = "Cumulative Density Function") #plot the cumulative distribution function
plt.ticklabel_format(useOffset=False) #if your x axis looks weird, look up the library and play around with settings
plt.xlabel("U (m/s)") #change this to you variable of interest
plt.ylabel("Frequency")
plt.grid()
plt.legend()
plt.title("U - Component of Velocity")
plt.show()



N = len(v_comp) # number of measurements in column
v_comp_mean = sum(v_comp)/N # mean of measurements

#list compreheson: super weird pythonic notation that allows you to basically write a for loop inside the list where you are storing the output
v_comp_fluc = [x-v_comp_mean for x in v_comp] # fluctuation of each measurement

v_comp_var = sum(x**2 for x in v_comp_fluc)/(N-1) #calcuv_compion of variance from squaring the fluctuations
v_comp_std = v_comp_var**(1/2) # the square root of the variance is the standard deviation
v_comp_skew = sum(x**3 for x in v_comp_fluc)/((N-1)*v_comp_std**3) #calcuv_compion of skewness (the third moment) using list comprehension
v_comp_kurt = (sum((x-v_comp_mean)**4 for x in v_comp)/v_comp_std**4/N)-3 #calcuv_compion of kurtosis (the fourth moment) using list comprehension, the minus 3 is because the normal distribution has a value of 3... therefore the value returned from your data is in reference to the kurtosis of the normal distribution.

print("The first moment of the data is: ", v_comp_mean)
print("The second moment of the data is: ", v_comp_var)
print("The standard deviation of the data is: ", v_comp_std)
print("The third moment of the data is: ", v_comp_skew)
print("The fourth moment of the data is: ", v_comp_kurt)

x = np.linspace(min(v_comp),max(v_comp),100) #change the number of grid points if you want your distribution to be more or less discrete

#Calculate Probability Density Function
def pdf(x):
    P_x = (1/(v_comp_std*np.sqrt(2*math.pi)))*math.exp(-((x-v_comp_mean)**2)/(2*v_comp_std**2))
    return P_x

pdf = np.vectorize(pdf)
pdf = pdf(x)
print(pdf)

#Calculate Cumulative Density Function
cdf = np.zeros(len(pdf))
for i in range(len(pdf)):
    if i == 0:
        cdf[i] = pdf[i]
    else:
        cdf[i] = cdf[i-1]+pdf[i]
cdf = cdf/((len(x)-1)/(max(v_comp)-min(v_comp))) #multiply by spacial step

#plot simple histogram
bin_num = 25
print(bin_num)
plt.hist(v_comp, bins = bin_num, density = True, histtype = 'bar', label = "Histogram")
#plt.hist(v_comp, bins = bin_num, density = True, cumulative = True, histtype = 'bar', label = "Cumulative Histogram") 

plt.plot(x, pdf, 'r-', label = "Probability Density Function") #plot the probability distribution function
plt.plot(x,cdf, label = "Cumulative Density Function") #plot the cumulative distribution function
plt.ticklabel_format(useOffset=False) #if your x axis looks weird, look up the library and play around with settings
plt.xlabel("V (m/s)") #change this to you variable of interest
plt.ylabel("Frequency")
plt.grid()
plt.legend()
plt.title("V - Component of Velocity")
plt.show()

N = len(w_comp) # number of measurements in column
w_comp_mean = sum(w_comp)/N # mean of measurements

#list compreheson: super weird pythonic notation that allows you to basically write a for loop inside the list where you are storing the output
w_comp_fluc = [x-w_comp_mean for x in w_comp] # fluctuation of each measurement

w_comp_var = sum(x**2 for x in w_comp_fluc)/(N-1) #calcuw_compion of variance from squaring the fluctuations
w_comp_std = w_comp_var**(1/2) # the square root of the variance is the standard deviation
w_comp_skew = sum(x**3 for x in w_comp_fluc)/((N-1)*w_comp_std**3) #calcuw_compion of skewness (the third moment) using list comprehension
w_comp_kurt = (sum((x-w_comp_mean)**4 for x in w_comp)/w_comp_std**4/N)-3 #calcuw_compion of kurtosis (the fourth moment) using list comprehension, the minus 3 is because the normal distribution has a value of 3... therefore the value returned from your data is in reference to the kurtosis of the normal distribution.

print("The first moment of the data is: ", w_comp_mean)
print("The second moment of the data is: ", w_comp_var)
print("The standard deviation of the data is: ", w_comp_std)
print("The third moment of the data is: ", w_comp_skew)
print("The fourth moment of the data is: ", w_comp_kurt)

x = np.linspace(min(w_comp),max(w_comp),100) #change the number of grid points if you want your distribution to be more or less discrete

#Calculate Probability Density Function
def pdf(x):
    P_x = (1/(w_comp_std*np.sqrt(2*math.pi)))*math.exp(-((x-w_comp_mean)**2)/(2*w_comp_std**2))
    return P_x

pdf = np.vectorize(pdf)
pdf = pdf(x)
print(pdf)

#Calculate Cumulative Density Function
cdf = np.zeros(len(pdf))
for i in range(len(pdf)):
    if i == 0:
        cdf[i] = pdf[i]
    else:
        cdf[i] = cdf[i-1]+pdf[i]
cdf = cdf/((len(x)-1)/(max(w_comp)-min(w_comp))) #multiply by spacial step

#plot simple histogram
bin_num = 25
print(bin_num)
plt.hist(w_comp, bins = bin_num, density = True, histtype = 'bar', label = "Histogram")
#plt.hist(w_comp, bins = bin_num, density = True, cumulative = True, histtype = 'bar', label = "Cumulative Histogram") 

plt.plot(x, pdf, 'r-', label = "Probability Density Function") #plot the probability distribution function
plt.plot(x,cdf, label = "Cumulative Density Function") #plot the cumulative distribution function
plt.ticklabel_format(useOffset=False) #if your x axis looks weird, look up the library and play around with settings
plt.xlabel("W (m/s)") #change this to you variable of interest
plt.ylabel("Frequency")
plt.grid()
plt.legend()
plt.title("W - Component of Velocity")
plt.show()

N = len(T_comp) # number of measurements in column
T_comp_mean = sum(T_comp)/N # mean of measurements

#list compreheson: super weird pythonic notation that allows you to basically write a for loop inside the list where you are storing the output
T_comp_fluc = [x-T_comp_mean for x in T_comp] # fluctuation of each measurement

T_comp_var = sum(x**2 for x in T_comp_fluc)/(N-1) #calcuT_compion of variance from squaring the fluctuations
T_comp_std = T_comp_var**(1/2) # the square root of the variance is the standard deviation
T_comp_skew = sum(x**3 for x in T_comp_fluc)/((N-1)*T_comp_std**3) #calcuT_compion of skewness (the third moment) using list comprehension
T_comp_kurt = (sum((x-T_comp_mean)**4 for x in T_comp)/T_comp_std**4/N)-3 #calcuT_compion of kurtosis (the fourth moment) using list comprehension, the minus 3 is because the normal distribution has a value of 3... therefore the value returned from your data is in reference to the kurtosis of the normal distribution.

print("The first moment of the data is: ", T_comp_mean)
print("The second moment of the data is: ", T_comp_var)
print("The standard deviation of the data is: ", T_comp_std)
print("The third moment of the data is: ", T_comp_skew)
print("The fourth moment of the data is: ", T_comp_kurt)

x = np.linspace(min(T_comp),max(T_comp),100) #change the number of grid points if you want your distribution to be more or less discrete

#Calculate Probability Density Function
def pdf(x):
    P_x = (1/(T_comp_std*np.sqrt(2*math.pi)))*math.exp(-((x-T_comp_mean)**2)/(2*T_comp_std**2))
    return P_x

pdf = np.vectorize(pdf)
pdf = pdf(x)
print(pdf)

#Calculate Cumulative Density Function
cdf = np.zeros(len(pdf))
for i in range(len(pdf)):
    if i == 0:
        cdf[i] = pdf[i]
    else:
        cdf[i] = cdf[i-1]+pdf[i]
cdf = cdf/((len(x)-1)/(max(T_comp)-min(T_comp))) #multiply by spacial step

#plot simple histogram
bin_num = 25
print(bin_num)
plt.hist(T_comp, bins = bin_num, density = True, histtype = 'bar', label = "Histogram")
#plt.hist(T_comp, bins = bin_num, density = True, cumulative = True, histtype = 'bar', label = "Cumulative Histogram") 

plt.plot(x, pdf, 'r-', label = "Probability Density Function") #plot the probability distribution function
plt.plot(x,cdf, label = "Cumulative Density Function") #plot the cumulative distribution function
plt.ticklabel_format(useOffset=False) #if your x axis looks weird, look up the library and play around with settings
plt.xlabel("T (K)") #change this to you variable of interest
plt.ylabel("Frequency")
plt.grid()
plt.legend()
plt.title("Temperature")
plt.show()
