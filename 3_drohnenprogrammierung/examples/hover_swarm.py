#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

HOVER_DURATION = 5.0

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    
    allcfs.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0 + HOVER_DURATION)
    allcfs.land(targetHeight=0.02, duration=2.0)
    timeHelper.sleep(2.0)