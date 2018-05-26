# coding: utf-8
# three_body_2d.py
""" Use Docstrings like this so that help() can give useful output.
    These can be multi-line, that's nice ;-)
    Simple 3-body simulation constrained to 2D  """

# run it at os command line:
# osprompt> py three_body_2d.py

# v8 - adjusted to run in pythonista
# v7 - put previous comments at bottom; some tweaking for PEP8.
#      Include a 3D plot with t as the z axis (based on lines3d_demo.py)
#      (Test using git.)
# Shared as a gist:https://gist.github.com/f5fa24c52bc6d6087e3dc6f3c62ced09

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# max time to simulate
tmax = 6.0
# time step size
dt = 0.001

# include a "softening" parameter in the Force calculation
epsilon = 1.0e-4

# Gravitational constant... (here for completeness)
grav = 0.8

# variables and initial values for each body's x,y vx,vy and mass:
b1x = 1.0
b1y = 0.0
b1vx = 0.0
b1vy = 0.5
b1m = 3.0
b2x = -0.5
b2y = 0.86
b2vx = 0.5
b2vy = 0.0
b2m = 4.1
b3x = -0.5
b3y = -0.86
b3vx = -0.5
b3vy = 0.0
b3m = 3.9


# adjust the v's so that the CM is constant (total p = 0)
px = b1vx * b1m + b2vx * b2m + b3vx * b3m
dv = px / (b1m + b2m + b3m)
b1vx -= dv
b2vx -= dv
b3vx -= dv
# y axis
py = b1vy * b1m + b2vy * b2m + b3vy * b3m
dv = py / (b1m + b2m + b3m)
b1vy -= dv
b2vy -= dv
b3vy -= dv

##colors = np.random.rand(3)
colors = [0.07167369,  0.6313451, 0.98]

print()
print("(", b1x, b1y, ")  (", b2x, b2y, ")  (", b3x, b3y, ")")
print()
# print(colors)

# keep track of the locations, starting at
xs = [b1x, b2x, b3x]
ys = [b1y, b2y, b3y]

# coming into the Leapfrog loop they want "a0", so do this:
# calc distances squared - these are useful
r12sq = (b2x - b1x)**2 + (b2y - b1y)**2
r13sq = (b3x - b1x)**2 + (b3y - b1y)**2
r23sq = (b3x - b2x)**2 + (b3y - b2y)**2
# calc the forces
ftemp = grav * (b1m * b2m / r12sq) / np.sqrt(r12sq + epsilon)
f12x = ftemp * (b2x - b1x)
f12y = ftemp * (b2y - b1y)
ftemp = grav * (b1m * b3m / r13sq) / np.sqrt(r13sq + epsilon)
f13x = ftemp * (b3x - b1x)
f13y = ftemp * (b3y - b1y)
ftemp = grav * (b2m * b3m / r23sq) / np.sqrt(r23sq + epsilon)
f23x = ftemp * (b3x - b2x)
f23y = ftemp * (b3y - b2y)
# these forces can be used at step zero..
#
# do enough time steps to get to tmax
totalsteps = int(tmax / dt)
for thisstep in range(totalsteps):
    # create the x_n+1/2 values; they replace the current x's:
    b1x += 0.5 * dt * b1vx
    b1y += 0.5 * dt * b1vy
    b2x += 0.5 * dt * b2vx
    b2y += 0.5 * dt * b2vy
    b3x += 0.5 * dt * b3vx
    b3y += 0.5 * dt * b3vy
    # if it's the first time through add in acceleration:
    if (thisstep == 0):
        b1x += 0.25 * dt * dt * (f12x + f13x) / b1m
        b1y += 0.25 * dt * dt * (f12y + f13y) / b1m
        b2x += 0.25 * dt * dt * (-1.0 * f12x + f23x) / b2m
        b2y += 0.25 * dt * dt * (-1.0 * f12y + f23y) / b2m
        b3x += 0.25 * dt * dt * (-1.0 * f13x - f23x) / b3m
        b3y += 0.25 * dt * dt * (-1.0 * f13y - f23y) / b3m
    # do the force calculations for the x_n+1/2 values:
    # calc distances squared - these are useful
    r12sq = (b2x - b1x)**2 + (b2y - b1y)**2
    r13sq = (b3x - b1x)**2 + (b3y - b1y)**2
    r23sq = (b3x - b2x)**2 + (b3y - b2y)**2
    # calc the forces
    ftemp = grav * (b1m * b2m / r12sq) / np.sqrt(r12sq + epsilon)
    f12x = ftemp * (b2x - b1x)
    f12y = ftemp * (b2y - b1y)
    ftemp = grav * (b1m * b3m / r13sq) / np.sqrt(r13sq + epsilon)
    f13x = ftemp * (b3x - b1x)
    f13y = ftemp * (b3y - b1y)
    ftemp = grav * (b2m * b3m / r23sq) / np.sqrt(r23sq + epsilon)
    f23x = ftemp * (b3x - b2x)
    f23y = ftemp * (b3y - b2y)
    # update the velocities to v_n+1
    b1vx += dt * (f12x + f13x) / b1m
    b1vy += dt * (f12y + f13y) / b1m
    b2vx += dt * (-1.0 * f12x + f23x) / b2m
    b2vy += dt * (-1.0 * f12y + f23y) / b2m
    b3vx += dt * (-1.0 * f13x - f23x) / b3m
    b3vy += dt * (-1.0 * f13y - f23y) / b3m
    # update the positions to x_n+1
    b1x += 0.5 * dt * b1vx
    b1y += 0.5 * dt * b1vy
    b2x += 0.5 * dt * b2vx
    b2y += 0.5 * dt * b2vy
    b3x += 0.5 * dt * b3vx
    b3y += 0.5 * dt * b3vy
    # append them to the list
    xs += [b1x, b2x, b3x]
    ys += [b1y, b2y, b3y]

