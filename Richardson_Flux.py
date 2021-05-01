import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from utils import path_util


# file1 = r'C:\Users\makom\source\repos\EFD_Final_Project\EFD_Final_Project\select_fields\sonic_data_2'
# file2 = r'C:\Users\makom\source\repos\EFD_Final_Project\EFD_Final_Project\select_fields\sonic_data_5'
# file3 = r'C:\Users\makom\source\repos\EFD_Final_Project\EFD_Final_Project\select_fields\sonic_data_10'

file_dir = path_util.get_project_root() / "data" / "2021 Final Project Data" / "SonicData" / "select_fields"
file1 = file_dir / "sonic_data_2"
file2 = file_dir / "sonic_data_5"
file3 = file_dir / "sonic_data_10"


def load_data(file):
    return pd.read_csv(file, sep="\t", index_col=0, parse_dates=["time"])


sonic2 = load_data(file1)
sonic5 = load_data(file2)
sonic10 = load_data(file3)


def correct_time(data):
    data["time"] = data["time"] - datetime.timedelta(days=366)
    # data = data[(data["time"] >= pd.Timestamp('2018-09-13 21:00:00')) &
    #             (data["time"] <= pd.Timestamp('2018-09-14 06:00:00'))]
    return data


sonic2 = correct_time(sonic2)
sonic5 = correct_time(sonic5)
sonic10 = correct_time(sonic10)

time = sonic2['time'].to_numpy()
print(time)
u2 = pd.to_numeric(sonic2['u'], errors='coerce')
u2 = np.array(u2)
v2 = pd.to_numeric(sonic2['v'], errors='coerce')
v2 = np.array(v2)
w2 = pd.to_numeric(sonic2['w'], errors='coerce')
w2 = np.array(w2)
T2 = pd.to_numeric(sonic2['virtual_temp'], errors='coerce') #NOTE :is the virtual temp at sea level
T2 = np.array(T2)

u5 = pd.to_numeric(sonic5['u'], errors='coerce')
u5 = np.array(u5)
v5 = pd.to_numeric(sonic5['v'], errors='coerce')
v5 = np.array(v5)
w5 = pd.to_numeric(sonic5['w'], errors='coerce')
w5 = np.array(w5)
T5 = pd.to_numeric(sonic5['virtual_temp'], errors='coerce') #NOTE :is the virtual temp at sea level
T5 = np.array(T5)

u10 = pd.to_numeric(sonic10['u'], errors='coerce')
u10 = np.array(u10)
v10 = pd.to_numeric(sonic10['v'], errors='coerce')
v10 = np.array(v10)
w10 = pd.to_numeric(sonic10['w'], errors='coerce')
w10 = np.array(w10)
T10 = pd.to_numeric(sonic10['virtual_temp'], errors='coerce') #NOTE :is the virtual temp at sea level
T10 = np.array(T10)

def align_u(u,v):
    u1 = np.zeros(len(u))
    v1 = np.zeros(len(v))
    dir  = np.zeros(len(u))

    u_m = np.nanmean(u)
    v_m = np.nanmean(v)

    # quadrant I
    if u_m > 0 and v_m > 0:
        x = u_m
        y = v_m
        h = (x**2+y**2)**(1/2)

        theta = np.degrees(np.arccos(x/h))
        #print(theta)

        x1 = x*np.cos(np.radians(360-theta))-y*np.sin(np.radians(360-theta))
        y1 = x*np.sin(np.radians(360-theta))+y*np.cos(np.radians(360-theta))

    # quadrant 2
    if u_m < 0 and v_m > 0:
        x = u_m
        y = v_m
        h = (x**2+y**2)**(1/2)

        theta = np.degrees(np.arccos(x/h))
        #print(theta)

        x1 = x*np.cos(np.radians(360-theta))-y*np.sin(np.radians(360-theta))
        y1 = x*np.sin(np.radians(360-theta))+y*np.cos(np.radians(360-theta))
 
    # quadrant 3
    if u_m < 0 and v_m < 0:
        x = u_m
        y = v_m
        h = (x**2+y**2)**(1/2)

        theta = -np.degrees(np.arcsin(y/h))+180
        #print(theta)

        x1 = x*np.cos(np.radians(360-theta))-y*np.sin(np.radians(360-theta))
        y1 = x*np.sin(np.radians(360-theta))+y*np.cos(np.radians(360-theta))

    # quadrant 4
    if u_m > 0 and v_m < 0:
        x = u_m
        y = v_m
        h = (x**2+y**2)**(1/2)

        theta = (90+np.degrees(np.arcsin(y/h)))+270
        #print(theta)

        x1 = x*np.cos(np.radians(360-theta))-y*np.sin(np.radians(360-theta))
        y1 = x*np.sin(np.radians(360-theta))+y*np.cos(np.radians(360-theta))
        print("here", x1, y1)

    #throw out bad values... lets be real honest, a Campbell Scientific CSAT3 does not produce 0's 
    if u_m == np.nan or v_m == np.nan or v_m == 0 or u_m == 0:
        x1 = np.nan
        y1 = np.nan
        theta = np.nan



    return [x1, y1, theta]

#code is written to pass in raw u,v data with everything in numpy formats to deal with bad data
def rotate_array(u,v,theta):
        x = u
        y = v

        x1 = x*np.cos(np.radians(360-theta))-y*np.sin(np.radians(360-theta))
        y1 = x*np.sin(np.radians(360-theta))+y*np.cos(np.radians(360-theta))

        return [x1, y1]

#print(np.nanmean(u5))
#print(np.nanmean(v5))
#print(align_u(u5,v5))

#u5a = align_u(u5,v5) #mean aligned along u returns mean u, mean v (which is now 0), and theta for rotation operation in align array

