
# coding: utf-8

# In[10]:


# Functions for Q1

import numpy as np
import datetime
import pandas as pd


def compute_avg_with_start_times(start_time, column_name, A, Hz=20, dt=30):
    values = compute_avg(A, Hz, dt)
    return create_dataframe(column_name, dt, start_time, values)

def compute_std_with_start_times(start_time, column_name, A, Hz=20, dt=30):
    values = std_dev(A, Hz, dt)
    return create_dataframe(column_name, dt, start_time, values)


def create_dataframe(column_name, dt, start_time, values):
    count = 0
    times = []
    for value in values:
        minutes = dt * count
        new_time = start_time + datetime.timedelta(minutes=minutes)
        times.append(new_time)
        count += 1
    result = pd.DataFrame()
    result["time"] = times
    result[column_name] = values
    return result


def compute_avg(A, Hz=20, dt=30):
    # Compute averages of variable A; default to data taken at 20 Hz and 30 minute averages
    N=len(A)
    P=(dt*60)*Hz
    M=int(N/P)
    A_bar=np.zeros(M)
    for i in range(0,M):
        start=i*P
        end=(i+1)*P
        count = 0
        for j in range(start,end):
            if np.isnan(A[j]):
               # print("Skipping value at {}, NaN".format(j))
                pass
            else:
                A_bar[i] = A_bar[i]+A[j]
                count += 1
        A_bar[i]=A_bar[i]/count
    return A_bar
    
def compute_prime(A, A_bar, Hz=20, dt=30):
    # Compute fluctuation of variable A; default to data taken at 20 Hz and 30 minute averages
    
    N=len(A)
    P=(dt*60)*Hz
    M= int(N/P)
    A_prime=np.zeros(N)
    for i in range(0,M):
        start=i*P
        end=(i+1)*P
        for j in range(start,end):
            if A[j]:
                A_prime[j]=A[j]-A_bar[i]
    return A_prime
    
def wind_speed_avg(u, v, w, Hz=20, dt=30):
    # Compute averages of wind speed; default to data taken at 20 Hz and 30 minute averages
    
    ws=((u**2)+(v**2)+(w**2))**(1/2)
    ws_bar=compute_avg(ws, Hz=Hz, dt=dt)
    return ws_bar

def std_dev(A_prime, Hz=20, dt=30):
    # Compute standard deviation of variable A; default to data taken at 20 Hz and 30 minute averages
    
    square_fluc=A_prime*A_prime
    arg=compute_avg(square_fluc, Hz=Hz, dt=dt)
    sigma_A=arg**(1/2)
    return sigma_A

def kinematic_temp_flux(w_prime, T_prime, Hz=20, dt=30):
    # Compute kinematic temperature flux; default to data taken at 20 Hz and 30 minute averages
    
    arg=w_prime*T_prime
    wprime_Tprime_bar=compute_avg(arg, Hz=Hz, dt=dt)
    return wprime_Tprime_bar

def friction_velocity(u_prime, v_prime, ws_prime, Hz=20, dt=30):
    # Compute friction velocity; default to data taken at 20 Hz and 30 minute averages
    
    arg1=u_prime*ws_prime
    arg2=v_prime*ws_prime
    avg1=compute_avg(arg1, Hz=Hz, dt=dt)
    avg2=compute_avg(arg2, Hz=Hz, dt=dt)
    u_star=((avg1**2)+(avg2**2))**(1/4)
    return u_star

def sensible_heat_flux(wprime_Tprime_bar, rho, c_p):
    # Compute sensible heat flux
    H_s=rho*c_p*wprime_Tprime_bar
    return H_s

def compute_tke(u_prime, v_prime, w_prime, Hz=20, dt=30):
    # Compute turbulence kinetic energy; default to data taken at 20 Hz and 30 minute averages
    
    arg1=u_prime*u_prime
    arg2=v_prime*v_prime
    arg3=w_prime*w_prime
    avg1=compute_avg(arg1, Hz=Hz, dt=dt)
    avg2=compute_avg(arg2, Hz=Hz, dt=dt)
    avg3=compute_avg(arg3, Hz=Hz, dt=dt)
    tke=(1/2)*(avg1+avg2+avg3)
    return tke

def obukhov_length(theta_v_bar, u_star, w_prime_surface, theta_v_prime_surface, Hz=20, dt=30):
    # Compute Obukhov length; default to data taken at 20 Hz and 30 minute averages
    
    k=0.4
    g=9.81
    arg=w_prime_surface*theta_v_prime_surface
    avg=compute_avg(arg, Hz=Hz, dt=dt)
    L=(-theta_v_bar*(u_star**3))/(k*g*avg)
    return L

def convective_velocity_scale(z, theta_v_bar, ws_prime,theta_v_prime_surface, Hz=20, dt=30):
    # Compute convective velocity scale; default to data taken at 20 Hz and 30 minute averages
    
    g=9.81
    arg=ws_prime*theta_v_prime_surface
    avg=compute_avg(arg, Hz=Hz, dt=dt)
    w_star=(g*z*avg/theta_v_bar)**(1/3) # Need to edit this once z structure is known!
    return w_star

def dissipation_rate(z, theta_v_bar, theta_v_prime, u_prime, v_prime, w_prime, ws_bar_2, ws_bar_5, ws_bar_10, Hz=20, dt=30):
    # Compute dissipation rate; default to data taken at 20 Hz and 30 minute averages
    
    g=9.81
    arg1=w_prime*theta_v_prime
    arg2=u_prime*w_prime
    avg1=compute_avg(arg1, Hz=20, dt=30)
    avg2=compute_avg(arg2, Hz=20, dt=30)
    if z==2 :
        dU_dz=(-3*ws_bar_2+4*ws_bar_5-ws_bar_10)/8
    elif z==5 :
        dU_dx=(ws_bar_10-ws_bar_2)/8
    elif z==10 :
        dU_dz=(3*ws_bar_10-4*ws_bar_5+ws_bar_2)/8
    epsilon=((g/theta_v_bar)*avg1)-(avg2*dU_dz)
    return epsilon

def kolmogorov_length(nu, epsilon):
    # Compute Kolmogorov microscale
    
    eta=((nu**3)/epsilon)**(1/4)
    return eta
    

