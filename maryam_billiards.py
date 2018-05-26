# -*- coding: utf-8 -*-
"""
This program simulates the path of a billiard ball moving within a polygon.
The program and its style are very crude with lots of room for improvement ;-)
- Dan Dewey 8/8/2017

Usage:
    Run the file in a python environment, e.g. spyder.
    There are six parameters that can be adjusted:
        verts: a list of the (x,y) vertices of the polygon
        ballx, bally, rise, run: initial location of the 'ball'
                                 and its x,y direction (run,rise)
        nsegments: the number of segments to be followed/plotted.
                   If set to 0, shows the starting location and direction.

Some related web pages and papers:
- Maryam Mirzakhani:
https://www.youcubed.org/resources/maryam/
http://www.newyorker.com/tech/elements/
               maryam-mirzakhanis-pioneering-mathematical-legacy
- Papers:
https://www.mfo.de/math-in-public/snapshots/files/billiards-and-flat-surfaces
https://web.stanford.edu/~amwright/BilliardsToModuli.pdf
- And for a complete boggling of the mind, the EMM 2015 paper:
https://arxiv.org/pdf/1305.3015.pdf

"""
# get the math items used
from math import sqrt, atan2, pi

# use plotting from matplotlib
import matplotlib.pyplot as plt


# Parameters to set and adjust
# ============================
# polygon vertices
# - clockwise around interior
# - if not closed an additional vertex (equal to first) will be added


# simple assymetric 'house':
verts = [(0,0),(0,2),(3,4),(5,2),(5,0)]
# symmetric version
##verts = [(1,0),(1,2),(3,4),(5,2),(5,0)]
# starting location and direction of the 'ball'
ballx = 2  # 1
bally = 1  # 1
rise = 1   # 1
run = 0.25 # 2


# very complex m:
verts = [(0,0),(1,1),(1,5),(0,5+2.0/3.0),
         (4,7),(3.5,5),(6,6),(8,6),(10,5),
         (12,6),(15,6),(16.5,4.5),(16.5,1),(17.5,0),
         (13,0),(14,1),(14,3),(13,4),(11.5,4),
         (10.5,3),(10.5,1),(11.5,0),(7,0),(8,1),(8,3),
         (6,4),(4,3),(4,1),(5,0)]
# starting location and direction of the 'ball'
ballx = 1
bally = 3+0.11
rise = 2
run = 5


# number of 'bounces' to do
# Use 1 to show starting configuration
nsegments = 200

# ============================


def close_polygon():
    # make sure the last point is the same as the first
    if verts[0] != verts[-1]:
        verts.append(verts[0])


def plot_polygon():
    # draw the polygon outline
    polyxs = []
    polyys = []
    for ivert in range(len(verts)):
        polyxs.append(verts[ivert][0])
        polyys.append(verts[ivert][1])
    plt.plot(polyxs, polyys, '-g')


def find_hit_edge():
    # Determine which edge of the polygon the ball will hit
    # Use the angles of the vertices as seen from the ball
    # and compare them with the angle of the ball's direction.
    # The 4-quadrant atan2(y,x) gives -pi to +pi , ccw angle w.r.t. x axis.
    # Use both atan2(y,x) and atan2(x,y) to avoid the problem of
    # the jump from -pi to pi.
    ball_angx = atan2(rise,run)
    ball_angy = atan2(run,rise)
    ##print("ball angle:", ball_angx, "  ", ball_angy)
    # angle of the first vertex
    ivert=0
    vertdx = verts[ivert][0]-ballx
    vertdy = verts[ivert][1]-bally
    last_angx = atan2(vertdy,vertdx)
    last_angy = atan2(vertdx,vertdy)
    # go through subsequent vertices to find an edge (or the edges)
    # that contains the balls direction
    edge_verts = []
    for ivert in range(1,len(verts)):
        vertdx = verts[ivert][0]-ballx
        vertdy = verts[ivert][1]-bally
        vert_angx = atan2(vertdy,vertdx)
        vert_angy = atan2(vertdx,vertdy)
        ##print("vert ang:", vert_angx, "  ", vert_angy)
        # ball angle between this and last angles in both x and y measures
        xang_ok = (ball_angx < last_angx) and (ball_angx >= vert_angx)
        yang_ok = (ball_angy > last_angy) and (ball_angy <= vert_angy)
        # if either x or y ang measures are straddling their -pi to pi zone,
        # then set that one to true to ignore it
        if (abs(last_angx - vert_angx) > 1.2*pi):
            xang_ok = True
        if (abs(last_angy - vert_angy) > 1.2*pi):
            yang_ok = True
        # is this the/an edge we're looking for
        if (xang_ok and yang_ok):
            edge_verts.append(ivert - 1)
        # save these for next edge
        last_angx = 1.0*vert_angx
        last_angy = 1.0*vert_angy
    # didn't find any?
    if len(edge_verts) == 0:
        return -1
    # found exactly one?
    if len(edge_verts) == 1:
        return edge_verts[0]
    # OK, more than one found... return the closest (slight kludge)...
    dist = 1e9
    closest = -1
    for this_edge in edge_verts:
        # use the midpoint for the edge distance calc
        xcent = (verts[this_edge][0]+verts[this_edge+1][0])/2
        ycent = (verts[this_edge][1]+verts[this_edge+1][1])/2
        this_dist = (xcent-ballx)**2+(ycent-bally)**2
        ##print(this_edge, "  ", this_dist)
        if this_dist < dist:
            dist = 1.0*this_dist
            closest = this_edge
    ##print("")
    return closest


