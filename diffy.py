# -*- coding: utf-8 -*-
"""
Program to play Diffy.
See reference by Trapa (2006):
    https://www.math.utah.edu/mathcircle/notes/diffybox.pdf
and Behn et al. (2005)
    https://uta-ir.tdl.org/uta-ir/handle/10106/25680
Kribs (co-author of above) compiled a detailed list of references:
    http://mathed.uta.edu/~kribs/diffy.html
"""
import math as m
import numpy as np
# import matplotlib.pyplot as plt


# helping routines
def calc_diff(values):
    """
    Calculate and return the differences, wrapping around.
    """
    # setup output array
    diffvs = 0.0 * values
    for i in range(0, len(values)):
        diffvs[i] = values[i] - values[i - 1]
    return diffvs

# Jang's favorite
##inputs = np.array([1, 2, 6, 8])
# irrational version of Jang's
##inputs = np.array([m.sqrt(2.0) - 0.35, m.sqrt(5.0) -
##                   0.2, m.sqrt(37.0), m.sqrt(67.0)])

# Try inputs with all irrational values
##inputs = np.array([m.sqrt(2), m.sqrt(3), m.sqrt(7), m.sqrt(11)])
##inputs = np.array([m.sqrt(2), m.sqrt(3), m.sqrt(5), m.sqrt(11)])
# ah-ha! discover "two negatives messes things up" rule; tweak above:
##inputs = np.array([m.sqrt(2), m.sqrt(3), m.sqrt(5)-0.001, m.sqrt(11)-0.10])
# integer approx to previous values:
##inputs = np.array([1,16,42,91])

# My infinite levels solution, values a, b, c, 1
# --> This produces a "moving peak" solution.
# with "a" a solution of:
#   a^4 -6a^3 +12a^2 -8a +1 = 0
# estimate "a" from graph, and adjust to get to level 37 0s.
inf_a = 0.160713245
# and then
inf_b = 2.0 * inf_a - inf_a**2
inf_c = (2.0 - inf_a) * inf_b
# set it up as the input:
inputs = np.array([inf_a, inf_b, inf_c, 1.0])

# can convert these to Trapa's values!
#  --> reverse, and subtract from 1.0
##inputs = 1.0 - np.array([1.0, inf_c, inf_b, inf_a])

# use Trapa's p.8 table values
# --> This produces a "fixed peak" solution.
##inputs = np.array([0.0, 1.0, 1.543689, 1.839286755])


# Show conversion to Trapa's 0, 1, x, y version:
diffy_std = (inputs - inputs[0])
diffy_std = diffy_std / diffy_std[1]
print("Trapa standard form for input: ")
print("   ", diffy_std)


# Do the interations...
level = 0

print("")
print("Start   :", inputs)
print("")

lastout = inputs

while ((level < 100) and (max(lastout) > 1.e-6)):
    outputs = calc_diff(lastout)
    level += 1

    print("Level", level, ":", outputs)
    lastout = abs(outputs)

# the end
