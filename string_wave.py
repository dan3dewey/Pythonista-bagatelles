# -*- coding: utf-8 -*-
"""
Program to simulate waves on a string.
"""
import math as m
import numpy as np
import matplotlib.pyplot as plt


# helping routines
def bump_func(xs_arg, low, high, btype):
    """
    Setup initial displacement distribution of a bump,
    either sine or triangular.
    """
    # check the case of a single float as input
    if isinstance(xs_arg, (int, float)):
        xs_in = np.array([float(xs_arg)])
        scalar = True
    else:
        xs_in = xs_arg
        scalar = False
    Ys_out = 0.0 * xs_in
    mid = (low + high) / 2.0
    diff = high - low
    for i in range(0, len(Ys_out)):
        if ((xs_in[i] > low) and (xs_in[i] < high)):
            if (btype == 1):
                # triangle shape
                Ys_out[i] = 1.0 - abs((xs_in[i] - mid) / (0.5 * diff))
            else:
                # sine bump
                Ys_out[i] = (
                    1.0 + m.cos(2. * m.pi / diff * (xs_in[i] - mid))) / 2.
    if scalar is True:
        return Ys_out[0]
    else:
        return Ys_out


def d2Ydx2(Ys, h):
    """
    Return the second spatial derivative of Ys w.r.t. x
    """
    second = 0.0 * Ys
    # skip the end points
    for i in range(1, len(Ys) - 1):
        second[i] = (Ys[i - 1] - 2.0 * Ys[i] + Ys[i + 1]) / (h**2)
    return second


def dYdx(Ys, h):
    """
    Return the first derivative of Ys w.r.t x
    """
    first = 0.0 * Ys
    # skip the end points
    for i in range(1, len(Ys) - 1):
        first[i] = (Ys[i + 1] - Ys[i - 1]) / (2.0 * h)
    return first


def calc_energy(Ys, Vs, Vel, h):
    """
    Calculate the total energy of the string
    E_total = mu*(h/2)*( Vel^2*Sum{(dy/dx)^2} + Sum{(dy/dt)^2} )
    The returned value is E_total/mu.
    """
    energy = Vel * Vel * sum(dYdx(Ys, h)**2)
    energy += sum(Vs * Vs)
    return (h / 2.0) * energy

"""
Comments on the different versions:
v1 - "bump" on string is evolved and moves at Vel.
v2 - waterfall plot starting with bump on string.
v3 - friction damping.
v4 - three types of damping: friction, velocity, vel^2(=viscosity)
v5 - sine wave driven.
v6 - calculated total energy of string
v7 - custom "bump drive" resonance example; added energy-vs-time plot
v8 - Cleaned up plots, etc.
     Can show standing waves and off-resonance beating effects.
     Adding damping removes the strong beating;
     can manually scan over the damped resonance.
"""
# Sone parameters:
xmax = 100.0
# total time and time-per-frame
tstop = 20.5  # 32.5
dtframe = 0.2

Vel = 50.0  # velocity = sqrt(T/mu)

damping = 0.5
damp_type = 0  # 2   # 0, 1, 2, 3

amp_drive = 0.10
# N*0.25 --> a standing wave resonance (0.25 is from 2*xmax/Vel)
# N*0.25 + 0.125 --> example of putting energy in, then taking it out
# N*0.25 + 0.25/m --> long beat time of m*(1/0.25)
freq_drive = 1.0 + 0.25 / 4.0  # cycles per time unit
omega_drive = 2.0 * m.pi * freq_drive

# The discretization parameters
# - spacing of "masses" in x
#   0.2 is OK based on getting the same Energy vs time
h = 0.20
# - size of simulation time step, factor times time-to-go-h
#   wow: 1.0 is a sharp upper limit for a factor that works
dt = 1.0 * h / Vel

# Spatial coordinate
xs = np.linspace(0.0, xmax, num=int(xmax / h))

