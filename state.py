from recordtype import recordtype
import numpy as np
from collections import OrderedDict
from datetime import datetime


class BasicVehicleState(object):
    def __init__(self,other=None):
        self.ID = None
        self.position = {'x': None, 'y': None, 'z': None}
        self.velocity = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.counter = 0


    def getCSVLists(self):
        headers = []
        values = []

        headers.append('ID')
        values.append(self.ID)

        headers.append('Counter')
        values.append(self.counter)

        headers += ['x_pos','y_pos','z_pos']
        values  += [self.position['x'], self.position['y'], self.position['z']]

        headers += ['x_vel','y_vel','z_vel']
        values  += [self.velocity['x'], self.velocity['y'], self.velocity['z']]

        out = OrderedDict(zip(headers,values))
        return out



class FullVehicleState(BasicVehicleState):
    def __init__(self):
        super(FullVehicleState, self).__init__()
        self.time = 0.0

    def getCSVLists(self):
        base = super(FullVehicleState,self).getCSVLists()

        headers = base.keys()
        values = base.values()

        headers += ['time']
        values  += [self.time]

        out = OrderedDict(zip(headers,values))
        return out
        
