from recordtype import recordtype
import numpy as np
from collections import OrderedDict
from datetime import datetime



#################################################
#! This is the vehicle state class. This class is comprised of the BasicVehcleState() class
#  and the FullVehicleState() class.

#! Note that the BasicVehicleState() class contains general parameters for each vehicle. This
#  will be explained further when we begin to implement the commincation into this framework.

#! Note that the FullVehicleState() class uses the vehicle's BasicVehicleState() as its base. We use
#  a property called inheritance.

#################################################


#! We create a record type structure (mimics a c struct)
#                   ** This could probably be replaced by a list/dict **
Message = recordtype('Message', 'type,send_time,content', default=None )


#! Initiliaze the basic vehicle state class
class BasicVehicleState(object):
    def __init__(self,other=None):
        self.ID = None
        self.position = {'x': None, 'y': None, 'z': None}
        self.velocity = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.counter = 0


    #! This is not used in the threading_intro, but will be used when logging data
    def GetCSVLists(self):
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

        out = OrderedDict( zip(headers, values) )
        return out


#! Initialize the full vehicle state class using the basic vehicle state class as a base
class FullVehicleState(BasicVehicleState):
    def __init__(self):
        super(FullVehicleState, self).__init__()
        self.time = 0.0

    #! This is not used in the threading intro, but will be used when logging data
    def GetCSVLists(self):
        base = super(FullVehicleState, self).GetCSVLists()

        headers = list(base.keys())
        values = list(base.values())

        headers += ['time']
        values  += [self.time]

        out = OrderedDict( zip(headers, values) ) 
        return out
        
