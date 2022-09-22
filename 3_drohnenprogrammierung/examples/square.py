#!/usr/bin/env python

from pycrazyswarm import *
import numpy as np

Z = 0.5
D = 2.0

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=Z, duration=1.0+D)
    timeHelper.sleep(1.0+D)

    positions = [np.array([0, 1, Z]), np.array([1, 1, Z]), np.array([1, 0, Z]), np.array([0, 0, Z])]

    for p in positions:
        for cf in allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + p

            cf.goTo(pos, 0, 1.0+D)
        timeHelper.sleep(1.0+D)

    allcfs.land(targetHeight=0.02, duration=2.0+D)
    timeHelper.sleep(2.0+D)