# -*- coding: utf-8 -*-
"""
This program models making
a spiral design by moving
a marker in a straight line
while it is writing
on a spinning white board.
"""

# use math functions from np
# since it is vectorized
# (so, don't need this:  import math)
import numpy as np
import matplotlib.pyplot as plt

# parameters to set and adjust
# ============================
Tmax = 2.0 * np.pi    # 2pi seconds
omega = 4.52  # total revolutions
# marker starting and ending points
marker_start = np.matrix(
    np.array([[-2.0], [3.0]]))
marker_end = np.matrix(
    np.array([[2.4], [-2.6]]))
# ============================

# Setup lists to fill with the
# location of the marker in
# white-board (rotating) coord.s
xs = []
ys = []
# and save marker motion in
# absolute (non-rotating) coord.s
mxs = []
mys = []

# setup an array of times
ts = np.linspace(0.0, Tmax, num=1000)

# go through the times...
for t in ts:
    # rotation angle and matrix
    theta = omega * t
    rot_mat = np.matrix(np.array(
        [[np.cos(theta), np.sin(theta)],
         [-1.0 * np.sin(theta), np.cos(theta)]]))

    # location of the marker in
    # non-rotating coord.s
    marker_loc = marker_start + (t / Tmax) * (marker_end - marker_start)
    # save this marker location
    mxs.append(marker_loc[0, 0])
    mys.append(marker_loc[1, 0])

    # convert marker location to
    # location on rotating board,
    # rotate using a matrix multiply
    point = rot_mat * marker_loc
    # and save this location
    xs.append(point[0, 0])
    ys.append(point[1, 0])

# Close the previous plot
plt.close()

# open a plot
plt.figure(1, [8, 8], frameon=False)

# setup axes based on max value
max_ax = max([max(xs), max(ys)])
plt.ylim(-1.0 * max_ax, max_ax)
plt.xlim(-1.0 * max_ax, max_ax)
plt.xlabel('x')
plt.ylabel('y')
# draw x,y axes on plot
plt.plot([-1.0 * max_ax, max_ax], [0.0, 0.0], 'b--')
plt.plot([0.0, 0.0], [-1.0 * max_ax, max_ax], 'b--')

# show the satta spiral
plt.plot(xs, ys, 'r')

# show the marker non-rotating path
plt.plot(mxs, mys, 'g')

plt.title('A Satta Spiral')

plt.show()
