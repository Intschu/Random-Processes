import numpy as np
import random as rand
import matplotlib.pyplot as plt

def trajectory_wiener(h, n_steps, x_ini): # sample trajectory for free Wiener noise
    # h = step size, n_steps = number of steps
    x = [x_ini] # initial position
    
    for j in range(n_steps):
        x.append(x[-1] + np.sqrt(2*d*h)*rand.gauss())
    return x

def trajectory_ou(h, n_steps, x_ini): # sample trajectory for Ornstein-Uhlenbeck process
    # h = step size, n_steps = number of steps
    x = [x_ini] # initial position
    
    for j in range(n_steps):
        x.append(x[-1] - x[-1]*h + np.sqrt(2*d*h)*rand.gauss())
    return x

def trajectory_flashing(h, n_steps, x_ini): # sample trajectory for flashing racket
    # h = step size, n_steps = number of steps
    x = [x_ini] # initial position
    
    for j in range(n_steps):
        x.append(x[-1] - h*(np.cos(x[-1]) + 0.5*np.cos(2.0*x[-1]) -f )*(1.0 + a*np.sign(np.sin(omega*j*h))) + np.sqrt(2*d*h)*rand.gauss())
    return x

def trajectory_rocking(h, n_steps, x_ini): # sample trajectory for rocking racket
    # h = step size, n_steps = number of steps
    x = [x_ini] # initial position
    
    for j in range(n_steps):
        x.append(x[-1] - h*(np.cos(x[-1]) + 0.5*np.cos(2.0*x[-1]) -f - a*np.sin(omega*j*h) ) + np.sqrt(2*d*h)*rand.gauss())
    return x

def trajectory_resonance(h, n_steps, x_ini): # sample trajectory for resonance
    # h = step size, n_steps = number of steps
    x = [x_ini] # initial position
    
    for j in range(n_steps):
        x.append(x[-1] - h*(-x[-1] + x[-1]**3  - a*np.sin(omega*j*h) ) + np.sqrt(2*d*h)*rand.gauss())
    return x

def trajectory_synchronization(h, n_steps, x_ini): # sample trajectory for synchronization
    return trajectory_resonance(h, n_steps, x_ini)

def sample_trajectories(h, n_steps, x_ini, n_samples, trajectory): # plot n_samples random trajectries
    # argument trajectory specifies stochastic process
    t = np.arange(0.0, h*n_steps + h, h) # time axis
    
    for j in range(n_samples):
        x = trajectory(h, n_steps, x_ini)
        plt.plot(t, x, label = f"data_{j+1}")
        #print(x[:50])
    
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("position")
    plt.show()
    
    return 0

def average(h, n_steps, x_ini, n_runs, trajectory): # average position and average position squared
    t = np.arange(0.0, h*n_steps + h, h) # time axis
    x_avg = [0.0 for j in range(1 + n_steps)] # average position at each time point
    x_avg_sq = [0.0 for j in range(1 + n_steps)] # average position squared at each time point
    
    for k in range(n_runs): # loop over random trajectories
        x = trajectory(h, n_steps, x_ini)
        x_avg = np.add(x_avg, x)
        x_avg_sq = np.add(x_avg_sq, np.multiply(x, x))
    
    x_avg = np.multiply(x_avg, 1/n_runs)
    x_avg_sq = np.multiply(x_avg_sq, 1/n_runs)
    
    return [x_avg, x_avg_sq]


def average_plot(h, n_steps, x_ini, n_runs, trajectory): # plot average position and average squared position
    t = np.arange(0.0, h*n_steps + h, h) # time axis
    avg = average(h, n_steps, x_ini, n_runs, trajectory)
    x_avg = avg[0] # average position at each time point
    x_avg_sq = avg[1] # average position squared at each time point
    
    plt.plot(t, x_avg, label = "average x")
    plt.plot(t, [np.exp(-j) for j in t], label = "e^(-t)")
    plt.plot(t, x_avg_sq, label = "average x^2")
    plt.plot(t, [1 for j in t], label = "1")

    plt.legend()
    plt.xlabel("time")
    plt.ylabel("position")
    plt.show()
    
    return 0


def speed_flashing(h, n_steps, x_ini, n_runs, a, f): # speed for flashing rocket
    # h = step size, n_steps = number of steps
    v = 0.0
    for k in range(n_runs) :
        x = x_ini # initial position
        for j in range(n_steps):
            x = x - h*(np.cos(x) + 0.5*np.cos(2.0*x) -f )*(1.0 + a*np.sign(np.sin(omega*j*h))) + np.sqrt(2*d*h)*rand.gauss()
        v += x/(h*n_steps)
    return v/n_runs


def speed_rocking(h, n_steps, x_ini, n_runs, a, f): # speed for rocking rocket
    # h = step size, n_steps = number of steps
    v = 0.0
    for k in range(n_runs) :
        x = x_ini # initial position
        for j in range(n_steps):
            x = x - h*(np.cos(x) + 0.5*np.cos(2.0*x) -f - a*np.sin(omega*j*h) ) + np.sqrt(2*d*h)*rand.gauss()
        v += x/(h*n_steps)
    return v/n_runs


def angular_velocity(h, n_steps, x_ini): # sample trajectory for resonance
    # h = step size, n_steps = number of steps
    x = x_ini # initial position
    phi = 0
    for j in range(n_steps):
        x = x - h*(-x + x**3  - a*np.sin(omega*j*h) ) + np.sqrt(2*d*h)*rand.gauss()
        if phi%2 == 0 :
            if x < -0.75 :
                phi += 1
        else :
            if x > 0.75 :
                phi += 1
    return phi*np.pi/(n_steps*h)


omega = 0.01
a = 0.25
f = 0.0

h = 2.0*np.pi/(omega*10000) # step size
n_steps = 1000000 # number of steps
n_runs = 1 # number of runs for averageing
n_samples = 1 # number of random trajectories
d = 0.01 # diffusion coafficient
x_ini = 0.0 # initial position


#sample_trajectories(h, n_steps, x_ini, n_samples, trajectory_synchronization)
#average_plot(h, n_steps, x_ini, n_runs, trajectory_synchronization)

"""
# plot speed for flashing/rocking as a function of F/A

f_axis = np.arange(-1.0, 1.1, 0.1)
a_axis = np.arange(-1.0, 1.1, 0.1)
v_axis = []
for a in a_axis:
    v_axis.append(speed_rocking(h, n_steps, x_ini, n_runs, a, f))
plt.plot(a_axis, v_axis, label = "speed")
plt.legend()
plt.xlabel("A")
plt.ylabel("speed")
plt.show()
"""

"""
# plot spectral amplification for resonance

d_axis = np.arange(0.0, 0.5, 0.05)
amplification_axis = [] # spectral amplification
for j in range(len(d_axis)):
    d = d_axis[j]
    x = average(h, n_steps, x_ini, n_runs, trajectory_synchronization)[0][int(n_steps/2):]
    amplification_axis.append((np.max(x)-np.min(x))**2/(2.0*a)**2) 
plt.plot(d_axis, amplification_axis, label = "amplification")
plt.legend()
plt.xlabel("D")
plt.ylabel("amplification")
plt.show()
"""

"""
# plot phase velocity
d_axis = np.arange(0.0, 0.22, 0.02)
phi_vel_axis = [] # spectral amplification
for j in range(len(d_axis)):
    d = d_axis[j]
    phi_vel_axis.append(angular_velocity(h, n_steps, x_ini)) 
plt.plot(d_axis, phi_vel_axis, label = "angular velocity")
plt.legend()
plt.xlabel("D")
plt.ylabel("angular velocity")
plt.show()
"""