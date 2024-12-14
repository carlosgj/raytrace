import logging
import numpy as np
from utils import rotationMatrix

class Rays(object):
    # rays.N         [1x1] number of rays, N
    # rays.n2        [1x1] (current index of refraction)^2
    # rays.position  [Nx3] ray origins
    # rays.direction [Nx3] ray directions
    # rays.chief     [1x1] (set by source creator) index of chief ray
    # rays.opl       [Nx1] (set by intersection creator) current path length

    def __init__(self, positions, directions, chiefIndex, index=1.0, ):
        self.logger = logging.getLogger("Rays")
        self.positions = positions
        self.directions = directions
        self.chiefIndex = chiefIndex

        assert positions.shape == directions.shape
        self.N = positions.shape[0]

        self.index = index
        self.n2 = index**2

        self.OPL = np.zeros(self.N, dtype='double')

class PointSource(object):
    #diverging Generates a cone of diverging rays with half-angle NA uniformly
    #distributed in sine-angle
    # sourcePoint(position, direction, x, NA, Nrays) or
    # sourcePoint(aperture, Nrays, RefIndex)
    # aperture has position, direction, NA, local, n=RefIndex
    # position       [1x3] center of chief ray
    # direction      [1x3] direction of chief ray
    # x              [1x3] local x axis
    # NA             [1x1] half-angle of cone
    # nRays          [1x1] integer number of rays on radius
    # RefIndex       [1x1] scaling for ray direction

    def __init__(self, position, direction, x, NA, nRays=99, refIndex=1.0, name='Unnamed'):
        self.logger = logging.getLogger(f"PointSource::{name}")
        self.position = np.array(position)
        self.direction = np.array(direction)/np.linalg.norm(direction)
        self.x = np.array(x)
        self.NA = NA
        self.nRays = nRays
        self.refIndex = refIndex
        self.name = name

    def fromAperture(aperture, nRays=99, RefIndex=1.0, name='Unnamed'):
        x = aperture.local[1,:]
        self = PointSource(aperture.position, aperture.direction, x, aperture.NA, nRays=nRays, refIndex=refIndex, name=name)
        return self

    def makeRays(self):
        self.logger.info("Making rays...")
        cp = np.cross(self.direction, self.x)
        self.y = cp/np.linalg.norm(cp)

        # uniform grid sampling by angle
        U = self.NA/self.refIndex;
        dU = U * np.arange(-self.nRays, self.nRays)/self.nRays;
        self.logger.debug(f"U: {U}")
        if U > np.pi/4.0:
            self.logger.error('pointSource only works up to 45 deg')

        Ux, Uy = np.meshgrid(dU,dU)
        raysToInclude = (Ux**2 + Uy**2) <= U**2
        r, c = np.nonzero(raysToInclude)
        M = Ux.shape[0] #(2*Nr+1)^2
        N = np.count_nonzero(raysToInclude)
        self.logger.debug(f"M: {M} N: {N}")
        Ux = np.arcsin(Ux[raysToInclude])
        Uy = np.arcsin(Uy[raysToInclude])


        chiefIdx = np.ceil((2*self.nRays+2)*self.nRays+1)
        rpos = np.tile(self.position, (N,1))
        rdir = np.zeros([N,3])
        rays = Rays(rpos, rdir, chiefIdx, index=self.refIndex)
        #rays.n2 = RefIndex^2;
        #rays.N = N;

        #rays.map = np.empty([r c]) #full(sparse(r,c,1:N));
        rays.maskSize = [np.amax(r), np.amax(c)]
        rays.valid = np.full([N,1], True)

        z = self.direction.T * self.refIndex
        for i in range(N):
            th = -self.x * Uy[i] + self.y * Ux[i] #rotation vector
            angle = np.linalg.norm(th)
            if np.abs(angle) > 1e-18:
                axis = th/angle
            else:
                axis = np.identity(3)
            rays.directions[i,:] = rotationMatrix(axis, angle) @ z
            #  rays.direction(i,:) = QRotMatrix(th) * z