print("(", b1x, b1y, ")  (", b2x, b2y, ")  (", b3x, b3y, ")")
print()

# Show paths on 2D plot
fig2d = plt.figure(1)
plt.scatter(xs, ys, c=(int(len(xs) / 3)) * colors,
            s=20, alpha=0.5, edgecolors='face')
plt.show()

if 1 == 1:
        # Show paths in 3D
    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure(2)
    ax = fig.gca(projection='3d')

    # Make a z array - time!
    zs = dt * np.array(range(totalsteps))

    ax.plot(xs[0:3 * totalsteps:3], ys[0:3 * totalsteps:3], zs,
            label='Body 1')
    ax.plot(xs[1:3 * totalsteps:3], ys[1:3 * totalsteps:3], zs,
            label='Body 2')
    ax.plot(xs[2:3 * totalsteps:3], ys[2:3 * totalsteps:3], zs,
            label='Body 3')
    #ax.plot(x, y, z, label='parametric curve')
    #ax.plot(x, y, 0.5*z, label='squished curve')
    ax.legend()

    plt.show()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Previous versions info:
# v6 - all bodies moving, adjust parameters for fun... very sensitive.
# v5 - Implemented:  Leapfrog integration (remove the v4 A-B stuff)
#    https://msdn.microsoft.com/en-us/library/dn528554(v=vs.85).aspx
# Check/compare this to the v3 results:    * This is better, e.g., dt=0.05 not as bad. *
# dt=0.05:  ( 0.429118848385 1.71982512641 )  ( 0.393327671913 0.943054785555 )  ( -1.0 -0.86 )
# dt=0.03:  ( 0.449177825241 1.69442795657 )  ( 0.378174762019 0.960296617147 )  ( -0.9995 -0.86 )
# dt=0.01:  ( 0.487766620217 1.69262159742 )  ( 0.350414668134 0.962959806766 )  ( -1.0 -0.86 )
# dt=0.002: ( 0.487766620217 1.69262159742 )  ( 0.350414668134 0.962959806766 )  ( -1.0 -0.86 )
# dt=0.0001:( 0.490110100467 1.69129612836 )  ( 0.348699926487 0.963929662175 )  ( -1.0 -0.86 )
# v4 - added epsilon; tried to improve the interations, e.g. by using:
#   Two-step Adams-Bashforth (on https://en.wikipedia.org/wiki/Linear_multistep_method )
#      y_n+2 = y_n+1 + 3/2 dt f_n+1(t,y) - 1/2 dt f_n(t,y)
#   This didn't work... because v' is not f(t,v) ?
# v3 - set to two masses only by zeroing f13, f23; adjust v's for a wide orbit.
# Check numerical accuracy by looking at t=10 point vs dt, for simple "dv=a*dt, dx=v*dt" method:
# dt=0.05:  ( 0.279169636664 1.62654526791 )  ( 0.503046607319 1.01130834056 )  ( -1.0 -0.86 )
#  eps.1e-4 ( 0.278340759037 1.62615345622 )  ( 0.503653103143 1.01159503203 )  ( -1.0 -0.86 )
# dt=0.03:  ( 0.361276244657 1.65494013081 )  ( 0.442492991714 0.989190148188 )  ( -0.9995 -0.86 )
# dt=0.01:  ( 0.461599078445 1.68496607947 )  ( 0.369561649918 0.968561405263 )  ( -1.0 -0.86 )
# dt=0.005: ( 0.477366118664 1.68809842666 )  ( 0.358024791221 0.966269443908 )  ( -1.0 -0.86 )
# dt=0.002: ( 0.485886985153 1.68993737755 )  ( 0.351790010864 0.964923870083 )  ( -1.0 -0.86 )
# dt=0.001: ( 0.488567582574 1.69055396488 )  ( 0.349828598116 0.964472708628 )  ( -1.0 -0.86 )
# dt=0.0001:( 0.490911201825 1.69111267825 )  ( 0.348113754762 0.964063893965 )  ( -1.0 -0.86 )
#  eps.1e-4 ( 0.489854101957 1.69123302781 )  ( 0.34888724247  0.963975833309 )  ( -1.0 -0.86 )
# v2 - improve organization; use tmax; all 3 masses move.
# v1 - just starting...
