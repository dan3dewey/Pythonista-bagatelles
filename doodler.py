# -*- coding: utf-8 -*-
"""
This program models the LEGO "Doodler" Google it, and/or see:
    https://www.us.lego.com/en-us/mindstorms/community/robot?projectid=73d4591f-e964-4533-85fe-b608d3eb6a83
Briefly, a pen is at the end of a zig-zag expanding structure,
the left and right end points of the structure are connected to
to gears so they each end point moves in a circle.

Example: shown here is strucutre with n_zigzag = 3
  (three lengths from end point to tip; the Lego project has n_zig = 7);
  the length of each section in the diagram is L_zig = 3 (three "/"s)

       tip where the pen is
       /\
      /  \
    ./    \.
     \    /
      \  /
       \/
       /\
      /  \
     /    \
     L    R
   end points
The end points are attached a distance "radius" from the centers of
their gears, and the two gears centers are separated by 2*x_center distance.
"""

# use math functions from np
import numpy as np
# and plotting from matplotlib
import matplotlib.pyplot as plt

# parameters to set and adjust (see description above)
# ============================
# The mechanical setup:
n_zigzag = 7     # Lego online version has 7
L_zig = 7.0      # Lego design has spacong of 7 holes
x_center = 5.0   # Lego design has x_center = 5
radius = 1.58    # Lego design has radius = 1.58 = sqrt(1.5^2+0.5^2)
# The number of rotations for each gear before stopping,
# and the starting location (in rotations):
rot_l = 49
phi_l = -0.05
rot_r = -25
phi_r = -0.05
# FYI, the Lego page uses (effectively, note sign change too):
#    rot_l,'r = -49 & -50  (green in movie)
#             =  49 & -25  (blue in movie)
#    and Lego phi's look to be atan of 1/3 ~ 0.05 revs.
# ============================


def xys_of_rotations(rot_l, rot_r):
    """
    Calculate the location of the pen tip based on the
    amount of rotation of the two gears.
    """
    # convert rotations to radians (angle)
    theta_l = 2.0 * np.pi * rot_r
    theta_r = 2.0 * np.pi * rot_l
    # locations of the ends of the zig-zag from the angles,
    # note that they rotate in different directions
    # *** simple sin and cos use ***
    xl = -1.0 * (x_center + radius * np.cos(theta_l))
    yl = radius * np.sin(theta_l)
    xr = x_center + radius * np.cos(theta_r)
    yr = radius * np.sin(theta_r)
    # d is the half distance between the end points
    # *** distance formula ***
    d = np.sqrt((xr - xl)**2 + (yr - yl)**2) / 2.0
    # calculate the location of the tip of the zig-zag,
    # start at the midpoint of the two endpoints
    # *** midpoint formula ***
    xtip = (xl + xr) / 2.0
    ytip = (yl + yr) / 2.0
    # h is the extension distance of the zig-zag,
    # the "height" or distance of the tip from the midpoint
    # *** Pythagorean theorem ***
    h = n_zigzag * np.sqrt(L_zig**2 - d**2)
    # this distance is tilted from the vertical
    # by a tilt angle which has trig ratios:
    # *** simple trig, or similar triangles ***
    sintilt = 0.5 * (yr - yl) / d
    costilt = 0.5 * (xr - xl) / d
    # add the x and y components of the tilted height to the midpoint;
    # the x component of h is -h*sin(tilt)
    xtip = xtip - h * sintilt
    # the y component of h is hcos(tilt)\
    ytip = ytip + h * costilt
    # return the locations of the end points and writing tip
    # return (xl, yl, xr, yr, xtip, ytip)
    # or just the writing tip
    return (xtip, ytip)

# Setup a list of points to fill
xs = []
ys = []

# setup an array of times, from 0 to 1
Tmax = 1.0
ts = np.linspace(0.0, Tmax, num=2000)

# go through the times...
for t in ts:
    # evaluate the function for raotations at time t
    (xtip, ytip) = xys_of_rotations(rot_l * t + phi_l,
                                    rot_r * t + phi_r)
    xs.append(xtip)
    ys.append(ytip)

# Close the previous plot
plt.close()

# open a plot
plt.figure(1, [12, 12], frameon=False)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Doodler Output  [ rot_l = ' +
          str(rot_l) + ',  rot_r = ' + str(rot_r) + ' ]')

# set color to match Lego demo movie
if rot_r == -25 and rot_l == 49:
    plt.plot(xs, ys, '-b')
elif rot_r == -50 and rot_l == -49:
    plt.plot(xs, ys, '-g')
# or use red for other custom values
else:
    plt.plot(xs, ys, '-r')

plt.show()
