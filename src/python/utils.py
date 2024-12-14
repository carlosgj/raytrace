import logging
import numpy as np


def rotationMatrix(axis, angle):
    #rotationMatrix a 3x3 Euler rotation matrix that operates on column vectors
    #B = (rotationMatrix(axis,angle) * A')'
    #
    #Input:
    #   axis [1x3]: Rotation axis (normalized)
    #   angle  [1]: Rotation angle (radians)
    #Output:
    #   Q [3x3]: Euler rotation matrix

    if np.abs(angle)>1e-18:
        cq   = np.cos(angle)   #cos(theta)
        sq   = np.sin(angle)   #sin(theta)
        omcq = 1.0 - cq        #1 - cos(theta)

        Q = [
            [omcq*axis[0]**2+cq,                omcq*axis[0]*axis[1]-sq*axis[2],    omcq*axis[0]*axis[2]+sq*axis[1]],
            [omcq*axis[1]*axis[0]+sq*axis[2],   omcq*axis[1]**2+cq,                 omcq*axis[1]*axis[2]-sq*axis[0]],
            [omcq*axis[2]*axis[0]-sq*axis[1],   omcq*axis[2]*axis[1]+sq*axis[0],    omcq*axis[2]**2+cq]
            ]
    else:
        Q = np.identity(3)

    return np.array(Q)