def line_intersect(x1,y1,x2,y2,x3,y3,x4,y4):
    # Use two known points on each line and determinants to get
    # the intersection coordinates.
    #   https://en.wikipedia.org/wiki/Line-line_intersection
    # The denominator - should not be zero (not tested here)
    denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    # the numerators
    xnumer = (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)
    ynumer = (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)
    # the point of intersection
    return xnumer/denom, ynumer/denom


def intersect_reflect(hit_edge):
    # Find the interestion location and change the direction
    # Use these variables to be able to change the ball's values
    global ballx, bally, rise, run
    # set up to find the intersection
    x1 = ballx; y1 = bally
    x2 = ballx+run; y2 = bally+rise
    x3 = verts[hit_edge][0]; y3 = verts[hit_edge][1];
    x4 = verts[hit_edge+1][0]; y4 = verts[hit_edge+1][1];
    # and find it
    xinter, yinter = line_intersect(x1,y1,x2,y2,x3,y3,x4,y4)
    # move the ball to the intersection
    ballx = xinter
    bally = yinter
    # Reflect the direction of motion
    # Separate the direction vector into a vector along the edge
    # and one normal to the edge
    alongx = x4-x3
    alongy = y4-y3
    alongmag = sqrt(alongx*alongx+alongy*alongy)
    # dot product of direction and the along unit vector
    dir_dot_alonguv = (run*alongx+ rise*alongy)/alongmag
    # the direction component along the edge
    dir_alongx = dir_dot_alonguv*alongx/alongmag
    dir_alongy = dir_dot_alonguv*alongy/alongmag
    # subtract the along component to leave the normal component
    dir_normalx = run - dir_alongx
    dir_normaly = rise - dir_alongy
    # set the new, reflected direction to have -1 times the normal component
    run = dir_alongx - dir_normalx
    rise = dir_alongy - dir_normaly


def assemble_path(nsegs):
    # Assemble the locations of the desired number of paths
    if nsegs == 0:
        # just show initial location and direction
        pathxs = [ballx, ballx+run]
        pathys = [bally, bally+rise]
    else:
        # start at initial location
        pathxs = [ballx]
        pathys = [bally]
        # add on each segment of the path
        for iseg in range(nsegs):
            # find the edge the ball will hit;
            # hit_edge is the index of the first vertex on the edge going CW
            hit_edge = find_hit_edge()
            # didn't find an edge? maybe hit a vertex?
            if hit_edge < 0:
                # add some little wiggle to indicate this, and stop
                pathxs.append(ballx+0.1); pathys.append(bally-0.1)
                pathxs.append(ballx+0.1); pathys.append(bally+0.1)
                pathxs.append(ballx-0.1); pathys.append(bally+0.1)
                pathxs.append(ballx-0.1); pathys.append(bally-0.1)
                pathxs.append(ballx+0.1); pathys.append(bally-0.1)
                break
            # update the ball location (ballx, bally) and direction (rise, run)
            intersect_reflect(hit_edge)
            # add this to the output list
            pathxs.append(ballx)
            pathys.append(bally)

    return pathxs, pathys


# main program, called if this file is run
def maryam(nsegs):

    # make sure the polygon is closed
    close_polygon()

    # calculate the path:
    pathxs, pathys = assemble_path(nsegs)

    # Show the result with a plot
    # Close any previous plot
    plt.close()
    # open a plot, set its x,y size
    plt.figure(1, [9, 7], frameon=False)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Maryam Billiards Output  ('+str(len(pathxs)-1)+" segments)")

    # show the polygon
    plot_polygon();
    # add the path of the 'ball'
    plt.plot(pathxs, pathys, '-b')

    # show it
    plt.show()

if __name__ == "__main__":
    maryam(nsegments)