#u5r = rotate_array(u5,v5,u5a[2]) #all data rotated, index 0 is u and index 1 is v

avg_period = 20*60*10 # (sampling frequency)*(seconds in minute)*(minutes in window)

Ri_2 = [] # container for richardson numbers at 2 m
Ri_5 = [] # container for richardson numbers at 5 m
Ri_10 = [] # container for richarason number at 10 m
Ri_time = [] 
for i in range(0,len(u2),avg_period):

    g = 9.81 #gravity
  
    #ALL 3 SENSORS ARE ROTATED BY THE ROTATION NEEDED TO ALIGN 10 METER SONIC BECAUSE IT IS THE PREVAILING WIND, YOU SHOULD NOT ALIGN EACH INSTRAMENT, YOU WOULD BE GIVING EACH SONIC ITS OWN COORDINATE SYSTEM

    u10i = u10[i:i+avg_period] #extract window to be averaged
    v10i = v10[i:i+avg_period]
    u10im = align_u(u10i,v10i) #align mean wind speed with x axis and compute the theta needed to transform window values to align with u
    u10ir = rotate_array(u10i,v10i, u10im[2]) #rotate window of x and y so that mean of v fluctuations within the window is 0
    u10ip = u10ir[0]-u10im[0] #calculate the primes of u
    #print(u10ip)

    Ri_time.append(time[i]) #create time array of equal length to RI array
    
    u2i = u2[i:i+avg_period] #extract window to be averaged
    v2i = v2[i:i+avg_period] #v component window index i
    u2im = align_u(u2i,v2i) #align mean wind speed with x axis and compute the theta needed to transform window values to align with u
    u2ir = rotate_array(u2i,v2i, u10im[2]) #rotate window of x and y so that mean of v fluctuations within the window is 0
    u2ip = u2ir[0]-u2im[0] #calculate the primes of u
    #print(u2ip)

    u5i = u5[i:i+avg_period] #extract window to be averaged
    v5i = v5[i:i+avg_period]
    u5im = align_u(u5i,v5i) #align mean wind speed with x axis and compute the theta needed to transform window values to align with u
    u5ir = rotate_array(u5i,v5i, u10im[2]) #rotate window of x and y so that mean of v fluctuations within the window is 0
    u5ip = u5ir[0]-u5im[0] #calculate the primes of u
    #print(u5ip)

    w2i = w2[i:i+avg_period]
    w2im = np.nanmean(w2i)
    w2ip = w2i-w2im
    #print(w2ip)

    T2i = T2[i:i+avg_period]
    T2im = np.nanmean(T2i)
    T2ip = T2i - T2im
    #print(T2ip)

    dudz2 = (u2im[0]-0)/(2-0) #Euler forward in space approximation for the average velocity gradient
    Ri2 = (g/T2im)*np.nanmean(w2ip*T2ip)/(np.nanmean(u2ip*w2ip)*dudz2)
    #print(Ri2)
    Ri_2.append(Ri2)

    w5i = w5[i:i+avg_period]
    w5im = np.nanmean(w5i)
    w5ip = w5i-w5im
    #print(w5ip)

    T5i = T5[i:i+avg_period]
    T5im = np.nanmean(T5i)
    T5ip = T5i - T5im
    #print(T5ip)

    dudz5 = (u5im[0]-u2im[0])/(5-2) #Euler forward in space approximation for the average velocity gradient
    Ri5 = (g/T5im)*np.nanmean(w5ip*T5ip)/(np.nanmean(u5ip*w5ip)*dudz5)
    #print(Ri5)
    Ri_5.append(Ri5)

    w10i = w10[i:i+avg_period]
    w10im = np.nanmean(w10i)
    w10ip = w10i-w10im
    #print(w10ip)

    T10i = T10[i:i+avg_period]
    T10im = np.nanmean(T10i)
    T10ip = T10i - T10im
    #print(T10ip)

    dudz10 = (u10im[0]-u5im[0])/(10-5) #Euler forward in space approximation for the average velocity gradient
    Ri10 = (g/T10im)*np.nanmean(w10ip*T10ip)/(np.nanmean(u10ip*w10ip)*dudz10)
    #print(Ri10)
    Ri_10.append(Ri10)

#limit the range of Richards numbers to relavent values values greater than 10 are excluded, negative values generally mean Ri no longer good measurement
for i in range(len(Ri_5)):
    if Ri_2[i] > 10:
        Ri_2[i] = 10
    if Ri_2[i] < -5:
        Ri_2[i] = -5
    if Ri_5[i] > 10:
        Ri_5[i] = 10
    if Ri_5[i] < -5:
        Ri_5[i] = -5
    if Ri_10[i] > 10:
        Ri_10[i] = 10
    if Ri_10[i] < -5:
        Ri_10[i] = -5

fig, ax = plt.subplots()
plt.plot(Ri_time, Ri_2, "r-", label = "Ri # @ 2-meters")
plt.plot(Ri_time, Ri_5, "b-", label = "Ri # @ 5-meters")
plt.plot(Ri_time, Ri_10,"g-", label = "Ri # @ 10-meters")
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.HourLocator()))
from calculations.simple_time_averaging import get_dissipation_formation_times
dissipation, formation = get_dissipation_formation_times()
for line1, line2 in zip(formation, dissipation):
    ax.axvspan(line1, line2, alpha=0.2, color='blue')

ax.yaxis.set_major_locator(plt.MaxNLocator(20)) #number of ticks on the y-axis set to 20
plt.xlim(pd.Timestamp('2018-09-13 21:00:00'), pd.Timestamp('2018-09-14 06:00:00'))
plt.ylabel('Richardson Number')
plt.title("10-Minute Average Richardson Flux During Fog Event")
plt.legend()
plt.grid()
fig.set_size_inches(10, 4)
plt.show()