# initial spatial distribution, t=0
#  - string at rest:
Y0s = 0.0 * xs
#  - string with bunp(s) on it
# Y0s = 0.2*(bump_func(xs, 17.0, 23.0, 0) + bump_func(xs, 55.0, 85.0, 0))

# initial velocity distribution
V0s = 0.0 * Y0s
# initial time
time = 0.0

# setup the working YS and Vs
Ys = 1.0 * Y0s
Vs = 1.0 * V0s

# the accelerations now, t=0
#   accels = Vel**2 * d2Ydx2(Ys,h)
# adjust the Vs using accels for 1/2 time step
Vs = Vs + (dt / 2) * (Vel**2 * d2Ydx2(Ys, h))

# We'll make a "waterfall" plot
# and show the dispacement at a bunch of "frames"
num_frames = int(tstop / dtframe) + 1
# spread them out using dYdtime
dYdtime = 1.0  # Y value is the time

# Close the previous plot(s)
plt.close()
plt.close()
plt.figure(1, [8, 8], frameon=False)

# setup plot and plot the starting frame
plt.subplot(1, 1, 1)
plt.ylim(-1.05 * 0.2, 1.05 * 0.2 + num_frames * dtframe * dYdtime)
plt.xlim(0.0, xs[-1])
plt.plot(xs, Y0s, 'r')
plt.ylabel('Displacement  at  Time (y-axis value)')
plt.xlabel('x (units)')
freq_str = "  --  Frequency = " + str(int(1000.0 * freq_drive) / 1000.0)
plt.title('String Displacement' + freq_str)
# plt.show()

# setup arrays to store the total energy in the string at each frame time
frame_Es = 0.0 * np.linspace(0.0, num_frames - 1, num=num_frames)
frame_ts = 0.0 * frame_Es
# and do the simulation
for iframe in range(0, num_frames):
    # -- do some time steps
    last_frame_time = time
    # do the time stpes in this frame
    for i in range(0, int(dtframe / dt)):
        # advance Ys by 1/2 a time step
        Ys = Ys + (dt / 2.0) * Vs
        time += dt / 2.0
        # set Ys[0] based on the driving function
        Ys[0] = amp_drive * m.sin(omega_drive * time)
        # update Vs using accels from the Ys at n+1/2
        Vs = Vs + dt * (Vel**2 * d2Ydx2(Ys, h))
        # include damping term
        # constants are adjusted for similar effects
        if (damp_type == 1):
            #  - kinetic friction, decreases to 0 in finite time
            Vs = Vs - dt * 0.3 * damping * Vs / (abs(Vs) + 0.001)
        if (damp_type == 2):
            #  - standard damping F_d = -mu*V, exponential decay
            Vs = Vs - dt * 0.7 * damping * Vs
        if (damp_type == 3):
            #  - v^2 damping, long-lived low amplitude
            Vs = Vs - dt * damping * 1.0 * abs(Vs) * Vs
        # advance Ys by another 1/2 a time step
        Ys = Ys + (dt / 2.0) * Vs
        time += dt / 2.0
        # set Ys[0] based on the driving function
        Ys[0] = amp_drive * m.sin(omega_drive * time)

    # done with this frame
    energy = calc_energy(Ys, Vs, Vel, h)
    print(int(1000.0 * time + 0.5) / 1000.0, " . . . Energy = ", energy)
    frame_Es[iframe] = energy
    frame_ts[iframe] = time
    # plot in blue first frame every integer time:
    if (int(last_frame_time + 0.1 * dtframe) == int(time + 0.1 * dtframe)):
        plt.plot(xs, Ys + time * dYdtime, 'g')
    else:
        plt.plot(xs, Ys + time * dYdtime, 'r')

# plot the energy vs time
if False:
    plt.figure(2, [10, 6], frameon=False)
    plt.plot(frame_ts, frame_Es, 'b')
    plt.xlabel("Time (units)")
    plt.ylabel("E_total")
    plt.title("Total Energy in String  vs  Time" + freq_str)

# and show the plot(s)!
plt.show()
