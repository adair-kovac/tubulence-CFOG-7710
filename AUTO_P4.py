import numpy as np
import matplotlib.pyplot as plt

U = np.random.normal(5, 1, 1000) # Insert 30-min U period here
V = np.random.normal(5, 1, 1000) # Insert 30-min V period here
W = np.random.normal(5, 1, 1000) # Insert 30-min W period here
T = np.random.normal(5, 1, 1000) # Insert 30-min T period here

mean = sum(U)/len(U)
auto_corr_lag_U = []
auto_corr_denominator = sum((x-mean)**2 for x in U)
dt = 1/20 # 20 Hz
time = np.arange(0,len(U))
time = time*dt
#Assumption made: Data are sufficiently stationary (or homogeneous in space)
for j in range(len(U)): # time lag
    lag =[]
    for k in range(0,len(U)-j):
        index = (U[k]-mean)*(U[k+j]-mean)
        lag.append(index)
    auto_corr_lag_U.append(sum(lag)/auto_corr_denominator)

mean = sum(V)/len(V)
auto_corr_lag_V = []
auto_corr_denominator = sum((x-mean)**2 for x in V)
dt = 1/20 # 20 Hz
time = np.arange(0,len(V))
time = time*dt
#Assumption made: Data are sufficiently stationary (or homogeneous in space)
for j in range(len(V)): # time lag
    lag =[]
    for k in range(0,len(V)-j):
        index = (V[k]-mean)*(V[k+j]-mean)
        lag.append(index)
    auto_corr_lag_V.append(sum(lag)/auto_corr_denominator)

mean = sum(W)/len(W)
auto_corr_lag_W = []
auto_corr_denominator = sum((x-mean)**2 for x in W)
dt = 1/20 # 20 Hz
time = np.arange(0,len(W))
time = time*dt
#Assumption made: Data are sufficiently stationary (or homogeneous in space)
for j in range(len(W)): # time lag
    lag =[]
    for k in range(0,len(W)-j):
        index = (W[k]-mean)*(W[k+j]-mean)
        lag.append(index)
    auto_corr_lag_W.append(sum(lag)/auto_corr_denominator)

mean = sum(T)/len(T)
auto_corr_lag_T = []
auto_corr_denominator = sum((x-mean)**2 for x in T)
dt = 1/20 # 20 Hz
time = np.arange(0,len(T))
time = time*dt
#Assumption made: Data are sufficiently stationary (or homogeneous in space)
for j in range(len(T)): # time lag
    lag =[]
    for k in range(0,len(T)-j):
        index = (T[k]-mean)*(T[k+j]-mean)
        lag.append(index)
    auto_corr_lag_T.append(sum(lag)/auto_corr_denominator)

plt.plot(time,auto_corr_lag_U, label = "U velocity")
plt.plot(time,auto_corr_lag_V, label = "V velocity")
plt.plot(time,auto_corr_lag_W, label = "W velocity")
plt.plot(time,auto_corr_lag_T, label = "Temperature")
plt.ylabel('Autocorrelation')
plt.xlabel("Lag (seconds)")
plt.legend()
plt.grid()
plt.title("Autocorrelation vs. Lag")
plt.show()
