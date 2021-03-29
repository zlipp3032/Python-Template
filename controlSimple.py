import time
import logging
from state import *
import os
import queue
import threading
import recordtype
import math as m
from numpy import linalg as LA
from datetime import datetime, timedelta
import numpy as np
import copy
import json



class Controller(threading.Thread):
    def __init__(self, start_time):
        threading.Thread.__init__(self)
        
        self.start_time = start_time
        self.vehicle_state = FullVehicleState()
        self.Ts = 0.1 # Loop time
        
        self.stop_request = threading.Event()


    def stop(self):
        self.stop_request.set()
        print("Stop flag set - Control")

        
    def run(self):
        while(not self.stop_request.is_set()):
            loop_start_time = datetime.now()
            self.vehicle_state.counter += 1
            print("Counter: ", self.vehicle_state.counter)
            
            time_to_wait = max(self.Ts - (datetime.now() - loop_start_time).total_seconds(),1E-6)
            print("time 2 wait:", time_to_wait,"\n\n")
            time.sleep(time_to_wait)

        self.stop()
        print("Control Stopped")
